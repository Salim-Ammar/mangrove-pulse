"""Validate and export cached inspection metadata; no geospatial calculations.

This checks traceability, not field accuracy, ecological need or aircraft safety.
The baseline/audit engines and their frozen experiment are never imported here.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

COUNTS = {'C001': 11, 'C017': 32, 'C027': 42}
OBSERVATION_FIELDS = (
    'case_id', 'cell_id', 'acquisition_datetime_with_timezone',
    'actual_observer_longitude', 'actual_observer_latitude', 'position_uncertainty_m',
    'method', 'sensor_and_calibration', 'visibility_and_occlusion', 'evidence_file',
    'evidence_redistribution_permission', 'qualified_cover_identification',
    'cover_fraction_if_supported', 'alignment_evidence', 'temporal_relevance',
    'quality_decision', 'quality_reason', 'reviewer', 'interpretation',
    'remaining_uncertainty',
)


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(root, requests=None, targets=None, returns=None):
    """Fail closed on metadata mismatches; return an auditable check summary."""
    root = Path(root).resolve()
    folder = root / 'examples/inspection'
    requests = read_json(folder / 'inspection_requests.json') if requests is None else requests
    targets = read_json(folder / 'inspection_targets.geojson') if targets is None else targets
    returns = read_json(folder / 'observation_return_template.json') if returns is None else returns
    with (root / 'examples/audit/all_audit_cells.csv').open(newline='', encoding='utf-8') as stream:
        original = list(csv.DictReader(stream))
    rows = [r for r in original if r['cluster_id'] in COUNTS]
    by_id = {f"{r['cluster_id']}_r{r['row']}_c{r['column']}": r for r in rows}
    contexts = read_json(root / 'examples/reference_context/audit_cells_with_context.json')
    context_by_id = {f"{r['cluster_id']}_r{r['row']}_c{r['column']}": r for r in contexts}
    comparisons = {r['case']: r for r in read_json(root / 'examples/reference_context/case_comparison.json')}
    require(len(rows) == len(by_id) == 85, 'Original selected audit rows must be 85 unique centres')
    require(requests.get('historical_satellite_dates') == ['2018-11-20', '2018-11-30'], 'Historical dates changed')
    require(targets.get('type') == 'FeatureCollection', 'Invalid GeoJSON container')
    features = targets.get('features', [])
    ids = [f.get('id') for f in features]
    require(len(ids) == len(set(ids)) == 85 and set(ids) == set(by_id), 'Target IDs missing, duplicated or changed')
    for feature in features:
        identifier = feature['id']
        row = by_id[identifier]
        props = feature['properties']
        require(feature.get('type') == 'Feature' and feature['geometry'].get('type') == 'Point', 'Invalid target geometry type')
        require(feature['geometry']['coordinates'] == [float(row['longitude']), float(row['latitude'])], 'Original target coordinates changed')
        require(all(props.get(k) == v for k, v in row.items()), 'Original audit fields changed')
        context = context_by_id[identifier]
        require(props.get('gmw_v4112_2018') == context['gmw_v4112_2018'], 'GMW context changed')
        require(props.get('worldcover_v100_2020') == context['worldcover_v100_2020'], 'WorldCover context changed')
        require(props.get('worldcover_class_2020') == context['worldcover_class'], 'WorldCover class changed')
        require(props.get('target_semantics') == 'original_historical_cell_centre_not_flight_waypoint', 'Targets are not operational waypoints')
        require(props.get('field_observation_status') == 'not_collected', 'Unexpected field-observation claim')
    cases = requests.get('cases', [])
    require(len(cases) == 3 and {c['case_id'] for c in cases} == set(COUNTS), 'Case set changed')
    for case in cases:
        cid = case['case_id']
        expected_ids = [f['id'] for f in features if f['properties']['cluster_id'] == cid]
        require(case['target_count'] == COUNTS[cid] and case['cell_ids'] == expected_ids, 'Case count or membership changed')
        require(case['reference_comparison_2018'] == comparisons[cid]['gmw_2018_reference_comparison'], 'Reference comparison changed')
        require(case['worldcover_2020_later_context'] == comparisons[cid]['worldcover_2020_later_context'], 'Later-date context changed')
        require(case['field_observations_collected'] == 0 and case['cell_truth'] == 'unresolved', 'Field truth is unresolved')
        require(case['planting_recommendation'] == 'none' and case['deployment_status'] == 'not_authorized_or_planned', 'No intervention or operational authorization established')
    require(returns.get('package_id') == requests.get('package_id') and returns.get('status') == 'unfilled', 'Return template/package mismatch')
    require(returns.get('schema_version') == '1.0', 'Unsupported observation return schema')
    record = returns.get('observation_record_template')
    require(isinstance(record, dict) and set(record) == set(OBSERVATION_FIELDS), 'Observation template fields missing or unexpected')
    require(all(v is None for v in record.values()), 'Observation template must remain empty')
    require(len(returns.get('cases', [])) == 3 and {c['case_id'] for c in returns['cases']} == set(COUNTS), 'Return case set changed')
    require(all(c.get('status') == 'not_collected' and c.get('observations') == [] and c.get('conclusion') is None and c.get('independent_2018_truth') == 'unresolved' for c in returns['cases']), 'No completed observation/conclusion exists')
    for relative, expected in requests.get('sources', {}).items():
        source = (folder / relative).resolve()
        require(source.is_relative_to(root) and source.is_file(), 'Unsafe or missing source path')
        require(hashlib.sha256(source.read_bytes()).hexdigest() == expected, 'Source fingerprint mismatch')
    require(len(requests.get('sources', {})) == 2, 'Expected two pinned source records')
    return {'status': 'format_and_traceability_passed', 'case_counts': COUNTS.copy(),
            'original_centres': 85, 'field_observations_collected': 0,
            'interpretation': 'Metadata integrity, not field validation or an approved drone mission'}


def export(root, out):
    """Export a fresh task folder only after metadata validation succeeds."""
    root, out = Path(root).resolve(), Path(out).resolve()
    require(not out.exists() or (out.is_dir() and not any(out.iterdir())), 'Export directory must be fresh and empty')
    summary = validate(root)
    out.mkdir(parents=True, exist_ok=True)
    source = root / 'examples/inspection'
    for name in ['inspection_requests.json', 'inspection_targets.geojson', 'observation_return_template.json']:
        (out / name).write_bytes((source / name).read_bytes())
    template = read_json(source / 'observation_return_template.json')
    columns = list(dict.fromkeys(['case_id', 'cell_id', 'target_longitude', 'target_latitude', 'observation_status'] + list(template['observation_record_template'])))
    with (out / 'observations_UNFILLED.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for feature in read_json(source / 'inspection_targets.geojson')['features']:
            writer.writerow({'case_id': feature['properties']['cluster_id'], 'cell_id': feature['id'],
                             'target_longitude': feature['geometry']['coordinates'][0],
                             'target_latitude': feature['geometry']['coordinates'][1], 'observation_status': 'not_collected'})
    (out / 'ATTRIBUTION.md').write_bytes((root / 'ATTRIBUTION.md').read_bytes())
    (out / 'README.md').write_text('# Historical Khor Kalba observation requests\n\n'
                                  '85 original cell centres; NOT flight waypoints, sampling locations or landing sites.\n'
                                  'No field observations, operational access or planting recommendation established.\n'
                                  'Current observations cannot directly validate November 2018 cover.\n', encoding='utf-8')
    (out / 'validation.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(export(args.root, args.out), indent=2))
