# Attribution and limits

## Related research

SkyPlanter provides a published example of aerial seedling placement, but it does not test Mangrove Pulse's amphibious sensing concept: Lloyd, S.; Opstrup, T. K.; Ebeid, E. S. M.; Astrup, R. (2026). *SkyPlanter: Aerial Reforestation With an Ultralight, Seedling–Planting Drone*. IEEE/ASME Transactions on Mechatronics 31(2), 1617–1628; early online publication 2025. [DOI](https://doi.org/10.1109/TMECH.2025.3606620), [SDU publication record](https://portal.findresearcher.sdu.dk/en/publications/skyplanter-aerial-reforestation-with-an-ultralight-seedling-plant/).

<a id="separate-planet-tanager-qualification--11-may-2025"></a>
## Separate Planet Tanager qualification, 11 May 2025

Planet Tanager open data, item `20250511_074311_00_4001`, provider-labelled CC BY 4.0: [specific STAC source](https://www.planet.com/data/stac/tanager-core-imagery/coastal-water-bodies/20250511_074311_00_4001/20250511_074311_00_4001.json), [licence](https://creativecommons.org/licenses/by/4.0/). Modifications: projected visual/beta-mask display, predeclared central 64-by-64 window, three actual surface-reflectance channels, normalized red/NIR contrast and ETag-bound range caching. Small original visual/mask COGs and partial HDF5 byte blocks are included in `examples/tarif_qualification/results.zip`; not the full 1.11 GB cube. Specific provenance and limits: [Tarif qualification](docs/TARIF_SCENE_QUALIFICATION.md). No endorsement implied; optical measurements are not independent mangrove truth, water chemistry, drone implementation or ecological benefit. The returned archive's original catalogue attribution is preserved unchanged; this notice adds the specific item citation. The team code's licence is separate and remains unselected.

<a id="separate-dated-sentinel-2-context--24-september-2026"></a>
## Separate dated Sentinel-2 context, 24 September 2026

Contains modified Copernicus Sentinel data (2026), accessed through Microsoft Planetary Computer. Exact Sentinel-2C L2A item: `S2C_MSIL2A_20260924T064621_R020_T40RDN_20260924T114716`, PB 05.13. Modifications: small native SCL/TCI window extraction, study-rectangle centre/mask selection, categorical counts, labelled PNG displays and compressed native crop storage. No reflectance indices, historical overlay or model fitting. TCI retains provider uint8 display values without an additional adaptive stretch; SCL labels are not field truth or mangrove classes.

The exact returned source/specification, public unsigned STAC item, report, cache, status and figures are in `examples/recent_context/` with their original manifest. The item's licence link points to the [Sentinel data legal notice](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice); its [Copernicus-hosted text](https://cds.climate.copernicus.eu/licences/ec-sentinel) permits lawful reproduction, distribution and modification with source/modification notices and no data-quality or suitability warranty. Notice checked 8 October 2026. This is not blanket permission for third-party imagery, code or operation in the reserve; no provider endorsement is implied.

Bunting, Pete; Rosenqvist, Ake; Hilarides, Lammert; Lucas, Richard; Thomas, Nathan; Tadono, Takeo; Worthington, Thomas; Spalding, Mark; Murray, Nicholas; Rebelo, Lisa-Maria. (2022). Global Mangrove Watch (1996 - 2020) Version 3.0 Dataset. https://doi.org/10.5281/zenodo.6894273

CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
Modifications: two native tiles cropped; values sampled onto the SCL grid; imagery contrast stretched. No endorsement implied.
Contains modified Copernicus Sentinel data (2018), accessed previously through Microsoft Planetary Computer.
GMW is a separate extent reference, not field truth or a health label. The 2018 epoch is not the exact Sentinel acquisition date.
The specified historical experiment retains v3; it makes no claim that this is the latest or best release.

Additional modifications: November 30 Sentinel-2 crop, common-grid SCL comparison and shared-stretch displays. Contains modified Copernicus Sentinel data (2018).

Additional modifications: 2x2 mean red/NIR contrast, fixed geographic split, threshold predictions and GMW agreement statistics.

Additional modifications: frozen-prediction audit, connected components, cell/cluster tables and NIR inspection panels.

## Separate reference-context supplement

GMW v4.1.12: Bunting, P.; Hilarides, L.; Rosenqvist, A.; Oakes, G.; Castro Brandao Vaz dos Santos, P.; Worthington, T.; Rosenqvist, J.; Zanaga, D.; Van De Kerchove, R.; Tadono, T.; Kobayashi, K. (2026). Global Mangrove Watch: Timeseries of Mangrove Extent, version 4.1.12. https://doi.org/10.5281/zenodo.21346457 . CC BY 4.0. Modifications: local spatial selection, projection, clipping and membership at frozen grid centres. GMW v3 cached labels are retained for comparison, not replaced.

WorldCover: Zanaga, D. et al. (2021). ESA WorldCover 10 m 2020 v100. https://doi.org/10.5281/zenodo.5571936 . CC BY 4.0. © ESA WorldCover project 2020 / Contains modified Copernicus Sentinel data (2020) processed by ESA WorldCover consortium. Modifications: small native-grid crop and categorical centre sampling; maps and summary tables. It is later-date context and uses GMW auxiliary input, not independent November 2018 field truth.

Source-specific attribution and modifications are also preserved in `examples/reference_context/ATTRIBUTION.md`. New comparison figures display derived map labels, not Wayback/Maxar imagery pixels or the team's basemap screenshots. No provider endorsement is implied.

## Dated third-party occurrence metadata checked 9 October 2026

James Hardcastle / iNaturalist, observation [12260092](https://www.inaturalist.org/observations/12260092), via [GBIF 2542871866](https://www.gbif.org/occurrence/2542871866), *Avicennia marina*, 8 May 2018. The occurrence and photo are provider-labelled [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The team inspected the source photograph on 9 October; `evidence/gbif_2018_source_gate.json` records the metadata and qualification notes. Its location and species report do not label an entire 20 m cell or validate the 2018 cover map.

## Inspection handoff added 7 October 2026

Further modifications: selected 85 cached audit records from C001/C017/C027, retained original coordinates and map-label context, and reformatted them as proposed observation requests, original-centre GeoJSON points and blank return templates. No new spatial sampling or drone observations. The optional exporter retains these attributions. The energy-scenario extract is selected verbatim from the team's prior Colab analytical study; it contains hypothetical assumptions, not satellite data or measured drone performance. No blanket original-code licence is asserted.
