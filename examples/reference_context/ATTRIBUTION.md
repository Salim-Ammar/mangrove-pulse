# Sources and attribution

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
