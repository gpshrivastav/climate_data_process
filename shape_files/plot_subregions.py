import geopandas as gpd
import matplotlib.pyplot as plt
import regionmask as rg
import pandas as pd
import xarray as xr
import numpy as np


countries_mapunits = gpd.read_file('ne_50m_admin_0_map_units.zip')
countries = gpd.read_file('../shape_files/ne_50m_admin_0_countries.zip')

diff = ['Antigua', 'Autonomous Region of Bougainville', 'Azores','Barbuda','Brussels Capital Region','Caribbean Netherlands',
        'Christmas Island','Cocos','England','Federation of Bosnia and Herzegovina','Flemish Brabant','French Guiana',
        'Gaza Strip','Guadeloupe','Jan Mayen','Madeira','Martinique','Mayotte','Northern Ireland','Republika Srpska',
        'Réunion','Scotland','Svalbard','Tokelau','Vojvodina','Wales','Walloon Brabant','West Bank','Zanzibar']

df_cou = gpd.GeoDataFrame()
for cou in diff:
    df_cou = df_cou.append(countries_mapunits[countries_mapunits.NAME_EN == cou])

ll_sub = list(df_cou.SOVEREIGNT.values)
ll_sub_uniq = list(set(ll_sub))
print(ll_sub_uniq)
for cou in ll_sub_uniq:
    print('region in level 2:', cou)
    print('corresponding country in level 1:', df_cou[df_cou.SOVEREIGNT == cou])
    print(' ')
    fig, ax = plt.subplots (figsize = (15,15))
    df_cou[df_cou.SOVEREIGNT == cou].plot(column = 'NAME_EN',cmap= 'Accent',ax = ax, legend=True, legend_kwds={'loc': 'upper left'})

    if cou == 'Republic of Serbia': 
        cou_n = 'Serbia'
    elif cou == 'United Republic of Tanzania':
        cou_n = 'Tanzania'
    else:
        cou_n = cou

    countries[countries.NAME_EN == cou_n].boundary.plot(ax = ax, color='black') 
    plt.title(cou_n)
    name = cou.replace(" ","")
    plt.savefig('plots/' + name + '.png', dpi=200)
    print('---------------------------------')
##
## color maps in geopandas
'''
'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 
'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 
'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 
'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 
'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 
'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r',
'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 
'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 
'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 
'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 
'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 
'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 
'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 
'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 
'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 
'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r'
'''

## extra codes
'''
countries = gpd.read_file('../shape_files/ne_50m_admin_0_countries.zip')
countries_new = countries[['geometry', 'NAME_EN', 'ISO_A3']]

countries_new = countries_new.rename(columns={'ISO_A3':'ABBREVS'})
new_region = rg.Regions(countries_new.geometry, names=countries_new.NAME_EN, abbrevs=countries_new.ABBREVS)
df = pd.DataFrame(new_region)
df_countries = pd.read_csv('regions_countries.csv')
ll = df_countries['0'][:].tolist()
ll_new = [zou[:zou.find('(')].replace(" ", "") for zou in ll]

df_cou = gpd.GeoDataFrame()

for cou in diff:
    df_cou = df_cou.append(countries_mapunits[countries_mapunits.NAME_EN == cou])

countries_extra = df_cou[['geometry', 'NAME_EN', 'ISO_A3']]
countries_extra = countries_extra.rename(columns={'ISO_A3':'ABBREVS'})


fig, ax = plt.subplots (figsize = (15,15))
countries_extra.plot(column = 'NAME_EN',  ax = ax, legend=True, legend_kwds={'loc': 'upper left'})
countries.boundary.plot(ax=ax)

ll_sub = list(df_cou.SOVEREIGNT.values)
'''