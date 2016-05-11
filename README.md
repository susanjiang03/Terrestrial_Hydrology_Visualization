Terrestrial Surface Water State Indicators
==========================================

I. Project Summary
------------------

Terrestrial surface hydrologic state variables provide unique insight into linkages and feedbacks
in terrestrial energy, water and carbon cycles and allow examination to the response of the +of
abiotic, biotic (ecosystem), and anthropogenic impacts (Bogardi et al., 2013) and when considered
alone are poor indicators of climate change (Vörösmarty, 2002). As a critical element of the Earth
system, terrestrial surface hydrologic state variables such as landscape freeze/thaw (FT), Surface
inundation fraction (Fw), Snow Water Equivalent (SWE) and surface radiative flux have influence
on important ecosystem services associated with human well-being, strongly influencing the
condition of the biosphere both for humans as well as for other terrestrial organisms. Carefully
tracking the combination of these state variables in conjunction with the ecosystem services they
influence supports assessment of their mutual linkages as well as determination of the linkages of
a variety of ecosystem services to changing climate.

---
II. Indicators
--------------

###a. Land Surface Freeze/Thaw State

#### Description
The freeze/thaw (F/T) state of the ground over North America has been characterized using
microwave frequency active and passive remove sensing data combined to produce a unified F/T
product. These sensors are able to detect, through a dynamic temporal response in backscatter or
brightness temperature, the change in the bulk dielectric constant of the observed landscape as it
transitions from frozen to thawed or vice versa.

#### Source
MeaSUREs FT-ESDR (1978-2013) Daily Products: Passive microwave derived surface freeze/thaw state. Derived globally from SSMR and SSM/I. 1992-2013 Link:http://freezethaw.ntsg.umt.edu/

###b. Surface Inundation
####Description
The state of surface inundated area fraction (Fw) for North America is assembled from the global time series of the NASA Inundated Wetlands Earth System Data Record (ESDR)(http://wetlands.jpl.nasa.gov). Passive and active microwave data from the Advanced Microwave Scanning Radiometer-EOS (AMSR-E) on NASA’s Earth Observing System (EOS) Aqua Satellite and radar backscatter from NASA’s SeaWinds scatterometer on the QuikSCAT satellite platform
(QSCAT) provide the basis for the construction of this global time series inundated area fraction dataset.
####Source
MeaSUREs IW-ESDR (1992-2013) 10-day composites Fractional inundated area from QuikSCAT, ASCAT, SSM/I,AMSR-E http://wetlands.jpl.nasa.gov

###c. Snow Water Equivalent (SWE)
####Description
The daily estimate of snow water equivalent (SWE), the amount of snow on the ground in the equivalent water depth, over North America is currently assembled from the Global Snow Monitoring for Climate Research (GlobSnow, http://www.globsnow.info/) produced at the Finnish Meteorological Institute. The GlobSnow SWE product algorithm combines passive microwave satellite observations from satellite with weather station snow depth measurements on the ground into hemispherical scale SWE estimates (Pulliainen J., 2006).
####Source
GlobSNOW (1979-2014) Daily, Global snow water equivalent. http://www.globsnow.info/


###d. Energy Flux Datasets
####Description
Radiative fluxes are associated with downwelling short/longwave solar radiation and subsequent emission of the heat from Earth’s surface at longwave frequencies. Shortwave refers to the energy integrated over wavelengths from 0.2-4 micrometers from the sun. Longwave  refers to the energy integrated over wavelengths from 4-100 micrometers (also called thermal infrared radiation). Net radiation from the land surface (upwelling energy minus downwelling energy, R up -R down ), is termed “available energy” which corresponds to heat for both latent and sensible fluxes assuming ground heat flux to be negligible.
####Source
GEWEX Surface Radiation Budget (1983-2007)3-hourly  Global down-welling, upwelling radiation, shortwave and longwave Link:http://eosweb.larc.nasa.gov/PRODOCS/srb/table_srb.html

---
III. Data Description
---------------------

###a. Overview
Data from the indicators project data grids are summarized in a standardized measure of seasonal anomaly from a historic mean. Data are stored as tabular values for each indicator type and contain information on location and starting time for each record. 
The original surface hydrologic state climate indicators grid were assembled on a stereographic, equal area grid, the NSIDC Northern Hemisphere EASE-Grid (version 1). (https://nsidc.org/data/ease). In reformatting from a grid to tabular data source the amount of null-valued data positions are reduced by applying a land-mask that in the current normalized data only land-locations are retained. 

###b. Temporal Aggregation/Normalization
Data are summarized for 3-month periods in each record. The temporal segmentation is selected to capture seasons: Winter (Dec-Jan-Feb), Spring (Mar-Apr-May), Summer (Jun-Jul-Aug) and Fall (Sep-Oct-Nov). The starting date of each season is included in each record.
For non-binary data sources (all except Freeze/Thaw) the data is expressed as a count of  zscores (histogram) calculated per-location. Z-scores are calculated from historical observations from that particular season as 

``` 
z_i = (x_i – x_bar) / s_x 
```

Where the z-score, z_i for each observation, x_i is deviation from the historical mean, x_bar, expressed relative to the historical standard deviation, s_x. 

The variability of z-score within a 3-month period are defined by creating a histogram. For each climate indicator, the 5 bins for z-score values are: < -2, -2 to -1, -1 to 1, 1 to 2, >2.

The binary freeze/thaw indicator is a record of the freeze/thaw state of the surface for locations over time. The record is therefore a classification that has 4 binary states: frozen, thawed, transitional or inverse-transitional. The count of observations of each of these states are recorded for each season instead of expressing them relative to historic observations. 


###a. Data File
The data-file, indicators.csv, is a comma-delimited ASCII file containing records for each location and starting time.  Important Notes: For each variables zscore bins are labeled relative to their binning as follows:

* -3:  less than -2 
* -2:  from -2 to -1
* -1:  from -1 to +1
* +1: from+1 to +2
* +2: greater than +2

For periods where data is not available, the value 255 is used. Data should range from 0 to ~90 (+- several days depending on year and months). For areas that do not experience freeze/thaw, histogram counts may remain at zero.

####* The file contains 38 columns of variables defined as:

* [1] index: Index in land-mask (not used)

* [2] start_date: Start of 3-month period (YYYY-MM-DD) (date)

* [3] lat: Latitude in decimal-degrees.

* [4] lon: Longitude in decimal-degrees.

* [5] ft_frozen: Count of days where the ground surface is frozen.

* [6] ft_thawed: Count of days where the ground surface is thawed.

* [7] ft_trans: Count of days where the surface is transitioning between frozen and thawed (thaw during day / frozen during night).

* [8] ft_itrans: Count of days where the surface is transitions between frozen and thawed (thaw during night/ frozen during day).

* [9-13] fw_fw_06_swe -3, fw_fw_06_swe -2, fw_fw_06_swe -1,  fw_fw_06_swe +1,  fw_fw_06_swe +2: Histogram of fractional inundation (originally in percent).

* [14-18] swe_swe_average_-3, swe_swe_average_-2, swe_swe_average_-1, swe_swe_average_+1, swe_swe_average_+2: Histogram of average SWE (originally in inches).

* [19-23] energy_sw_up_-3, energy_sw_up_-2, energy_sw_up_-1, energy_sw_up_+1, energy_sw_up_+2: Histogram of short-wave upwelling (originally in W/m^2).

* [24-28] energy_sw_dn_-3, energy_sw_dn_-2, energy_sw_dn_-1, energy_sw_dn_+1, energy_sw_dn_+2: Histogram of short-wave down-welling (originally in W/m^2).

* [29-33] energy_lw_up_-3, energy_lw_up_-2, energy_lw_up_-1, energy_lw_up_+1, energy_lw_up_+2: Histogram of long-wave upwelling (originally in W/m^2).

* [34-38] energy_lw_dn_-3,energy_lw_dn_-2,energy_lw_dn_-1,energy_lw_dn_+1,energy_lw_dn_+2: Histogram of ling-wave down-welling (originally in W/m^2).


