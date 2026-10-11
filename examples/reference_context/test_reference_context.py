"""Synthetic verification tests: executed only in the team's Colab runtime."""
import tempfile
import unittest
from pathlib import Path
import numpy as np
import rasterio
import pyogrio
import geopandas as gpd
from affine import Affine
from shapely.geometry import box, Polygon
from pyproj import Transformer
from reference_context import compare_binary, class_counts, polygon_labels, sample_native, write_grid, verify_input, sha256


class ContextTests(unittest.TestCase):
    def test_cross_tab(self):
        d = compare_binary([0, 0, 1, 1], [0, 1, 0, 1], [True] * 4)
        self.assertEqual([d[k] for k in ("both_not_mapped", "v4_only_mapped", "v3_only_mapped", "both_mapped")], [1] * 4)
        self.assertAlmostEqual(d["mapped_jaccard"], 1 / 3)

    def test_masked_values_not_compared(self):
        d = compare_binary([1, 255], [1, 99], [True, False])
        self.assertEqual(d["centres"], 1)
        self.assertEqual(d["mapped_jaccard"], 1)

    def test_no_union_is_undefined(self):
        self.assertIsNone(compare_binary([0], [0], [True])["mapped_jaccard"])

    def test_empty_population(self):
        d = compare_binary([255], [255], [False])
        self.assertEqual(d["centres"], 0)
        self.assertIsNone(d["differently_mapped_fraction"])

    def test_wrong_shape_rejected(self):
        with self.assertRaises(ValueError):
            compare_binary([[0]], [0], [True])

    def test_nonbinary_rejected(self):
        with self.assertRaises(ValueError):
            compare_binary([0], [95], [True])

    def test_worldcover_missing_separate(self):
        rows = class_counts(np.array([0, 95, 95, 80], dtype="uint8"))
        self.assertEqual({d["code"]: d["centres"] for d in rows}, {0: 1, 80: 1, 95: 2})

    def test_unknown_worldcover_code_rejected(self):
        with self.assertRaises(ValueError):
            class_counts(np.array([1]))

    def test_polygon_boundary_included(self):
        v = polygon_labels([box(0, 0, 1, 1)], np.array([0, .5, 2]), np.array([.5, .5, .5]))
        np.testing.assert_array_equal(v, [1, 1, 0])

    def test_empty_geometry_not_absence(self):
        with self.assertRaises(ValueError):
            polygon_labels([], np.array([.5]), np.array([.5]))

    def test_invalid_geometry_rejected(self):
        bowtie = Polygon([(0, 0), (1, 1), (0, 1), (1, 0), (0, 0)])
        with self.assertRaises(ValueError):
            polygon_labels([bowtie], np.array([.5]), np.array([.5]))

    def test_native_categories_not_interpolated(self):
        a = np.array([[10, 95], [80, 0]], dtype="uint8")
        tx = Affine(1, 0, 0, 0, -1, 2)
        v, within = sample_native(a, tx, np.array([.5, 1.5, .5, 1.5, 2.5]),
                                  np.array([1.5, 1.5, .5, .5, .5]))
        np.testing.assert_array_equal(v, [10, 95, 80, 0, 0])
        np.testing.assert_array_equal(within, [True, True, True, True, False])

    def test_coordinate_order(self):
        transformer = Transformer.from_crs(4326, 32640, always_xy=True)
        x, y = transformer.transform(56.362, 24.996)
        self.assertTrue(400000 < x < 500000 and 2700000 < y < 2800000)
        lon, lat = Transformer.from_crs(32640, 4326, always_xy=True).transform(x, y)
        np.testing.assert_allclose([lon, lat], [56.362, 24.996], atol=1e-8, rtol=0)

    def test_grid_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "grid.tif"
            a = np.array([[0, 1], [255, 1]], dtype="uint8")
            tx = Affine(20, 0, 435000, 0, -20, 2765700)
            prof = dict(driver="GTiff", width=2, height=2, crs="EPSG:32640", transform=tx)
            write_grid(path, a, prof, "synthetic")
            with rasterio.open(path) as ds:
                np.testing.assert_array_equal(ds.read(1), a)
                self.assertEqual(ds.transform, tx)
                self.assertEqual(ds.nodata, 255)

    def test_geopackage_bbox(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.gpkg"
            gdf = gpd.GeoDataFrame({"label": [1, 2]}, geometry=[box(0, 0, 1, 1), box(10, 10, 11, 11)], crs=4326)
            pyogrio.write_dataframe(gdf, path, layer="extent", driver="GPKG")
            self.assertEqual(pyogrio.list_layers(path).tolist()[0][0], "extent")
            local = pyogrio.read_dataframe(path, layer="extent", columns=[], bbox=(.2, .2, .8, .8))
            self.assertEqual(len(local), 1)

    def test_checksum_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "toy"
            path.write_bytes(b"toy")
            verify_input(path, {"size": 3, "sha256": sha256(path)})
            with self.assertRaises(ValueError):
                verify_input(path, {"size": 3, "sha256": "0" * 64})


if __name__ == "__main__":
    unittest.main(verbosity=2)
