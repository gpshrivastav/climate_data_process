import xarray as xr
from pre_process import get_mask
##======================================================##
""" 
Function to fix xarray dataset geo coding..  
"""
##------------------------------------------------------##
def fix_geo_code(data):
    """
    * Description:
      ------------
      Sometimes TRENDY models have variables where latitude of the data is reversed.
      In those cases, the map is inverted in the sense that northern hemisphere have latitude
      ranging from [-90, 0].

      To avoid this issue, we use regionmask and match the latitude range of a given country, say India.
      If the latitude range of India is reversed in data and mask, then the latitude of the input data
      is reversed.

      The function calls get_mask function from pre_process.

    * Parameters:
      -----------
      data:            xarray dataset; 
                       input dataset for which geocoding has to be fixed.
      var_for_fix:     xarray dataset; 
                       input data variable with which the resolution has to be matched.
      axis:            str; 
                       "lat", or "lon". if None, both axis will be considered. 
      -----------

    * Return:
      -----------
      variable with lat, lon or both consistent with the lat, lon of the input data.
      ----------- 
    """

    mask = get_mask.get_grid_mask(data)

    ind = mask.where(mask.sel(reg_mask = mask.reg_mask_name == 'India') == True, drop = True)

    ## compare coordinates of India from the data* mask and only from mask... if these are reversed then
    ## reverse the latitude of the data.. 


    data['lat'] =  xr.concat([var_for_fix['lat'].sel(lat =lat_val, method='nearest') 
                                         for lat_val in var_to_be_fixed['lat']], dim = 'lat')
    if var_to_be_fixed.name != None:
        print('fixed lat.. for ', var_to_be_fixed.name)
    else:
        print('fixed lat.. for unnamed variable')
    var_to_be_fixed['lon']  =  xr.concat([var_for_fix['lon'].sel(lon=lon_val,method='nearest') 
                                          for lon_val in var_to_be_fixed['lon']],dim = 'lon') 
    if var_to_be_fixed.name != None:
        print('fixed lon.. for ', var_to_be_fixed.name)
    else:    
        print('fixed lon.. for unnamed variable')

    #elif axis == 'lat':
    #    var_to_be_fixed['lat'] =  xr.concat([var_for_fix['lat'].sel(lat = lat_val, method='nearest') 
    #                                         for lat_val in var_to_be_fixed['lat']], dim = 'lat')
    #    if var_to_be_fixed.name != None:
    #         print('fixed lat.. for ', var_to_be_fixed.name)
    #    else:
    #         print('fixed lat.. for unnamed variable')
#
#
    #elif axis == 'lon':
    #    var_to_be_fixed['lon']  =  xr.concat([var_for_fix['lon'].sel(lon=lon_val,method='nearest') 
    #                                          for lon_val in var_to_be_fixed['lon']],dim = 'lon')
    #    if var_to_be_fixed.name != None:
    #        print('fixed lon.. for ', var_to_be_fixed.name)
    #    else:    
    #        print('fixed lon.. for unnamed variable')
#
    #else:
    #    raise Warning('provide an axis for matching/or wrong axis name')

    return data
##=========== axis mismatch function ends ==============##