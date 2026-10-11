# Experiment plan: MP-REFERENCE-SENSITIVITY-01

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
