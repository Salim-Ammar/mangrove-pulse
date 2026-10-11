"""MP-REFERENCE-SENSITIVITY-01: separate team-run Colab experiment.
No model fitting, EO acquisition, ecological diagnosis or change attribution.
"""
import csv
import gzip
import hashlib
import json
import platform
import shutil
from pathlib import Path

EXPERIMENT = "MP-REFERENCE-SENSITIVITY-01"
AOI = [56.350, 24.986, 56.374, 25.006]
EXPECTED = {
    "gmw_v4112_2018_mng_ext_cntry_info_vec.gpkg.gz": {
        "size": 165428975,
        "sha256": "53eda1adad353cc349ae840cfba7e934dc7e2651769491bc2b367dcf2b597f96",
    },
    "ESA_WorldCover_10m_2020_v100_N24E054_Map.tif": {
        "size": 21292309,
        "sha256": "8ae908a79184d0bdf7a9a2335b5c7a0366e9e52a1c7197c4c926c38b880d1536",
    },
}
WC_LABELS = {
    0: "No data", 10: "Tree cover", 20: "Shrubland", 30: "Grassland",
    40: "Cropland", 50: "Built-up", 60: "Bare / sparse vegetation",
    70: "Snow / ice", 80: "Permanent water", 90: "Herbaceous wetland",
    95: "Mangroves", 100: "Moss / lichen",
}
LIMITATIONS = [
    "Reference-map sensitivity, not ecological or field accuracy.",
    "GMW epochs represent annual extents, not exact November observation dates.",
    "GMW v3 cached nearest-pixel labels and v4.1.12 vector point membership differ in release, source resolution and representation; differences cannot be attributed to one cause.",
    "Both GMW releases belong to the same product family; v4.1.12 uses optical and SAR imagery, including Sentinel-2. They are not independent field truth.",
    "WorldCover is later-2020 context, not validation of November 2018. Differences do not demonstrate growth, loss, tide, stress or map error.",
    "WorldCover uses Sentinel-1/Sentinel-2 and GMW among auxiliary inputs; independence cannot be assumed.",
    "WorldCover InputQuality is not uploaded. Class values do not supply local certainty.",
    "Zero GMW means not mapped, not proven absence. WorldCover zero is missing data, not background.",
    "Counts describe sampled 20 m grid centres, not native pixel counts, canopy fractions or confirmed mangrove area.",
    "Point membership includes polygon boundaries. No all-touched burn, alignment shifts, threshold retuning or split change.",
    "Review cases were already selected and inspected; comparisons are descriptive/post-hoc, not fresh held-out validation.",
    "No field observations, drone operations, planting needs, survival or carbon benefit are established.",
]
ATTRIBUTION = """# Sources and attribution

GMW v3: Bunting, P.; Rosenqvist, A.; Hilarides, L.; Lucas, R.; Thomas, N.;
Tadono, T.; Worthington, T.; Spalding, M.; Murray, N.; Rebelo, L.-M. (2022).
Global Mangrove Watch (1996-2020), Version 3.0.
https://doi.org/10.5281/zenodo.6894273
CC BY 4.0. Cached nearest-centre 2018 labels are embedded unchanged.
The original reference preparation sampled cropped source tiles onto the SCL grid.

GMW v4.1.12: Bunting, P.; Hilarides, L.; Rosenqvist, A.; Oakes, G.;
Castro Brandao Vaz dos Santos, P.; Worthington, T.; Rosenqvist, J.;
Zanaga, D.; Van De Kerchove, R.; Tadono, T.; Kobayashi, K. (2026).
Global Mangrove Watch: Timeseries of Mangrove Extent, version 4.1.12.
https://doi.org/10.5281/zenodo.21346457
CC BY 4.0, confirmed through the public Zenodo record API on 2026-09-30.
Modifications: AOI spatial filter, projection, clipping and grid-centre sampling.

WorldCover: Zanaga, D. et al. (2021). ESA WorldCover 10 m 2020 v100.
https://doi.org/10.5281/zenodo.5571936
CC BY 4.0. Attribution: © ESA WorldCover project 2020 /
Contains modified Copernicus Sentinel data (2020) processed by ESA WorldCover consortium.
Modifications: small native-grid crop and categorical centre sampling.

No endorsement is implied. Team case coordinates, original audit fields and
review notes are cached PoC evidence; notes are not field labels.
No third-party imagery pixels or team's basemap screenshots are embedded.

Primary documentation:
- https://esa-worldcover.org/en/data-access
- https://esa-worldcover.s3.eu-central-1.amazonaws.com/v100/2020/docs/WorldCover_PUM_V1.0.pdf
- https://pyogrio.readthedocs.io/en/latest/api.html
- https://shapely.readthedocs.io/en/stable/reference/shapely.intersects_xy.html
- https://rasterio.readthedocs.io/en/stable/topics/windowed-rw.html
"""
METHOD = """# Experiment plan: MP-REFERENCE-SENSITIVITY-01

Status: unexecuted until the team runs Colab. Created 2026-10-01.
Purpose: describe reference-map sensitivity for the frozen Khor Kalba PoC and
three already-reviewed cases; add clearly later-date 2020 land-cover context.

Preserve the cached GMW v3 raster/grid, original audit rows and case register.
Use all 13,401 AOI centres for the GMW map cross-tabulation, without a Sentinel
quality gate. This population differs from the original eligible southern
evaluation; no new model score is computed. Original threshold 0.49 and
north/south split with a 200 m gap remain unchanged.

Compare GMW v3 2018 with GMW v4.1.12 2018 on the EXACT cached EPSG:32640,
20 m centre coordinates. v4 labels are point intersections with polygons:
boundaries included, any polygon counts as mapped. Select a unique polygon
layer, transform the spatial-query bounds into its CRS, read only local
features, reject missing/invalid geometries rather than repairing silently,
project to the grid CRS, then clip to the grid bounds.

WorldCover v100 represents 2020. Read only a small native EPSG:4326 window
covering the frozen grid. For every grid centre, transform x/y to longitude/
latitude with always_xy=True and use the containing native raster pixel
(equivalent to nearest-centre sampling on this regular raster, subject to
ties at pixel boundaries). Never interpolate categorical class codes.
Masked native values become zero (missing), explicitly counted separately.
No source quality layer is supplied.

Report: GMW 2x2 reference cross-tab and Jaccard, full-AOI sampled WorldCover
class histogram, paired summaries for C001/C017/C027, and all 208 original
audit centres with added map values. Jaccard is map agreement, not accuracy.
No feature fitting, threshold search, shifting, field labels or causation.

These are release/representation/sampling comparisons. v3 and v4 native
sources have different representations/resolutions; differences alone cannot
isolate a release algorithm effect. WorldCover also uses GMW auxiliary input.

Checks: strict input sizes and SHA-256, embedded-file hashes, frozen raster
footprint, native WorldCover metadata/classes/coverage, unique case IDs and
expected case populations, audit label/coordinate consistency, synthetic
helper tests, same-grid output invariants and archive CRC/hash manifest.
Invalid/missing/ambiguous inputs stop the experiment and still produce a
diagnostic ZIP when the Colab runtime reaches the packaging cell.

ZIP includes source, tests, small embedded inputs, local clipped maps,
per-centre JSON, summaries, PNGs, methods, citations, environment and logs.
It excludes uploaded global datasets and private account information.
Do not publish/add to submission before inspecting returned results.
"""


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def dump(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def verify_input(path, expected):
    if Path(path).stat().st_size != expected["size"] or sha256(path) != expected["sha256"]:
        raise ValueError("Unexpected or changed input: " + Path(path).name)


def compare_binary(old, new, valid):
    import numpy as np
    old, new, valid = np.asarray(old), np.asarray(new), np.asarray(valid, bool)
    if old.shape != new.shape or old.shape != valid.shape:
        raise ValueError("Comparison grids differ.")
    if not np.isin(old[valid], [0, 1]).all() or not np.isin(new[valid], [0, 1]).all():
        raise ValueError("Nonbinary values in compared cells.")
    counts = {
        "both_not_mapped": int(np.sum(valid & (old == 0) & (new == 0))),
        "v3_only_mapped": int(np.sum(valid & (old == 1) & (new == 0))),
        "v4_only_mapped": int(np.sum(valid & (old == 0) & (new == 1))),
        "both_mapped": int(np.sum(valid & (old == 1) & (new == 1))),
    }
    union = sum(counts[k] for k in ("v3_only_mapped", "v4_only_mapped", "both_mapped"))
    total = int(valid.sum())
    changed = counts["v3_only_mapped"] + counts["v4_only_mapped"]
    return dict(counts, centres=total, differently_mapped_centres=changed,
                differently_mapped_fraction=changed / total if total else None,
                mapped_jaccard=counts["both_mapped"] / union if union else None,
                interpretation="Reference-map agreement, not field accuracy or ecological change")


def class_counts(values):
    import numpy as np
    vals, counts = np.unique(values, return_counts=True)
    if not set(int(v) for v in vals).issubset(WC_LABELS):
        raise ValueError("Unexpected WorldCover code.")
    return [{"code": int(v), "class": WC_LABELS[int(v)], "centres": int(n)}
            for v, n in zip(vals, counts)]


def polygon_labels(geometries, xs, ys):
    import numpy as np
    import shapely
    if not geometries:
        raise ValueError("No local GMW polygons: do not silently infer absence.")
    for geom in geometries:
        if geom is None or geom.is_empty or not geom.is_valid:
            raise ValueError("Empty/missing/invalid local geometry. No automatic repair.")
        if geom.geom_type not in ("Polygon", "MultiPolygon"):
            raise ValueError("Nonpolygon geometry.")
    return np.asarray(shapely.intersects_xy(shapely.union_all(geometries), xs, ys), dtype="uint8")


def sample_native(array, transform, xs, ys):
    import numpy as np
    xs, ys = np.asarray(xs), np.asarray(ys)
    if xs.shape != ys.shape:
        raise ValueError("Coordinate array shapes differ.")
    c, r = (~transform) * (xs, ys)
    c, r = np.floor(c).astype(int), np.floor(r).astype(int)
    within = (r >= 0) & (c >= 0) & (r < array.shape[0]) & (c < array.shape[1])
    sampled = np.zeros(xs.shape, dtype="uint8")
    sampled[within] = array[r[within], c[within]]
    return sampled, within


def write_grid(path, array, profile, description, **tags):
    import rasterio
    prof = profile.copy()
    prof.update(count=1, dtype="uint8", nodata=255, compress="deflate")
    with rasterio.open(path, "w", **prof) as ds:
        ds.write(array.astype("uint8"), 1)
        ds.update_tags(experiment=EXPERIMENT, description=description, **tags)


def run(inputs, embedded, out, scratch, layer_name=None):
    import numpy as np
    import rasterio
    import geopandas as gpd
    import pyogrio
    import pyproj
    import shapely
    from rasterio.features import geometry_window
    from rasterio.warp import transform_bounds
    from shapely.geometry import box, mapping
    out, inputs, embedded, scratch = map(Path, (out, inputs, embedded, scratch))
    checks = []

    def check(name, condition):
        checks.append({"check": name, "passed": bool(condition)})
        dump(out / "data_checks.json", checks)
        if not condition:
            raise ValueError("Data check failed: " + name)

    dump(out / "environment.json", {
        "python": platform.python_version(), "numpy": np.__version__,
        "rasterio": rasterio.__version__, "rasterio_gdal": rasterio.__gdal_version__,
        "geopandas": gpd.__version__, "pyogrio": pyogrio.__version__,
        "pyogrio_gdal": pyogrio.__gdal_version_string__, "pyproj": pyproj.__version__,
        "shapely": shapely.__version__,
    })
    for name, expected in EXPECTED.items():
        verify_input(inputs / name, expected)
        check("Uploaded checksum: " + name, True)
    with rasterio.open(embedded / "gmw3.tif") as ds:
        old, tx, crs, profile = ds.read(1), ds.transform, ds.crs, ds.profile.copy()
        bounds = ds.bounds
        check("Frozen north-up 20 m EPSG:32640 grid",
              crs.to_epsg() == 32640 and tx.a == 20 and tx.e == -20 and tx.b == 0 and tx.d == 0)
        grid = {"shape": list(old.shape), "transform": list(tx)[:6], "crs": str(crs),
                "bounds": list(bounds), "reference_sha256": sha256(embedded / "gmw3.tif")}
    inside = old != 255
    check("Frozen reference codes and counts",
          set(np.unique(old)).issubset({0, 1, 255}) and inside.sum() == 13401 and (old == 1).sum() == 1158)
    rr, cc = np.indices(old.shape)
    xs, ys = tx * (cc + .5, rr + .5)
    lon, lat = pyproj.Transformer.from_crs(crs, "EPSG:4326", always_xy=True).transform(xs, ys)
    dump(out / "grid.json", grid)
    source_aoi = json.loads((embedded / "AOI.geojson").read_text(encoding="utf-8"))
    check("AOI bbox unchanged", source_aoi.get("bbox") == AOI)

    gpkg = scratch / "gmw2018.gpkg"
    with gzip.open(inputs / "gmw_v4112_2018_mng_ext_cntry_info_vec.gpkg.gz", "rb") as src, gpkg.open("wb") as dst:
        shutil.copyfileobj(src, dst, length=1024 * 1024)
    check("Full gzip CRC/length", gpkg.stat().st_size == 824799232)
    layers = pyogrio.list_layers(gpkg).tolist()
    dump(out / "gmw_layers.json", {"layers": layers})
    polygons = [name for name, typ in layers if typ and "Polygon" in typ]
    if layer_name is not None:
        check("Explicit polygon layer exists", layer_name in polygons)
    else:
        check("One unambiguous polygon layer", len(polygons) == 1)
        layer_name = polygons[0]
    info = pyogrio.read_info(gpkg, layer=layer_name)
    dump(out / "gmw_layer_info.json", {
        "layer": layer_name, "crs": info["crs"], "geometry_type": info["geometry_type"],
        "features": int(info["features"]), "fields": info["fields"].tolist(),
        "total_bounds": list(info["total_bounds"]) if info["total_bounds"] is not None else None,
    })
    check("GMW CRS exists", bool(info["crs"]))
    # Query a small buffer beyond the grid; bbox must use the source layer CRS.
    query_box = transform_bounds(crs, info["crs"],
                                 bounds.left - 5, bounds.bottom - 5, bounds.right + 5, bounds.top + 5,
                                 densify_pts=21)
    local = pyogrio.read_dataframe(gpkg, layer=layer_name, columns=[], bbox=query_box,
                                  force_2d=True, on_invalid="raise")
    check("Local GMW polygons present", len(local) > 0)
    check("All source local geometries present and valid",
          not local.geometry.isna().any() and not local.geometry.is_empty.any() and local.geometry.is_valid.all())
    local = local.to_crs(crs)
    check("Projected local geometries valid", local.geometry.is_valid.all())
    clipped = [geom.intersection(box(*bounds)) for geom in local.geometry]
    clipped = [geom for geom in clipped if not geom.is_empty]
    new = polygon_labels(clipped, xs, ys)
    new[~inside] = 255
    check("New GMW grid retains exactly frozen AOI", np.array_equal(new != 255, inside))
    dump(out / "gmw_local_diagnostics.json", {
        "queried_features": len(local), "clipped_nonempty": len(clipped),
        "invalid_source_geometries": 0, "automatic_repairs": 0,
        "query_bbox_layer_crs": list(query_box), "point_boundary_rule": "intersects, boundary included",
        "note": "Local polygon presence is confirmed; unmapped areas are not proven absence.",
    })
    clipped_wgs = gpd.GeoSeries(clipped, crs=crs).to_crs(4326)
    dump(out / "gmw4_2018_clipped.geojson", {
        "type": "FeatureCollection",
        "features": [{"type": "Feature", "properties": {"source": "GMW v4.1.12", "epoch": 2018},
                      "geometry": mapping(geom)} for geom in clipped_wgs],
    })
    write_grid(out / "gmw4_2018_on_frozen_grid.tif", new, profile,
               "1=mapped, 0=not mapped, 255=outside frozen AOI; point boundary included", epoch="2018")

    wc_path = inputs / "ESA_WorldCover_10m_2020_v100_N24E054_Map.tif"
    with rasterio.open(wc_path) as ds:
        check("WorldCover exact native grid metadata",
              ds.crs.to_epsg() == 4326 and ds.shape == (36000, 36000) and ds.count == 1
              and np.allclose(ds.res, [1 / 12000, 1 / 12000], rtol=0, atol=1e-12)
              and np.allclose(list(ds.bounds), [54, 24, 57, 27]))
        crop_bounds = transform_bounds(crs, ds.crs, *bounds, densify_pts=21)
        win = geometry_window(ds, [mapping(box(*crop_bounds))], pad_x=2, pad_y=2)
        check("Small native read only", win.width * win.height < 2000000)
        native_masked = ds.read(1, window=win, masked=True)
        native = native_masked.filled(0).astype("uint8")
        native_tx = ds.window_transform(win)
        cp = ds.profile.copy()
        cp.update(width=native.shape[1], height=native.shape[0], transform=native_tx,
                  count=1, compress="deflate")
        native_cmap = ds.colormap(1)
        wc_meta = {"source": wc_path.name, "epoch": 2020, "version": "v100",
                   "native_crs": str(ds.crs), "native_resolution_degrees": list(ds.res),
                   "window": [win.col_off, win.row_off, win.width, win.height],
                   "native_masked_pixels_in_crop": int(np.ma.getmaskarray(native_masked).sum()),
                   "source_nodata": ds.nodata, "input_quality_available": False}
    check("WorldCover class codes valid in crop", set(np.unique(native)).issubset(WC_LABELS))
    with rasterio.open(out / "worldcover2020_native_crop.tif", "w", **cp) as ds:
        ds.write(native, 1)
        ds.write_colormap(1, native_cmap)
        ds.update_tags(epoch="2020", purpose="Later-date context, not 2018 field truth")
    wc, within = sample_native(native, native_tx, lon, lat)
    check("WorldCover spatial coverage of AOI", bool(within[inside].all()))
    wc_meta["aoi_missing_centres"] = int(((wc == 0) & inside).sum())
    wc[~inside] = 255
    check("WorldCover sampled grid retains frozen AOI", np.array_equal(wc != 255, inside))
    dump(out / "worldcover_metadata.json", wc_meta)
    write_grid(out / "worldcover2020_on_frozen_grid.tif", wc, profile,
               "2020 context; native-pixel categorical centre sample; 0=missing,255=outside AOI", epoch="2020")

    original_rows = list(csv.DictReader((embedded / "audit_cells_original.csv").read_text(encoding="utf-8").splitlines()))
    check("Original audit population", len(original_rows) == 208)
    check("Original audit cells unique",
          len({(int(d["row"]), int(d["column"])) for d in original_rows}) == 208)
    augmented = []
    for d in original_rows:
        r, c = int(d["row"]), int(d["column"])
        check_label = 0 <= r < old.shape[0] and 0 <= c < old.shape[1] and inside[r, c]
        if not check_label or int(d["gmw"]) != int(old[r, c]):
            raise ValueError("Original audit reference mismatch.")
        if abs(float(d["longitude"]) - lon[r, c]) > 1e-7 or abs(float(d["latitude"]) - lat[r, c]) > 1e-7:
            raise ValueError("Original audit coordinate mismatch.")
        augmented.append(dict(d, gmw_v4112_2018=int(new[r, c]), worldcover_v100_2020=int(wc[r, c]),
                              worldcover_class=WC_LABELS[int(wc[r, c])]))
    check("Audit labels and coordinates match frozen grid", True)
    dump(out / "audit_cells_with_context.json", augmented)

    case_register = json.loads((embedded / "case_reviews_original.json").read_text(encoding="utf-8"))
    check("Exactly three expected review cases", {d["case"] for d in case_register} == {"C001", "C017", "C027"} and len(case_register) == 3)
    case_reports = []
    for case in case_register:
        rows = [d for d in augmented if d["cluster_id"] == case["case"]]
        check(case["case"] + " original population", len(rows) == {"C001": 11, "C017": 32, "C027": 42}[case["case"]] == case["cells"])
        a = np.array([int(d["gmw"]) for d in rows], dtype="uint8")
        b = np.array([d["gmw_v4112_2018"] for d in rows], dtype="uint8")
        w = np.array([d["worldcover_v100_2020"] for d in rows], dtype="uint8")
        case_reports.append({"case": case["case"], "original_review": case,
                             "gmw_2018_reference_comparison": compare_binary(a, b, np.ones(a.shape, bool)),
                             "worldcover_2020_later_context": class_counts(w),
                             "cell_truth": "unresolved", "next_evidence": case["next_evidence"]})
    summary = {
        "experiment": EXPERIMENT, "result_type": "Descriptive reference sensitivity; no new model scores",
        "full_aoi_gmw2018": compare_binary(old, new, inside),
        "full_aoi_worldcover2020": class_counts(wc[inside]), "cases": case_reports,
        "limitations": LIMITATIONS,
    }
    dump(out / "comparison_summary.json", summary)
    dump(out / "case_comparison.json", case_reports)
    diff = np.full(old.shape, 255, dtype="uint8")
    diff[inside] = old[inside] * 2 + new[inside]
    write_grid(out / "gmw_reference_pairs.tif", diff, profile,
               "0=neither mapped;1=v4 only;2=v3 only;3=both;255=outside. Map differences, not ecological change.")
    render_maps(out, old, new, wc, inside, xs, ys, bounds, augmented, case_reports, native_cmap)
    totals = summary["full_aoi_gmw2018"]
    lines = [
        "# Returned reference-context comparison", "",
        "RESULT: Descriptive map sensitivity, not new model/field accuracy.", "",
        f"Full AOI: {totals['centres']} frozen 20 m centres.",
        f"GMW 2018: {totals['both_mapped']} mapped in both; {totals['v3_only_mapped']} v3-only; "
        f"{totals['v4_only_mapped']} v4-only; {totals['both_not_mapped']} mapped in neither.",
        "Differences are reference release/representation/sampling sensitivity, not confirmed 2018 ecological change.", "",
        "| Original case | Centres | v3-only | v4-only | Both mapped |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for d in case_reports:
        v = d["gmw_2018_reference_comparison"]
        lines.append(f"| {d['case']} | {v['centres']} | {v['v3_only_mapped']} | {v['v4_only_mapped']} | {v['both_mapped']} |")
    lines += ["", "WorldCover class histograms are in comparison_summary.json and case_comparison.json.",
              "WorldCover zero/missing values are counted separately; no quality layer was supplied.",
              "Original threshold, geographic split, predictions, audit categories and scores are unchanged.", "",
              "## Limits", ""] + ["- " + text for text in LIMITATIONS]
    (out / "RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary


def render_maps(out, old, new, wc, inside, xs, ys, bounds, rows, cases, native_cmap):
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap, BoundaryNorm
    from matplotlib.patches import Patch
    extent = (bounds.left, bounds.right, bounds.bottom, bounds.top)
    codes = sorted(WC_LABELS)
    colors = [tuple(v / 255 for v in native_cmap.get(code, (110, 110, 110, 255))[:3]) for code in codes]
    colors[0] = (0.9, 0.6, 0.9)
    wc_index = np.zeros(wc.shape, dtype="uint8")
    for i, code in enumerate(codes):
        wc_index[wc == code] = i
    palettes = [ListedColormap(["#e5e5e5", "#16835b"])] * 2 + [ListedColormap(colors)]
    norms = [BoundaryNorm([-.5, .5, 1.5], 2)] * 2 + [BoundaryNorm(np.arange(len(codes) + 1) - .5, len(codes))]
    arrays = [old, new, wc_index]
    titles = ["GMW v3 — 2018", "GMW v4.1.12 — 2018", "WorldCover v100 — 2020 context"]
    present = sorted(set(int(v) for v in wc[inside]))
    wc_legend = [Patch(facecolor=colors[codes.index(code)], label=str(code) + ": " + WC_LABELS[code]) for code in present]
    binary_legend = [Patch(facecolor="#e5e5e5", label="Not mapped"), Patch(facecolor="#16835b", label="Mapped")]
    case_colors = {"C001": "#aa00ff", "C017": "#e87700", "C027": "#080808"}

    def draw(name, selected=None):
        fig, axes = plt.subplots(1, 3, figsize=(15, 7), layout="constrained")
        for i, ax in enumerate(axes):
            ax.imshow(np.ma.array(arrays[i], mask=~inside), extent=extent,
                      cmap=palettes[i], norm=norms[i], interpolation="nearest")
            for case, color in case_colors.items():
                points = [d for d in rows if d["cluster_id"] == case and (selected is None or case == selected)]
                r = np.array([int(d["row"]) for d in points], int)
                c = np.array([int(d["column"]) for d in points], int)
                if len(r):
                    ax.scatter(xs[r, c], ys[r, c], s=18, marker="s", facecolors="none", edgecolors=color, linewidths=.8, label=case)
            if selected:
                points = [d for d in rows if d["cluster_id"] == selected]
                r = np.array([int(d["row"]) for d in points])
                c = np.array([int(d["column"]) for d in points])
                ax.set_xlim(xs[r, c].min() - 100, xs[r, c].max() + 100)
                ax.set_ylim(ys[r, c].min() - 100, ys[r, c].max() + 100)
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles=handles + (wc_legend if i == 2 else binary_legend), fontsize=7, loc="upper left")
            ax.set_title(titles[i], fontsize=10)
            ax.set_aspect("equal")
            ax.tick_params(labelsize=7)
            ax.ticklabel_format(useOffset=False, style="plain")
            ax.set_xlabel("Easting (m), EPSG:32640", fontsize=8)
        axes[0].set_ylabel("Northing (m), EPSG:32640", fontsize=8)
        fig.suptitle((selected + ": " if selected else "") + "Reference context — not field truth or ecological change", fontsize=12)
        fig.savefig(out / name, dpi=150)
        plt.close(fig)
    draw("reference_context_overview.png")
    for case in cases:
        draw(case["case"] + "_reference_context.png", case["case"])
