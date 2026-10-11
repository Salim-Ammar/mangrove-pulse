# Historical Kalba field evidence: what it adds

8 October 2026 | Third-party context, not team validation

The [Schile et al. (2016) Dryad dataset](https://datadryad.org/dataset/doi:10.15146/R3K59Z), DOI `10.15146/R3K59Z`, includes Kalba field records despite its Abu Dhabi project title. The team inspected the original workbook without modifying or recalculating it; the source link gives access to the dataset.

## Directly inspected source

In `plot information`, rows 77-100 contain East, North, South and West mangrove plot entries. East/North/South are dated 15/13/14 November 2014, respectively; West's date is `n.d.`. Salinity and pH entries exist for North/South/West; East has pH but blank salinity. The salinity header supplies no unit or scale.

North's six rows repeat one handheld-GPS coordinate (25.01736, 56.35649); West's six repeat another (25.00956, 56.35998). Both latitudes are north of our frozen AOI bound, 25.006. East/South coordinates are blank. Repeated coordinates do not locate individual plot footprints. None is an established location for C001, C017 or C027.

Related source tables use the spelling `Khalba`: `soil carbon data` rows 523-631 and `raw mature mangrove tree data` rows 1569-3440. The former separates total/inorganic/organic carbon and depth intervals; the latter includes DBH observations and allometric biomass/carbon formulas. Similar labels/dates suggest a possible join, but identities require checking before merging. Stocks and calculated biomass do not measure carbon gains.

The dataset's general methods describe soil/porewater sampling. Its prose also says the extended biogeochemical suite was not collected for 2014 mangroves, while the workbook contains 2014 salinity/pH entries. That unresolved scope conflict prevents assigning the whole method suite to these rows. Exact medium/depth, units, calibration and uncertainty need qualification. Missing entries remain missing, not zero or inferred values.

<a id="what-the-primary-methods-now-resolve"></a>

## Primary methods and remaining gaps

The [Dryad Methods section](https://datadryad.org/dataset/doi%3A10.15146/R3K59Z) describes shallow soil porewater collected from corer boreholes 5-10 cm below the surface. Salinity used a refractometer or chloride-based calculation; the description does not specify a salinity scale. Selected 2013 redox measurements used electrodes inserted 10 cm into soil for 1-20 minutes. These details describe the general acquisition methods, not every 2014 Kalba entry or a channel-water sensor's required dwell.

Mature-tree sampling refers to a 7 m plot without explicitly stating radius there; planted sites use 2 m-radius plots and salt-marsh radii vary from 1-4 m. These plot observations cannot establish complete satellite-pixel labels. The methods also leave the coordinate reference system and elevation datum unspecified. The Dryad dataset record gives a CC0 licence; that licence does not resolve the measurement or spatial-support gaps. The workbook remains unmodified and outside this repository.

Channel-water sensing must remain a separate water-column mission. The workbook's porewater salinity cannot serve as its reference value, acceptance threshold or current station locator. Root-zone or carbon questions need acquisition methods that the floating-probe concept does not implement.

## Spatial support and alternative-site checks

The cited [CIFOR mangrove carbon-assessment tutorial](https://www2.cifor.org/swamp-resources/PDF/C3_C-stocks_assessment_mangroves.pdf), slides 8-11, describes a 7 m-radius mature-tree plot, nested smaller plots, transect sampling and recorded plot-centre GPS positions. It helps interpret the protocol without establishing the precise geometry or coordinate reference system of each UAE workbook row. The UAE study also adapts the stem-size inclusion rule. Habitat at a plot centre cannot establish complete pixel cover, and nearby transect plots are not independent site replicates.

The [associated paper's indexed Methods, page 861](https://digitalcommons.fiu.edu/nanna/record/19941/files/FIDC006320.pdf?registerDownload=1&version=1&withMetadata=0&withWatermark=0), names Jubail for the 3/7/10-year planting sequence, while the retained workbook's `plot information` rows 153-167 label that sequence Eastern Mangrove. The full PDF retrieval was blocked; the stand identities need resolution before any alias merge. A planted-versus-natural comparison must first qualify populated measurements, locations, stand identities and sampling units. Even a valid cross-sectional comparison would measure neither the team's drone benefit nor planting-caused carbon gains.

## A concrete ecological constraint, not a demonstrated benefit

The same paper's indexed discussion, page 871, reports that Abu al Abyad plantations were about 50 cm lower in the tidal frame than Jubail plantations, with longer inundation and reduced growth up to 15-fold. The authors interpret this contrast as consistent with inundation stress. This is third-party, site-specific chronosequence evidence, not a randomized estimate or a transferable planting-height threshold. It supports a practical gate: establish tidal position and inundation exposure before recommending planting. A one-time channel conductivity/temperature pair does not measure that exposure; an appropriately referenced water-level record and site elevations would need a separate acquisition plan. No such records have been collected by the team.

The evidence therefore justifies a habitat-suitability question and attacks planting-by-cover-map alone. It does not show that our workflow improves establishment, survival, biodiversity or net carbon. Those outcomes still require a defined intervention, comparator, baseline and follow-up under the [ecological-benefit protocol](VALIDATION_AND_BENEFIT_TESTS.md).

## A dated alternative-site field-presence lead

A bounded [GBIF query for UAE Avicennia marina observations in 2018](https://api.gbif.org/v1/occurrence/search?country=AE&year=2018&limit=5&taxonKey=2925403), checked 9 October 2026, returned six records. This is one provider query, not an exhaustive inventory of UAE field evidence. The [retained metadata and qualification decision](../evidence/gbif_2018_source_gate.json) distinguish one comparatively precise candidate from broad or missing spatial support.

The original [iNaturalist observation 12260092](https://www.inaturalist.org/observations/12260092), mirrored as [GBIF 2542871866](https://www.gbif.org/occurrence/2542871866), reports Avicennia marina on 8 May 2018, at 24.4517416667 N, 54.4364916667 E near Abu Dhabi. Its provider-reported positional uncertainty is 5 m. The location is unobscured, its status is wild/non-captive and research grade, and two current identifications name that species (one categorized as improving, one as supporting). The record and associated photograph are CC-BY, credited to James Hardcastle / iNaturalist. The original photograph was loaded once and visually inspected in the browser on 9 October; it is neither bundled nor saved as a file. Research grade and reported uncertainty cannot guarantee accuracy or substitute for independent team measurements.

The photograph shows a ground/oblique view of trees, foliage, trunks/roots and shallow standing water. It is compatible with the provider's mangrove-presence identification, but this review is not botanical expert verification. No surveyed scale, organism footprint, aerial-cell boundary or complete cover fraction is visible, so the image cannot resolve camera-to-organism offset or whole-cell truth. Its date remains provider-reported, without independent verification from original image-file metadata. The [provider's observation guidance](https://help.inaturalist.org/en/support/solutions/articles/151000192921) describes an organism encounter and entering an observer location/accuracy circle; [research-grade rules](https://help.inaturalist.org/en/support/solutions/articles/151000169936) describe community identification and data-quality status. Neither certifies satellite registration. Acquiring another EO scene would not by itself make this record a pixel-accuracy reference.

The record supports dated third-party species presence and an alternative-site lead. It cannot supply a whole-cell cover label, independent accuracy of the frozen Khor Kalba map, proof of absence elsewhere or a drone/ecological outcome. An organism's position and photograph do not establish complete canopy cover in a 20 m cell, and May presence cannot directly validate November cover. The two identifications are not two field replicates; the record supplies neither a probability sample nor a negative-reference set.

This is a more precisely dated field-presence lead than an undated land-cover point, but not sufficient reason to discard the executed Kalba case. A separate Abu Dhabi experiment must first qualify photographic identification, organism/location support, date-matched EO inputs and an evaluable sampling design. It must run separately in Colab, preserve the frozen core and report only the endpoint its evidence actually supports. No such experiment or site switch is claimed here.

## The practical EO-to-drone connection

Kalba/Khalba-labelled records provide a local field-method lead. They motivate specifying separate below-canopy/soil quantities without assigning the general method suite to particular dated plots. Our EO workflow supplies traceable cover questions; a field protocol must specify the different quantity, location, date and measurement support it needs.

The proposed channel-water study would collect separately dated, calibrated conductivity/temperature observations and compare amphibious supported delivery against simpler methods under the [same measurement contract](OBSERVABLES_AND_MEASUREMENT_CHAIN.md).

The concept supplies no borehole porewater, sediment cores, tree diameter or laboratory soil carbon. A floating probe does not automatically observe the root zone; those quantities need separate methods, none of which is implemented. The historical records cannot select a present station or establish current stress, planting need, 2018 cover accuracy, drone superiority or ecological benefit.

This strengthens the [local research rationale](WATER_CONTACT_RATIONALE.md) without changing the frozen threshold, split, map scores or blank team observations. It is source-qualified historical context, not a new statistical/geospatial experiment.
