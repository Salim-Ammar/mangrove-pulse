"""Replay saved scene-label summaries in Colab, with no raster/network acquisition.

This checks cache integrity and repeats descriptive counts. It is not independent
validation of the source product, AOI membership, field cover or drone claims.
"""
from __future__ import annotations

import hashlib
import io
import json

CACHE_SHA256 = "1f89eff69db90f6cecc2021cdbeb090bc23d1f4059d43c2063926eb9453df589"
REPORT_SHA256 = "ac95159b90196ca3fb47bcd0f43aedf92ab73a3fc5c39219246b5e14d477d611"
ITEM_ID = "S2C_MSIL2A_20260924T064621_R020_T40RDN_20260924T114716"


def run(cache_bytes: bytes, report_bytes: bytes) -> dict:
    import numpy as np

    checks = []

    def require(condition, label):
        if not condition:
            raise ValueError(label)
        checks.append(label)

    require(hashlib.sha256(cache_bytes).hexdigest() == CACHE_SHA256, "Exact retained crop hash")
    require(hashlib.sha256(report_bytes).hexdigest() == REPORT_SHA256, "Exact returned report hash")
    report = json.loads(report_bytes)
    require(report["item_id"] == ITEM_ID and report["acquisition_date"] == "2026-09-24",
            "Expected item and date")
    require(report["field_observations"] == report["independent_2018_labels"] == 0
            and report["sampling_stations"] == [] and report["deployment_authorized"] is False,
            "No empirical evidence or deployment authorization")
    require(report["spectral_indices_computed"] == [] and report["reflectance_bands_used"] == [],
            "No calibrated spectral analysis")
    schema = {
        "scl": ((112, 122), "uint8"), "scl_mask": ((112, 122), "bool"),
        "scl_inside": ((112, 122), "bool"), "tci": ((3, 223, 244), "uint8"),
        "tci_mask": ((223, 244), "bool"), "tci_inside": ((223, 244), "bool"),
        "scl_transform": ((6,), "float64"), "tci_transform": ((6,), "float64"),
    }
    with np.load(io.BytesIO(cache_bytes), allow_pickle=False) as cache:
        require(set(cache.files) == set(schema) | {"item_id", "crs"}, "Exact ten-field cache schema")
        require(cache["item_id"].shape == () and cache["item_id"].dtype.kind == "U"
                and str(cache["item_id"].item()) == ITEM_ID, "Cache item identity")
        require(cache["crs"].shape == () and cache["crs"].dtype.kind == "U"
                and str(cache["crs"].item()) == "EPSG:32640", "Cache projected CRS")
        for key, (shape, dtype) in schema.items():
            require(cache[key].shape == shape and cache[key].dtype == np.dtype(dtype),
                    "Cache shape/dtype: " + key)
        for key, resolution, report_key in (("scl_transform", 20, "scl"), ("tci_transform", 10, "tci")):
            affine = cache[key]
            require(bool(np.isfinite(affine).all()) and affine[0] == resolution
                    and affine[4] == -resolution and affine[1] == affine[3] == 0,
                    "Native north-up crop affine: " + key)
            source = report[report_key]["source_affine"]
            col = float((affine[2] - source[2]) / resolution)
            row = float((source[5] - affine[5]) / resolution)
            require(col >= 0 and row >= 0 and col.is_integer() and row.is_integer(),
                    "Crop origin lies on recorded source grid: " + key)
        # Reuse exact saved membership. This does not independently recompute the AOI.
        scl, source_mask, inside = cache["scl"], cache["scl_mask"], cache["scl_inside"]
        valid = inside & ~source_mask & (scl != 0)
        require(bool(valid.any()), "Nonempty valid SCL selection")
        require(bool(np.all(scl[valid] <= 11)), "SCL class domain")
        counts = {str(code): int(np.count_nonzero(valid & (scl == code))) for code in range(12)}
        masked = int(np.count_nonzero(inside & ~valid))
        require(counts == report["scl"]["valid_class_counts"], "Cached product-label counts reproduce report")
        require(masked == report["scl"]["masked_or_nodata_count"], "SCL masked/NoData count reproduces report")
        centres = int(np.count_nonzero(inside))
        require(centres == report["scl"]["aoi_cell_centres"] == 13401
                and sum(counts.values()) + masked == centres, "Native SCL centre-count closure")
        tmask, tinside = cache["tci_mask"], cache["tci_inside"]
        require(bool(np.all(tmask[~tinside])), "TCI outside-AOI pixels are masked")
        require(bool(np.any(tinside & ~tmask)), "Nonempty TCI display selection")
        require(int(np.count_nonzero(tmask)) == report["tci"]["masked_or_outside_aoi_pixel_count"],
                "TCI combined mask count reproduces report")
    return {
        "experiment_id": "MP-KALBA-OFFLINE-CONTEXT-01",
        "status": "succeeded_cached_summary_replay",
        "item_id": ITEM_ID, "acquisition_date": "2026-09-24",
        "cache_sha256": CACHE_SHA256, "returned_report_sha256": REPORT_SHA256,
        "numpy_version": np.__version__, "checks_passed": len(checks), "checks": checks,
        "native_20m_scl_counts": counts, "aoi_centres": centres,
        "eo_network_requests_in_reader": 0,
        "source_AOI_membership_recomputed": False,
        "independent_validation": False, "field_observations": 0,
        "independent_2018_labels": 0, "sampling_stations": [],
        "deployment_authorized": False, "reflectance_indices_computed": [],
        "not_inferred": report["not_inferred"],
        "limits": ["Replay of cached product labels, not field truth or current mangrove extent.",
                   "No historical overlay, chemical measurement, aircraft test or ecological outcome.",
                   "Network-free reader does not mean zero browser/notebook/save transfer overhead."],
    }
