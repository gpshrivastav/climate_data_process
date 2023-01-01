import numpy as np
from pre_process import variables_TRENDYv8 as vars
from pre_process import extra_functions as ef
#import fix_axis
import geopandas as gpd
import regionmask as rg

##======================================================##
'''     Function to get land mask from regionmask      '''
##------------------------------------------------------##
def get_grid_mask( VAR, regions = vars.regions, res=0.1):
    #res = 0.1
    
    data_points_lat =  int(abs((np.ceil(VAR.lat.diff('lat').mean().values/res)//2)*2 +1))                
    mid_point_lat = data_points_lat//2
    ratio_lat     = mid_point_lat/data_points_lat

    data_points_lon = int(abs((np.ceil(VAR.lon.diff('lon').mean().values/res)//2)*2 +1))
    mid_point_lon = data_points_lon//2  
    ratio_lon     = mid_point_lon/data_points_lon
                
    lat2 = np.linspace(VAR.lat[0]-ratio_lat*VAR.lat.diff('lat').mean(), VAR.lat[-1]
                                   +ratio_lat*VAR.lat.diff('lat').mean(), data_points_lat*len(VAR.lat))
    lon2 = np.linspace(VAR.lon[0]- ratio_lon*VAR.lon.diff('lon').mean(), VAR.lon[-1]
                                   +ratio_lon*VAR.lon.diff('lon').mean(), data_points_lon*len(VAR.lon))

    mask = regions.mask_3D(lon2,lat2).rename('masked_regions')
    masked_regions = mask.coarsen(lat=data_points_lat).mean('lat').coarsen(lon=data_points_lon).mean('lon')

    #-- fix lat, lon according to the variable...
    masked_regions = ef.fix_axis(masked_regions, VAR)

    masked_regions['region'] = 1+ masked_regions['region']    
    masked_regions = masked_regions.rename({'region' : 'reg_mask'     })
    masked_regions = masked_regions.rename({'names'  : 'reg_mask_name'})
    masked_regions = masked_regions.rename({'abbrevs': 'reg_mask_code'})

    masked_regions = masked_regions/ masked_regions.sum('reg_mask', min_count=1)
    
    return masked_regions          ## returning unnormalized masked regions.. adv. is that it provides fraction 
                                   ## of land in coastal regions which is used for defining land area.
##============== land mask function ends ===============## 
def get_land_mask( VAR, regions = vars.regions, res=0.1):
    """
    Description:
    ------------
    This function calculates land mask. Note that the actual land area calculated from here may be different
    from that used in vegetation models. 

    Usage:
    ------
    get_mask.get_land_mask(ds, regions, res)

    Parameters:
    -----------
    VAR     =  Xarray Dataset or DataArray
    regions = World regions, if not provided, will be calculated from regionmask.defined_countries.natural_earth.countries_50m
              Courtries obtained from Natural Earth at medium scale resolution.
    res     = resolution at which downscaling has to done, default value is 0.1. For details, see funtion "get_land_mask" 

    Return:
    -------
    Land mask excluding ice and water bodies
    """
    
    data_points_lat =  int(abs((np.ceil(VAR.lat.diff('lat').mean().values/res)//2)*2 +1))                
    mid_point_lat = data_points_lat//2
    ratio_lat     = mid_point_lat/data_points_lat

    data_points_lon = int(abs((np.ceil(VAR.lon.diff('lon').mean().values/res)//2)*2 +1))
    mid_point_lon = data_points_lon//2  
    ratio_lon     = mid_point_lon/data_points_lon
                
    lat2 = np.linspace(VAR.lat[0]-ratio_lat*VAR.lat.diff('lat').mean(), VAR.lat[-1]
                                   +ratio_lat*VAR.lat.diff('lat').mean(), data_points_lat*len(VAR.lat))
    lon2 = np.linspace(VAR.lon[0]- ratio_lon*VAR.lon.diff('lon').mean(), VAR.lon[-1]
                                   +ratio_lon*VAR.lon.diff('lon').mean(), data_points_lon*len(VAR.lon))

    mask = regions.mask_3D(lon2,lat2).rename('masked_regions')
    masked_regions = mask.coarsen(lat=data_points_lat).mean('lat').coarsen(lon=data_points_lon).mean('lon')

    #-- fix lat, lon according to the variable...
    masked_regions = ef.fix_axis(masked_regions, VAR)

    masked_regions['region'] = 1+ masked_regions['region']    
    masked_regions = masked_regions.rename({'region' : 'reg_mask'     })
    masked_regions = masked_regions.rename({'names'  : 'reg_mask_name'})
    masked_regions = masked_regions.rename({'abbrevs': 'reg_mask_code'})
    
    return masked_regions          ## returning unnormalized masked regions.. adv. is that it provides fraction 
                                   ## of land in coastal regions which is used for defining land area.
##============== land mask function ends ===============##    

##======================================================##
'''     Function to get land mask from regionmask      '''
##------------------------------------------------------##
def get_full_land_mask( VAR, regions=vars.regions, res = 0.1):
    """
    Description:
    ------------
    This function calculates land area including rivers, lakes, artificial reserviors, and 
    glaciated regions. Note that the actual land area calculated from here may be different
    from that used in vegetation models. 

    Usage:
    ------
    get_mask.get_full_land_mask(ds, regions, res)

    Parameters:
    -----------
    VAR     =  Xarray Dataset or DataArray
    regions = World regions, if not provided, will be calculated from regionmask.defined_countries.natural_earth.countries_50m
              Courtries obtained from Natural Earth at medium scale resolution.
    res     = resolution at which downscaling has to done, default value is 0.1. For details, see funtion "get_land_mask" 

    Return:
    -------
    Full land mask excluding ice and water bodies
    """
    #res = 0.1
    print(len(regions), res)
    data_points_lat =  int(abs((np.ceil(VAR.lat.diff('lat').mean().values/res)//2)*2 +1))                
    mid_point_lat = data_points_lat//2
    ratio_lat     = mid_point_lat/data_points_lat

    data_points_lon = int(abs((np.ceil(VAR.lon.diff('lon').mean().values/res)//2)*2 +1))
    mid_point_lon = data_points_lon//2  
    ratio_lon     = mid_point_lon/data_points_lon
                
    lat2 = np.linspace(VAR.lat[0]-ratio_lat*VAR.lat.diff('lat').mean(), VAR.lat[-1]
                                   +ratio_lat*VAR.lat.diff('lat').mean(), data_points_lat*len(VAR.lat))
    lon2 = np.linspace(VAR.lon[0]- ratio_lon*VAR.lon.diff('lon').mean(), VAR.lon[-1]
                                   +ratio_lon*VAR.lon.diff('lon').mean(), data_points_lon*len(VAR.lon))

    '''
    open this section when land area with water bodies is needed..
    '''
    land = gpd.read_file("shape_files/ne_50m_land.zip")        

    mask_land = rg.mask_geopandas(land, lon2, lat2)
    mask_land = mask_land.where(mask_land.isnull(), 1).rename('land')
    mask_land = mask_land.where(mask_land.notnull(), 0)

    river = gpd.read_file('shape_files/ne_50m_rivers_lake_centerlines_scale_rank.zip')
    
    mask_rivers = rg.mask_geopandas(river, lon2, lat2)
    mask_rivers = mask_rivers.where(mask_rivers.isnull(), 0).rename('river')
    mask_rivers = mask_rivers.where(mask_rivers.notnull(), 1)

    lakes = gpd.read_file('shape_files/ne_50m_lakes.zip')
    
    mask_lakes = rg.mask_geopandas(lakes, lon2, lat2)
    mask_lakes = mask_lakes.where(mask_lakes.isnull(),0)
    mask_lakes = mask_lakes.where(mask_lakes.notnull(),1).rename('lake')

    ice = gpd.read_file('shape_files/ne_50m_glaciated_areas.zip')
   
    mask_ice = rg.mask_geopandas(ice, lon2, lat2)
    mask_ice = mask_ice.where(mask_ice.isnull(), 0)
    mask_ice = mask_ice.where(mask_ice.notnull(), 1).rename('ice')

    mask = regions.mask_3D(lon2,lat2).rename('masked_regions')
    masked_regions = mask_land * mask_ice* mask_lakes * mask_rivers * mask   
    masked_regions = masked_regions.coarsen(lat=data_points_lat).mean('lat').coarsen(lon=data_points_lon).mean('lon')

    #-- fix lat, lon according to the variable...
    masked_regions = ef.fix_axis(masked_regions, VAR)

    masked_regions['region'] = 1+ masked_regions['region']    
    masked_regions = masked_regions.rename({'region' : 'reg_mask'     })
    masked_regions = masked_regions.rename({'names'  : 'reg_mask_name'})
    masked_regions = masked_regions.rename({'abbrevs': 'reg_mask_code'})
    
    return masked_regions          ## returning unnormalized masked regions.. adv. is that it provides fraction 
                                   ## of land in coastal regions which is used for defining land area.
##============== land mask function ends ===============## 