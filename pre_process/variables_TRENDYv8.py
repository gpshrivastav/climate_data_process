'''
All necessary varibles are defined here, to avoid clutter in the main
code and imported from this file.. 

'''
import regionmask as rg
#import sys
#sys.path.insert(1, '/p/esm/imbalancep/Earth_system_modeling/OSCARv3_drivers_preprocessing/support_files')
#import extra_functions as ef

#work_dir           = '/p/esm/imbalancep/Earth_system_modeling/OSCARv3_parameters_preprocessing/land_TRENDYv8/models'
pre_process_dir    = 'pre_process_w1'
pre_process_dir_w3 = 'pre_process_w3'
dir_raw            = 'raw_data'

t_chunks  = 4
reg_chunk = 4

area_earth = 510.1E6*1E6

##--- get regions from region mask ---------------------##
regions = rg.defined_regions.natural_earth_v5_0_0.countries_50

region_list = regions.numbers   
region_list.append(len(regions.numbers))
region_names = regions.names
region_names.append('Unknown')

region_abbrevs = regions.abbrevs
region_abbrevs.append('UNK')

##------- details of the server and login --------
host = 'trendy.ex.ac.uk'
port = 22
username = 'trendy-v8'
password = 'gcp-2019'
host_dir = 'output'
dest_dir = '../data' ## same as work_dir..

model_list =  ['CLASS-CTEM', 'CLASS-CTEM_Corrected', 'CABLE-POP',   'DLEM', 'JSBACH', 'LPJ-GUESS', 'ORCHIDEE', 'ORCHIDEE-CNP', \
               'SDGVM', 'VISIT', 'LPX-Bern', 'OCN', 'CLM5.0', 'JULES-ES-1.0', 'ISAM'] #   
                # CLM5.0_Corrected, OCN ## JULES-ES-1.0     ## 'ISAM' (lon mismatch see comments)

simu_list  =   ['S0','S1','S2', 'S3', 'S4', 'S5', 'S6', 'S7']   #  now every run has simu list.. when parallel runs not required, open this block and change 
                                                                # the running script accordingly.

var_list   = ['cVeg', 'nbp', 'cLitter',  'cRoot', 'cSoil', 'npp', 'ra', 'rh', 'cProductWhvst', 
              'fCrop', 'fDOC', 'fEst', 'fFire', 'fGrazing', 'fHarvest', 'fLitterSoil', 'fLuc', 'fVegLitter', 
              'cProducts',  'cWood', 'fVegSoil', 'fWoodHarvest', 'cProduct', 'gpp'] #      #### ,,'cProduct'

#-- fix model-specific names of lat, lon, and pft axes...

lon_names = ['longitude', 'x', 'ncl3'] #, 'ncl2'
lon_axis  = {model:'lon' for model in model_list}

lat_names = ['latitude', 'y', 'ncl2'] # , 
lat_axis  = {model:'lat' for model in model_list}

pft_names = ['vegtype', 'PFT', 'ncl1'] #, 'ncl1'
pft_axis  = {model:'pft' for model in model_list}

##--- EXCEPTIONS for bio_time, models which do not follow CF-time convention ----------------
bio_time = {'VISIT'     : {'S0':1860, 'S1':1860, 'S2':1860, 'S3':1860, 'S4':1860, 'S5':1860, 'S6':1860, 'S7':1860},
            'ISAM'      : {'S0':1700, 'S1':1700, 'S2':1700, 'S3':1700, 'S4':1700, 'S5':1700, 'S6':1700, 'S7':1700}
           }
## 'CABLE-POP' : {'S0':1700, 'S1':1700, 'S2':1700, 'S3':1700, 'S4':1700, 'S5':1700},
##--- Model with one biome missing (in TRENDYv7 DLEM and LPJ-GUESS have no bare soil)
bio_model = ['LPX-Bern'] ## see note

##-- Models which use land area ------------------------------------------------------------------
models_land_area = ['LPJ-GUESS','ORCHIDEE', 'LPX-Bern', 'CLASS-CTEM',  'LPJ-GUESS', 'ORCHIDEE',
                    'SDGVM', 'OCN', 'CLM5.0', 'JULES-ES-1.0', 'LPX-Bern', 'ISAM', 'CABLE-POP']  
 
##-- if raw data already downloaded --------------------------------------------------------------
raw_data_exits = False

##== EXCEPTIONS and data structure of TRENDYv8 models ==##
'''
** LPX-Bern has no bare soil in the PFT 
** CLM5.0 has no landCoverFrac file in S0-S2. S3-S7 have landCoverFrac file with 79 PFTs and '0' is baresoil.
** CLM5.0 landCoverFrac in S3 has no lat lon associated to dims ncl2 and ncl3 these are just indices.. so ncl2 and ncl3
   have been replaced by the lat, lon of cVeg variable.
** CLM5.0/S3/fLitterSoil has wierd time, lat, lon axes. (lat, lon) axes have 0.0 for their entire length and time never 
   increased beyond the first value 1700-01-01.

**CABLE-POP: cProduct- lon and lat axis are x, y. Also, the len(lat) = 150 for cProduct and for other variables
it is 180.
**ISAM: landCoverFrac for S0 has (lon, lat) = (718, 360) and variables have (lon, lat) = (718, 360).
        landCoverFrac for S1 has (lon, lat) = (718, 360) and variables have (lon, lat) = (718, 360).
        landCoverFrac for S2 has (lon, lat) = (718, 360) while variables have (lon, lat) = (720, 360). ## problem..      
        landCoverFrac for S3 has (lon, lat) = (720, 360) and variables have (lon, lat) = (720, 360).

**PFT axis: extra entry..
    LPX-Bern 
    JULES-ES-1.0

**models with no land area/oceanFrac file..
    ORCHIDEE-CNP, SDGVM, VISIT, ISAM

**oceanCoverFrac-yes : 
    CABLE-POP (per simulation); I guess can't be used but ask.. 
    CLASS-CTEM (per simulation); can't be used only ocean mask.
    LPJ-GUESS (per simulation); can be used
    ORCHIDEE  (per simulation); can be used 
    LPX-Bern (landmask file per simulation); can be used
    JULES-ES-1.0 (landAreaFrac per simulation), can be used
                         
**oceanCoverFrac-No  : 
    DLEM (landFrac folder); perfect, land area (not mask or fractional mask)
    ISAM (nothing); 
    JSBACH (slm file); land mask, can't be used
    OCN (nothing in S0 - S2; oceanCoverFrac in S3 - S6); 
    ORCHIDEE-CNP (nothing); 
    SDGVEM (nothing);

**Bio_frac time ok (1700-2018) for models..
    LPX-Bern, LPJ-GUESS, SDGVM, CLASS-CTEM, CABLE-POP,ORCHIDEE-CNP, ORCHIDEE, JULES-ES-1.0

**Bio_frac time not ok for models..
    1. VISIT: units [years since.. ]; 
    2. ISAM: array [0,...,319]; 
    3. JSBACH: no time axis    

**var time ok for models..
    JULES-ES-1.0, LPX-Bern, LPJ-GUESS, SDGVM, CLASS-CTEM, CABLE-POP, ORCHIDEE-CNP, ORCHIDEE, JSBACH

**var time not ok for models..
    1. VISIT: units[months since];  
    2. ISAM: array [0..319]

**most irritating models : ISAM, CLM5.0
 
'''