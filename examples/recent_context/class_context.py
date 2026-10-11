"""Display-only Sentinel-2 TCI and native-grid SCL context for the fixed AOI.

This module deliberately does not read reflectance bands or compute indices.
Call ``run(spec, item, out)`` in the prepared Colab runtime; signed asset URLs
are transient and are never returned, printed, or written to output files.
"""

from __future__ import annotations

import json
import math
import os
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


_ITEM_ID = "S2C_MSIL2A_20260924T064621_R020_T40RDN_20260924T114716"
_COLLECTION = "sentinel-2-l2a"
_BASELINE = "05.13"
_EXPECTED_CODES = set(range(12))
_PALETTE = {
    0: (0, 0, 0), 1: (255, 0, 255), 2: (80, 80, 80), 3: (180, 0, 0),
    4: (0, 150, 0), 5: (180, 150, 100), 6: (0, 100, 220), 7: (180, 180, 180),
    8: (255, 170, 0), 9: (255, 80, 0), 10: (220, 220, 255), 11: (240, 240, 240),
}
_LABELS = {
    0: "No data", 1: "Saturated/defective", 2: "Cast shadows", 3: "Cloud shadow",
    4: "Vegetation", 5: "Bare/non-vegetated", 6: "Water label", 7: "Unclassified",
    8: "Cloud, medium probability", 9: "Cloud, high probability", 10: "Cirrus",
    11: "Snow/ice",
}


def _safe_fail(stage: str, exc: BaseException) -> RuntimeError:
    # Do not include exception text: GDAL/network exceptions can contain SAS URLs.
    return RuntimeError(f"class-context run failed at {stage} ({type(exc).__name__})")


def _bounded_get(url: str, limit: int = 1_000_000) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "MangrovePulse-context/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise ValueError("unexpected HTTP status")
        if response.headers.get("Content-Length"):
            if int(response.headers["Content-Length"]) > limit:
                raise ValueError("response too large")
        body = response.read(limit + 1)
        if len(body) > limit or response.headers.get("Content-Type", "").lower().startswith("text/html"):
            raise ValueError("invalid or oversized response")
        return body


def _signed_asset(unsigned_href: str) -> str:
    parsed = urllib.parse.urlsplit(unsigned_href)
    if parsed.scheme != "https" or parsed.query or not parsed.hostname or not parsed.hostname.endswith(".blob.core.windows.net"):
        raise ValueError("unexpected unsigned asset")
    endpoint = "https://planetarycomputer.microsoft.com/api/sas/v1/sign?href=" + urllib.parse.quote(unsigned_href, safe="")
    signed = json.loads(_bounded_get(endpoint, limit=100_000))["href"]
    actual = urllib.parse.urlsplit(signed)
    if (actual.scheme, actual.hostname, actual.path) != (parsed.scheme, parsed.hostname, parsed.path) or not actual.query:
        raise ValueError("signed asset identity mismatch")
    return signed


def _asset_identity(item: dict[str, Any], key: str, suffix: str) -> tuple[str, dict[str, Any]]:
    assets = item.get("assets")
    if not isinstance(assets, dict) or key not in assets:
        raise ValueError("required asset missing")
    asset = assets[key]
    href = asset.get("href")
    parsed = urllib.parse.urlsplit(href or "")
    if (parsed.scheme != "https" or parsed.query or not parsed.hostname
            or parsed.hostname != "sentinel2l2a01.blob.core.windows.net"
            or not parsed.path.lower().endswith(suffix.lower())):
        raise ValueError("asset identity mismatch")
    expected_prefix = '/sentinel2-l2/40/R/DN/2026/09/24/S2C_MSIL2A_20260924T064621_N0513_R020_T40RDN_20260924T114716.SAFE/GRANULE/L2A_T40RDN_A010715_20260924T065959/IMG_DATA/'
    if parsed.path != expected_prefix + suffix:
        raise ValueError('Asset belongs to a different SAFE/granule')
    # The item is exact and these expected asset names identify the native products.
    roles = asset.get("roles", [])
    if not isinstance(roles, list) or "data" not in roles:
        raise ValueError("asset role mismatch")
    safe_meta = {"key": key, "host": parsed.hostname, "path": parsed.path,
                 "type": asset.get("type"), "roles": roles,
                 "file:size": asset.get("file:size"), "checksum:multihash": asset.get("checksum:multihash")}
    return href, safe_meta


def run(spec: dict[str, Any], item: dict[str, Any], out: str | os.PathLike[str]) -> dict[str, Any]:
    """Create dated display PNGs and unsigned local QA/provenance JSON.

    ``item`` is the unsigned STAC item. The returned result contains output
    filenames only; never pass signed URLs in ``item`` or ``spec``.
    """
    stage = "input_validation"
    try:
        import numpy as np
        import rasterio
        from rasterio.windows import from_bounds, Window
        from rasterio.warp import transform, transform_bounds
        os.environ['MPLBACKEND'] = 'Agg'
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.colors import ListedColormap, BoundaryNorm

        if not isinstance(spec, dict) or not isinstance(item, dict):
            raise ValueError("spec and item must be mappings")
        if (spec.get("item_id") != _ITEM_ID or item.get("id") != _ITEM_ID
                or item.get("collection") != _COLLECTION
                or item.get("properties", {}).get("s2:processing_baseline") != _BASELINE
                or spec.get("expected_processing_baseline") != _BASELINE):
            raise ValueError("item or baseline mismatch")
        bounds = spec.get("aoi_wgs84")
        if bounds != [56.350, 24.986, 56.374, 25.006]:
            raise ValueError("AOI mismatch")
        out_path = Path(out)
        out_path.mkdir(parents=True, exist_ok=True)
        scl_href, scl_meta = _asset_identity(item, "SCL", "R20m/T40RDN_20260924T064621_SCL_20m.tif")
        tci_href, tci_meta = _asset_identity(item, "visual", "R10m/T40RDN_20260924T064621_TCI_10m.tif")
        if [b.get('common_name') for b in item['assets']['visual'].get('eo:bands', [])] != ['red', 'green', 'blue']:
            raise ValueError('TCI band order not established')
        if not item['properties'].get('datetime', '').startswith('2026-09-24T06:46:21'):
            raise ValueError('Acquisition timestamp mismatch')
        signed_scl, signed_tci = _signed_asset(scl_href), _signed_asset(tci_href)

        # Prevent GDAL diagnostics from leaking signed URLs into notebook output.
        stage = "raster_read"
        env = {"GDAL_DISABLE_READDIR_ON_OPEN": "EMPTY_DIR",
               "CPL_VSIL_CURL_ALLOWED_EXTENSIONS": ".tif",
               "GDAL_HTTP_TIMEOUT": "30", "GDAL_HTTP_MAX_RETRY": "0",
               "CPL_LOG": os.devnull, "CPL_DEBUG": "OFF"}
        with rasterio.Env(**env):
            with rasterio.open(signed_scl) as sds, rasterio.open(signed_tci) as tds:
                if (sds.count != 1 or sds.dtypes != ("uint8",) or sds.crs is None
                        or sds.crs.to_epsg() != 32640 or tds.count != 3
                        or tds.dtypes != ("uint8", "uint8", "uint8") or tds.crs != sds.crs):
                    raise ValueError("raster band, dtype, or CRS mismatch")
                scl_affine, scl_nodata = list(sds.transform)[:6], sds.nodata
                tci_affine, tci_nodata = list(tds.transform)[:6], tds.nodata
                sx, sy = abs(sds.transform.a), abs(sds.transform.e)
                tx, ty = abs(tds.transform.a), abs(tds.transform.e)
                if not (math.isclose(sx, 20, abs_tol=0.01) and math.isclose(sy, 20, abs_tol=0.01)
                        and math.isclose(tx, 10, abs_tol=0.01) and math.isclose(ty, 10, abs_tol=0.01)):
                    raise ValueError("unexpected native resolution")
                if any(abs(v) > 1e-9 for v in (sds.transform.b, sds.transform.d, tds.transform.b, tds.transform.d)):
                    raise ValueError("rotated raster grid is unsupported")
                if any(ds.transform.a <= 0 or ds.transform.e >= 0 for ds in (sds, tds)):
                    raise ValueError('Unsupported raster axis directions')
                if not (sds.transform.c == tds.transform.c and sds.transform.f == tds.transform.f
                        and sds.width * 2 == tds.width and sds.height * 2 == tds.height):
                    raise ValueError('SCL and TCI source grid alignment mismatch')
                for ds, key in ((sds, 'SCL'), (tds, 'visual')):
                    if list(ds.transform)[:6] != item['assets'][key].get('proj:transform'):
                        raise ValueError('STAC/source transform mismatch')
                    if [ds.height, ds.width] != item['assets'][key].get('proj:shape'):
                        raise ValueError('STAC/source shape mismatch')
                def enclosing_window(ds, projected_bounds):
                    # Include all possible native cell centres; then apply the exact AOI predicate.
                    floating = from_bounds(*projected_bounds, transform=ds.transform)
                    c0, r0 = math.floor(floating.col_off), math.floor(floating.row_off)
                    c1 = math.ceil(floating.col_off + floating.width)
                    r1 = math.ceil(floating.row_off + floating.height)
                    if c0 < 0 or r0 < 0 or c1 > ds.width or r1 > ds.height:
                        raise ValueError('AOI not fully covered by source raster')
                    return Window(c0, r0, c1 - c0, r1 - r0)
                projected = transform_bounds("EPSG:4326", sds.crs, *bounds, densify_pts=21)
                swin = enclosing_window(sds, projected)
                if swin.width <= 0 or swin.height <= 0 or swin.width >= 1000 or swin.height >= 1000:
                    raise ValueError("SCL AOI window outside size limits")
                scl = sds.read(1, window=swin, masked=True)
                smask = np.ma.getmaskarray(scl).copy()
                svals = np.asarray(scl.data, dtype=np.uint8)
                st = sds.window_transform(swin)
                # Count only native SCL cell centres actually inside the WGS84 AOI.
                rows, cols = np.indices(svals.shape)
                xs = st.c + (cols + 0.5) * st.a + (rows + 0.5) * st.b
                ys = st.f + (cols + 0.5) * st.d + (rows + 0.5) * st.e
                lon, lat = transform(sds.crs, "EPSG:4326", xs.ravel().tolist(), ys.ravel().tolist())
                lon, lat = np.asarray(lon).reshape(xs.shape), np.asarray(lat).reshape(ys.shape)
                in_aoi = ((lon >= bounds[0]) & (lon <= bounds[2]) &
                          (lat >= bounds[1]) & (lat <= bounds[3]))
                raw_valid = in_aoi & ~smask
                raw_valid &= svals != 0  # SCL code 0 means NO_DATA even if TIFF nodata is absent.
                if sds.nodata is not None:
                    raw_valid &= svals != int(sds.nodata)
                if not in_aoi.any() or not raw_valid.any():
                    raise ValueError("no valid SCL AOI cells")
                unexpected = sorted(int(v) for v in np.unique(svals[raw_valid]) if int(v) not in _EXPECTED_CODES)
                if unexpected:
                    raise ValueError("unexpected SCL class values")
                valid_counts = {str(code): int(np.count_nonzero(raw_valid & (svals == code))) for code in range(12)}
                masked_count = int(np.count_nonzero(in_aoi & ~raw_valid))

                tprojected = transform_bounds("EPSG:4326", tds.crs, *bounds, densify_pts=21)
                twin = enclosing_window(tds, tprojected)
                if twin.width <= 0 or twin.height <= 0 or twin.width >= 1000 or twin.height >= 1000:
                    raise ValueError("TCI AOI window outside size limits")
                tci = tds.read((1, 2, 3), window=twin, masked=True)
                tmask = np.ma.getmaskarray(tci).any(axis=0)
                tvals = np.asarray(tci.data, dtype=np.uint8)
                tt = tds.window_transform(twin)
                if not np.isfinite(tvals).all():
                    raise ValueError("non-finite TCI samples")
                trows, tcols = np.indices(tmask.shape)
                txs = tt.c + (tcols + 0.5) * tt.a
                tys = tt.f + (trows + 0.5) * tt.e
                tlon, tlat = transform(tds.crs, "EPSG:4326", txs.ravel().tolist(), tys.ravel().tolist())
                tin_aoi = ((np.asarray(tlon).reshape(tmask.shape) >= bounds[0]) &
                           (np.asarray(tlon).reshape(tmask.shape) <= bounds[2]) &
                           (np.asarray(tlat).reshape(tmask.shape) >= bounds[1]) &
                           (np.asarray(tlat).reshape(tmask.shape) <= bounds[3]))
                tmask |= ~tin_aoi
                if not np.any(tin_aoi & ~tmask):
                    raise ValueError('No valid RGB display pixels in AOI')

                # Preserve the one acquired AOI crop for later offline Colab use.
                # No full scenes or signed URLs are retained.
                np.savez_compressed(out_path / 'native_context_cache.npz',
                    scl=svals, scl_mask=smask, scl_inside=in_aoi,
                    tci=tvals, tci_mask=tmask, tci_inside=tin_aoi,
                    scl_transform=np.asarray(list(st)[:6]),
                    tci_transform=np.asarray(list(tt)[:6]),
                    item_id=np.asarray(_ITEM_ID), crs=np.asarray('EPSG:32640'))

                common = dict(crs=sds.crs.to_string(), bounds_wgs84=bounds,
                              axis_labels=["UTM zone 40N easting (m)", "UTM zone 40N northing (m)"],
                              source="Microsoft Planetary Computer Sentinel-2 L2A",
                              acquisition_date="2026-09-24", item_id=_ITEM_ID,
                              notice="Display/context only; not field truth or ecological diagnosis.")
                # Native, unresampled provider TCI display; no scene-dependent stretch.
                rgb = np.moveaxis(tvals, 0, -1)
                rgb[tmask] = 0
                fig, ax = plt.subplots(figsize=(9, 9))
                fig.subplots_adjust(bottom=0.18)
                extent = (tt.c, tt.c + tt.a * twin.width, tt.f + tt.e * twin.height, tt.f)
                ax.imshow(rgb, extent=extent, interpolation="nearest", origin="upper")
                ax.set(xlabel=common["axis_labels"][0], ylabel=common["axis_labels"][1],
                       title="Provider Sentinel-2 TCI — display only (2026-09-24)")
                fig.text(0.06, 0.05, f"{_ITEM_ID}\nMicrosoft Planetary Computer / Copernicus Sentinel-2\nRGB display only; not field truth, water chemistry, ecological change or a flight route.", fontsize=8)
                fig.savefig(out_path / "dated_tci_display.png", dpi=150)
                plt.close(fig)

                # SCL stays native 20 m. Cell-centre AOI filter is applied for map display.
                display = np.ma.array(svals, mask=(~in_aoi) | (~raw_valid))
                cmap = ListedColormap([np.array(_PALETTE[i]) / 255 for i in range(12)])
                cmap.set_bad((1, 1, 1, 0))
                norm = BoundaryNorm(np.arange(-0.5, 12.5, 1), cmap.N)
                fig, ax = plt.subplots(figsize=(9, 10))
                fig.subplots_adjust(bottom=0.30)
                extent = (st.c, st.c + st.a * svals.shape[1], st.f + st.e * svals.shape[0], st.f)
                ax.imshow(display, cmap=cmap, norm=norm, extent=extent, interpolation="nearest", origin="upper")
                ax.set(xlabel=common["axis_labels"][0], ylabel=common["axis_labels"][1],
                       title="Sentinel-2 SCL labels — native 20 m grid (2026-09-24)")
                from matplotlib.patches import Patch
                handles = [Patch(facecolor=np.array(_PALETTE[i])/255, label=f'{i}: {_LABELS[i]}') for i in range(1, 12)]
                handles.append(Patch(facecolor='white', edgecolor='grey', label='NoData / masked / outside AOI'))
                fig.legend(handles=handles, loc='lower center', bbox_to_anchor=(0.5, 0.09), ncol=3, fontsize=8)
                fig.text(0.06, 0.025, f"{_ITEM_ID}\nMicrosoft Planetary Computer / Copernicus Sentinel-2\nProduct labels only; not validated cover, current chemistry, ecological change or permissions.", fontsize=8)
                fig.savefig(out_path / "native_scl_context.png", dpi=150)
                plt.close(fig)

        stage = "write_unsigned_reports"
        report = {
            "experiment_id": spec.get("experiment_id"), "status": "context_generated",
            "item_id": _ITEM_ID, "collection": _COLLECTION, "processing_baseline": _BASELINE,
            "acquisition_date": "2026-09-24", "aoi_wgs84": bounds,
            "assets": {"SCL": scl_meta, "visual": tci_meta},
            "scl": {"crs": "EPSG:32640", "native_resolution_m": [sx, sy],
                    "source_affine": scl_affine, "nodata_value": scl_nodata,
                    "window_shape_rows_cols": list(svals.shape), "aoi_cell_centres": int(in_aoi.sum()),
                    "valid_class_counts": valid_counts, "masked_or_nodata_count": masked_count,
                    "unexpected_values": unexpected, "counts_unit": "native 20 m cells",
                    "labels_are_ground_truth": False},
            "tci": {"crs": "EPSG:32640", "native_resolution_m": [tx, ty],
                    "source_affine": tci_affine, "nodata_value": tci_nodata,
                    "window_shape_rows_cols": list(tvals.shape[1:]), "rgb_band_order": [1, 2, 3],
                    "dtype": "uint8", "masked_or_outside_aoi_pixel_count": int(tmask.sum()),
                    "display_only": True, "stretch": "none; provider values displayed as uint8"},
            "outputs": ["dated_tci_display.png", "native_scl_context.png", "class_context_report.json", "native_context_cache.npz"],
            "reflectance_bands_used": [], "spectral_indices_computed": [],
            "sampling_stations": [], "field_observations": 0, "independent_2018_labels": 0,
            "historical_overlay": "Not produced in this implementation.",
            "unresolved_context": ["SCL classes are not field-validated here.",
                "TCI is a provider visualization and supports no calibrated colour or quantitative inference.",
                "No current water chemistry, ecological change, condition, depth, tide, navigability, access, or mission feasibility is established."],
            "not_inferred": spec.get("not_inferred", []),
            "deployment_authorized": False,
        }
        (out_path / "class_context_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        return {"status": "success", "outputs": report["outputs"], "out": str(out_path),
                "known_limits": report["unresolved_context"]}
    except Exception as exc:
        raise _safe_fail(stage, exc) from None
