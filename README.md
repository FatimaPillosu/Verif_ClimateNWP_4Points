[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

# ecPoint-Climate

### Background
To establish climatologies that facilitate the contextualization of extreme, high-impact weather events in relation to historical occurrences or to comprehend the influence of climate change on their intensity and frequency, an extensive collection of observations extending as far back as possible is essential. Yet, these observations exhibit inaccuracies and uneven distributions in space and time. These attributes may lead to a distorted representation of past weather and climate, particularly for variables like rainfall, which can exhibit substantial variations in space and time. Reanalyses and reforecasts fill the gaps in the observational records. Existing literature has demonstrated that both reanalysis and reforecast datasets offer a more accurate representation of past weather and climate, owing to their global completeness and temporal consistency. Nonetheless, reanalyses and reforecasts may not adequately depict localized and/or rare events as effectively as observational climatologies might do (provided sufficient observations are available) due to the coarse spatial resolutions of both modelled datasets. This misrepresentation is particularly pertinent for discontinuous variables, such as precipitation. This study will examine the representation of point-rainfall climatologies by four distinct global modelled datasets: ERA5_EDA (reanalysis, 62km), ERA5 (reanalysis, 31km), ECMWF reforecasts (reforecasts, 18 km), and ERA5_ePoint (reanalysis, point-scale over an 18km grid).

### Description of the repository's content
-> README.md
-> License.md
-> .gitignore

-> **Scripts/**
|-> **Raw/**
||-> README.md
||-> Retrieve_ERA5_ecPoint.sh
||-> Retrieve_ERA5_EDA_LongRange.sh
||-> Retrieve_ERA5_EDA_ShortRange.sh
||-> Retrieve_ERA5_LongRange.sh
||-> Retrieve_ERA5_ShortRange.sh
||-> Retrieve_HRES_46r1.sh
||-> Retrieve_Reforecasts_46r1.sh
||-> Retrieve_OBS_CPC.sh
||-> Retrieve_OBS_STVL.sh
||-> Retrieve_LSM.sh
|-> **Processed/**

-> **Data/**
|-> **Raw/**
||-> _FC/_ 
|||-> ERA5_ecPoint
|||-> ERA5_EDA_LongRange
|||-> ERA5_EDA_ShortRange
|||-> ERA5_LongRange
|||-> ERA5_ShortRange
|||-> HRES_46r1
|||-> Reforecasts_46r1
||-> _OBS/_
|||-> CPC_24h/
|||-> STVL_24h/
||-> _LSM/_
|||-> lms_ERA5_EDA.grib
|||-> lms_ERA5.grib
|||-> lms_HRES.grib
|||-> lms_Reforecasts.grib
|-> **Compute**
|-> **Plot**

-> **Manuscript/**
|-> Manuscript.docx
|-> Figures/


### Description on how to run the code
The description of how to run the code can be found in the README files in:
-> Scripts/Raw/README.md
-> Scripts/Processed/README.md


### Licensing
The code and the paper are freely available under the CC BY-NC-SA 4.0 license (Creative Commons, Attribution-NonCommercial-ShareAlike).  
The data (i.e. rainfall forecasts and observations) is available upon request to the main author of the repository and prior authorization from ECMWF management.

#### Main author
Fatima Pillosu
PhD student at University of Reading & Visiting scientist at ECMWF
fatima.pillosu@ecmwf.int