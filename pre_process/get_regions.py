##------------------------------------------------------##
import geopandas as gpd
import regionmask as rg
import warnings
warnings.filterwarnings('ignore')

def get_regions():
    """
    This function creates regions of interest. The regions of interest consists of countries defined in natural earth at 
    the medium scale resolution (1:50m). France and Netherlands are separated from main land and their islands across the 
    globe.
    * Parameters
    ------------
        Currently, no parameters needed.
    ------------
    """
    countries = gpd.read_file('shape_files/ne_50m_admin_0_countries.zip')
    regions_map_units= gpd.read_file('shape_files/ne_50m_admin_0_map_units.zip')   

    ll_fr_nl_terr_mis = []
# open missing countrie sfile and read the content in a list
    with open("data/countries.txt",  'r') as fp:
        for line in fp:
            x = line[:-1]
            ll_fr_nl_terr_mis.append(x)

    df_cou = gpd.GeoDataFrame()
    for cou in ll_fr_nl_terr_mis:
        if cou == 'RÃ©union': cou = 'Réunion'
        df_cou = df_cou.append(regions_map_units[regions_map_units.NAME_EN == cou]) 

    countries_w_fr      = countries[countries.NAME_EN       !='France']
    countries_w_fr_nl   = countries_w_fr[countries.NAME_EN  !='Netherlands']

    France      = regions_map_units[regions_map_units.NAME_EN == 'France']
    Netherlands = regions_map_units[regions_map_units.NAME_EN == 'Netherlands']

    reg_w_fr_nl_terr = countries_w_fr_nl.append([df_cou, France, Netherlands])
    ## New addition ... removing special characters from region names and sorting regions alphabetically.
    dict_spc_regs = {
                 'Curaçao' : 'Curacao',
                 'Réunion' : 'Reunion',
                 'Saint Barthélemy' : 'Saint Barthelemy',
                 'São Tomé and Príncipe' : 'Sao Tome and Principe',
                 'Åland' : 'Aland'
                }

    for spc_name in dict_spc_regs.keys():
        reg_w_fr_nl_terr['NAME_EN'][reg_w_fr_nl_terr['NAME_EN'] == spc_name] = dict_spc_regs[spc_name]

    reg_w_fr_nl_terr = reg_w_fr_nl_terr.sort_values('NAME_EN', ignore_index = True)

    # dictionary of countries with no iso code
    dico_iso_codes = {
                    'Ashmore and Cartier Islands':'XAU', 
                    'Somaliland': 'XSO', 
                    'Norway': 'NOR', 
                    'Kosovo': 'XXK', 
                    'Turkish Republic of Northern Cyprus':'XCY', 
                    'Australian Indian Ocean Territories': 'XXC',                   
                    'Siachen Glacier': 'XXG'
                }

    for reg in dico_iso_codes.keys():
        id = reg_w_fr_nl_terr.index[reg_w_fr_nl_terr['NAME_EN'] == reg].values[0]
        reg_w_fr_nl_terr.at[id,'ISO_A3'] = dico_iso_codes[reg]    
    ## new addition ends

    rgmask_reg_w_fr_nl_terr = rg.Regions(reg_w_fr_nl_terr.geometry, names=reg_w_fr_nl_terr.NAME_EN, 
                                          abbrevs=reg_w_fr_nl_terr.ISO_A3)
    return rgmask_reg_w_fr_nl_terr
##============== region function ends ===============##