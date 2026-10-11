# What EO supplies, and what contact sensing must supply

8 October 2026 | Measurement requirements, not collected measurements

The drone proposal concerns observations missing from this satellite experiment. Adding hardware does not by itself improve the classifier. The [local water-contact rationale](WATER_CONTACT_RATIONALE.md) defines the question, and the [empty version 1.1 contract](../examples/inspection/water_context_question.json) records its measurement requirements.

## Do not overstate the satellite limitation

Our Sentinel-2 products supply dated RGB display and categorical scene labels. The experiment does not retrieve conductivity, salinity or water temperature. A "water" label gives no measurement at a specified depth and time, so these outputs alone cannot answer the proposed water-column question.

Satellites can retrieve salinity at other scales. NASA's description of RSS SMAP V5 includes 40 km and approximately 70 km products, with land-contamination limitations. Those footprints differ from channel-scale probe observations in our small coastal study rectangle. This comparison concerns scale and the quantity measured; the PoC has neither acquired nor evaluated SMAP pixels at Kalba. [NASA RSS SMAP V5](https://salinity.oceansciences.org/data-smap-v5.htm).

An optical proxy or future hyperspectral model would need its own physical model, local calibration and independent evaluation. Neither an image's appearance nor a catalogue intersection supplies that validation. Contact measurements could supply a different observable; they do not establish that an aircraft is necessary. Shore/boat probes, fixed loggers and USVs remain genuine alternatives.

## Define the measurement before comparing platforms

| Requirement to declare before a trial | Failure it prevents |
|---|---|
| Conductivity quantity, units and temperature-compensation convention; retain the measured in-situ value where available | Comparing an in-situ value with a value normalized to a reference temperature |
| Measured temperature, scale, timing and calibration; sensor identity and calibration standards/range with pre/post checks | Temperature, drift or an unsuitable calibration range masquerading as a site or platform difference |
| Sensor depth below a stated water-surface reference, uncertainty, sea-pressure treatment and justification | Confusing probe depth with total water depth or silently assuming zero pressure |
| Response/stability rule, placement/flow, cleaning and rotor/propeller/hull disturbance checks | Accepting an equilibrated but biased or contaminated reading |
| Common acceptance rule and explicit rejection reasons, fixed before the matched comparison | Giving one method an easier definition of a usable observation |

USGS distinguishes specific conductance normalized to 25°C from temperature-dependent conductivity. Its field manual addresses equipment, calibration, measurement and reporting. Do not pass a 25°C-compensated output into a conversion expecting in-situ conductivity without a documented valid reconstruction. This is a proposed data-handling safeguard, not a verified sensor procedure. [USGS explanation](https://nrtwq.usgs.gov/co/constituents/view/00095), [2019 field manual](https://doi.org/10.3133/tm9A6.3).

<a id="a-concrete-sensor-precedent--not-a-selected-payload"></a>

## Commercial sensor precedent

YSI's [EXO conductivity/temperature sensor, SKU 599870](https://www.ysi.com/product/id-599870/exo-conductivity--temperature-smart-sensor), provides a commercial example of the proposed observable:

| Quantity | Manufacturer-listed specification | Consequence for this PoC |
|---|---|---|
| Conductivity | 0–200 mS/cm; 0–100 mS/cm accuracy ±0.5% of reading or 0.001 mS/cm, whichever is greater; 100–200 mS/cm ±1%; T63 <2 s | Retain the quantity/range and calibration conditions. Response is not full observation acceptance. |
| Temperature | −5 to 50°C; accuracy ±0.01°C through 35°C, then ±0.05°C; T63 <1 s | A specification does not establish field uncertainty or a station difference. |
| Integration | Requires a compatible EXO sonde; the sensor does not function alone | Account for the complete logger/power/mounting chain, not a bare probe. No payload is selected. |

These figures come from the search-indexed manufacturer page; direct HTML retrieval failed, and its full current manual/test conditions were not verified. Treat them as a documented catalog precedent, not measured performance or a completed calibration procedure. No equipment was purchased, installed or tested.

Neither these response specifications nor the site evidence establishes a 150-second contact requirement. T63 is a partial-response metric, not T95/T99, thermal equilibration of the assembly, an averaging interval or a field stability rule. The resource model needs the measured time to an accepted observation. Its saved 30-second counterexample makes water support costlier under the assumed inputs; the 150-second saving remains hypothetical. Neither scenario establishes field dwell, and catalog response alone cannot determine complete mission cost.

A shore/boat probe, fixed logger, USV or aerial delivery method could use the same measurement technology. Sensor availability supports the observable, not the aircraft choice. The [task-specific comparison](WATER_CONTACT_RATIONALE.md#one-refutable-task-comparison) isolates those two questions.

## Salinity is a derived quantity with a domain

The official GSW function `gsw_SP_from_C(C,t,p)` expects conductivity in **mS/cm**, in-situ ITS-90 temperature in °C and **sea pressure** in dbar. Its Practical Salinity output is dimensionless. The documented PSS-78 validity range is `2 < SP < 42`; the function uses a modified Hill formulation below 2. An output outside a documented domain is not validated merely because software returns a number. [GSW input/output and domain documentation](https://teos-10.org/pubs/gsw/html/gsw_SP_from_C.html).

Absolute Salinity is a different output, in g/kg, with additional pressure/location inputs in GSW. Its `in_ocean` flag does not validate conditions at a coastal station. Practical Salinity cannot simply be relabelled as g/kg or equated with the historical "ppt" values. [GSW Absolute Salinity documentation](https://teos-10.org/pubs/gsw/html/gsw_SA_from_SP.html).

The historical Ramsar description reports interior values up to 44 **ppt**, but does not specify a measurement method or establish equivalence to Practical Salinity. It cannot justify a present conversion, an out-of-domain extrapolation, sensor range or a harm threshold. Keep conductivity and temperature as primary observations; derive salinity only after documenting the selected algorithm/version, scale, input conventions, validity domain and uncertainty. If that chain is unresolved, withhold derived salinity rather than invent it.

The research question remains a separately dated conductivity/temperature comparison. Its blank contract requires the declarations above, and future sensing and delivery tests must use the same acceptance rule. Conversion, sensor selection, field results, aircraft advantage, ecological diagnosis and planting decisions remain unestablished. The declarations document requirements; they do not implement an acceptance validator. Older executed notebooks preserve their version 1.0 preparation snapshots.
