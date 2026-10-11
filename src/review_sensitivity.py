"""Exploratory split/edge checks on reproduced, unchanged baseline inputs."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


def edge_mask(ref):
    padded = np.pad(ref, 1, constant_values=255)
    edge = np.zeros(ref.shape, bool)
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == dc == 0:
                continue
            neighbour = padded[1+dr:1+dr+ref.shape[0], 1+dc:1+dc+ref.shape[1]]
            edge |= (ref != 255) & (neighbour != 255) & (neighbour != ref)
    return edge


def agreement(pred, truth, mask):
    tp = int((pred & truth & mask).sum())
    fp = int((pred & ~truth & mask).sum())
    fn = int((~pred & truth & mask).sum())
    tn = int((~pred & ~truth & mask).sum())
    def ratio(a, b):
        return a/b if b else None
    return dict(tp=tp, fp=fp, fn=fn, tn=tn, precision=ratio(tp, tp+fp),
                recall=ratio(tp, tp+fn), f1=ratio(2*tp, 2*tp+fp+fn),
                iou=ratio(tp, tp+fp+fn))


def select_threshold(feature, truth, calibration):
    if min(int((calibration & truth).sum()), int((calibration & ~truth).sum())) < 50:
        raise ValueError('Calibration requires at least 50 cells in each reference class.')
    candidates = [(float(t), agreement(feature >= t, truth, calibration))
                  for t in np.linspace(-1, 1, 201)]
    return max(candidates, key=lambda row: (row[1]['f1'], row[0]))


def run(baseline, out):
    import rasterio
    if json.loads((baseline.parent/'run_status.json').read_text())['status'] != 'succeeded':
        raise ValueError('First reproduce the baseline successfully with run_submission.py.')
    data = baseline/'inputs'
    with rasterio.open(data/'previous/gmw2018_on_scl_grid.tif') as ds:
        ref, tx, crs = ds.read(1), ds.transform, ds.crs
    with rasterio.open(baseline/'geographic_split.tif') as ds:
        if ds.transform != tx or ds.crs != crs:
            raise ValueError('Split/reference grid mismatch.')
        split = ds.read(1)
    with rasterio.open(baseline/'2018-11-20_predictions.tif') as ds:
        if ds.transform != tx or ds.crs != crs:
            raise ValueError('Prediction/reference grid mismatch.')
        original = ds.read(1)
    truth = ref == 1
    eligible = original != 255
    south, north = split == 2, split == 1
    edge = edge_mask(ref)
    population = south & eligible
    disagreements = population & ((original == 1) != truth)
    groups = {}
    for name, mask in [('all_eligible_south', population),
                       ('disagreements', disagreements),
                       ('agreements', population & ~disagreements)]:
        total, touching = int(mask.sum()), int((mask & edge).sum())
        groups[name] = dict(cells=total, edge_cells=touching,
                            edge_fraction=touching/total if total else None)
    if groups['all_eligible_south']['cells'] != 5653 or groups['disagreements'] != dict(
            cells=121, edge_cells=96, edge_fraction=96/121):
        raise ValueError('Original audit population or edge definition does not reconcile.')

    # Repeat the original four-subpixel mean, not a resampled band or mean of ratios.
    rr, cc = np.indices(ref.shape)
    xs, ys = tx * (cc+.5, rr+.5)
    with rasterio.open(data/'previous/input_crops/SCL_crop.tif') as ds:
        if ds.transform != tx or ds.crs != crs or ds.shape != ref.shape:
            raise ValueError('SCL/reference grid mismatch.')
        valid = (ref != 255) & np.isin(ds.read(1), [4, 5, 6])
    means = {}
    for band in ('B04', 'B08'):
        with rasterio.open(data/'previous/input_crops'/f'{band}_crop.tif') as ds:
            if ds.crs != crs or not np.allclose(ds.res, [10, 10]) or ds.transform.b or ds.transform.d:
                raise ValueError('Expected native, north-up 10 m bands.')
            values, parts = ds.read(1), []
            for dx, dy in [(-5, -5), (-5, 5), (5, -5), (5, 5)]:
                c, r = (~ds.transform) * (xs+dx, ys+dy)
                if not np.allclose(c-np.floor(c), .5, atol=1e-6, rtol=0) or not np.allclose(r-np.floor(r), .5, atol=1e-6, rtol=0):
                    raise ValueError('Subpixel centres do not align.')
                c, r = np.floor(c).astype(int), np.floor(r).astype(int)
                within = (c >= 0) & (r >= 0) & (c < ds.width) & (r < ds.height)
                part = np.zeros(ref.shape, float)
                part[within] = values[r[within], c[within]]
                good = within & np.isfinite(part) & (part > 0)
                if ds.nodata is not None:
                    good &= part != ds.nodata
                valid &= good
                parts.append(part)
            means[band] = np.mean(parts, axis=0)
    denominator = means['B08'] + means['B04']
    feature = np.divide(means['B08']-means['B04'], denominator,
                        out=np.full(ref.shape, np.nan), where=denominator > 0)
    valid &= np.isfinite(feature)
    if not np.array_equal(valid, eligible):
        raise ValueError('Reconstructed eligibility differs from the original.')
    original_threshold = json.loads((baseline/'frozen_threshold.json').read_text())['threshold']
    if not np.array_equal((feature >= original_threshold)[eligible], (original == 1)[eligible]):
        raise ValueError('Reconstructed features do not reproduce original predictions.')
    threshold, calibration = select_threshold(feature, truth, south & eligible)
    original_south = agreement(original == 1, truth, population)
    original_north = agreement(original == 1, truth, north & eligible)
    stored = json.loads((baseline/'baseline_summary.json').read_text())
    for actual, expected in [(original_south, stored['held_out']['2018-11-20']['all_eligible_southern_cells']),
                             (original_north, stored['calibration'])]:
        if any(actual[k] != expected[k] for k in actual):
            raise ValueError('Original confusion counts/metrics changed.')
    report = {
        'status': 'succeeded_exploratory_sensitivity',
        'scope': 'GMW reference agreement, not independent cover accuracy or a causal edge diagnosis',
        'edge_definition': 'Any of eight neighbouring 20 m cells has a different 0/1 GMW value; outside-AOI 255 ignored.',
        'edge_populations': groups,
        'original': dict(threshold=original_threshold, north_calibration=original_north,
                         south_evaluation=original_south),
        'reverse_exploratory': dict(threshold=threshold, south_calibration=calibration,
                                   north_evaluation=agreement(feature >= threshold, truth, north & eligible)),
        'limitations': ['Both halves were already inspected; reversing them does not create an untouched holdout.',
                        'Cellwise edge proportions are descriptive and spatially dependent, not independent trials.',
                        'Different cover composition, source lineage and registration can affect agreement; this test does not isolate cause.'],
        'input_sha256': {str(p.relative_to(baseline)): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in sorted(baseline.rglob('*')) if p.is_file()},
    }
    out.mkdir(parents=True, exist_ok=False)
    (out/'review_sensitivity.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'input_sha256'}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    run(args.baseline, args.out)
