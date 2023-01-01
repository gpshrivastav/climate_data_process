import xarray as xr
##======================================================##
''' Function to fix lat, lon axis mismatch..           '''
##------------------------------------------------------##
def fix_axis(var_to_be_fixed, var_for_fix, axis = None):
    """
    This function fixes the grid resolution (lat, lon) of variable of interest according to the
    input data.
    * Parameters:
      -----------
      var_to_be_fixed: xarray dataset; 
                       variable for which resolution to be fixed.
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
    if axis == None:

        var_to_be_fixed['lat'] =  xr.concat([var_for_fix['lat'].sel(lat =lat_val, method='nearest') 
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

    elif axis == 'lat':
        var_to_be_fixed['lat'] =  xr.concat([var_for_fix['lat'].sel(lat = lat_val, method='nearest') 
                                             for lat_val in var_to_be_fixed['lat']], dim = 'lat')
        if var_to_be_fixed.name != None:
             print('fixed lat.. for ', var_to_be_fixed.name)
        else:
             print('fixed lat.. for unnamed variable')


    elif axis == 'lon':
        var_to_be_fixed['lon']  =  xr.concat([var_for_fix['lon'].sel(lon=lon_val,method='nearest') 
                                              for lon_val in var_to_be_fixed['lon']],dim = 'lon')
        if var_to_be_fixed.name != None:
            print('fixed lon.. for ', var_to_be_fixed.name)
        else:    
            print('fixed lon.. for unnamed variable')

    else:
        raise Warning('provide an axis for matching/or wrong axis name')

    return var_to_be_fixed
##=========== axis mismatch function ends ==============##