##======================================================##
'''Downloading CMIP data using ESMValtool...'''
##======================================================##
def get_cmip_data(var, dataset, project, mip, experiment, ensemble, realms, grid, start_year, end_year):    
    '''
    Funtion for downloading CMIP data using esmvaltool. This function makes changes in esmvaltool recipe and 
    calls esmvaltool excutable externally to run the recipe. The run is not successful as esmvaltool cannot be 
    installed inside a python environment (in this case envOSCAR). However, it does download the data. 
    *Parameters:
        var: variables to be downloaded
        dataset: cmip model
        project: cmip project (CMIP6 in the present case)
        mip: no idea
        expriment: experiment for the run 
        ensemble: no idea
        grid: gridding of the data
        start_year: year since when processing is needed
        end_year: end of the processing

    *Location of the output files and data storage, etc. can be set in ~/.esmvaltool/config.yml file. 
    '''
    recipe_file = '/p/esm/imbalancep/Earth_system_modeling/OSCARv3_drivers_preprocessing/climate-CMIP6/first-recipe.yml'
    with open(recipe_file, 'r') as f:
        lines = f.readlines()
    with open(recipe_file, 'w') as f:
        print('changing dataset details in recipe file..', f)
        for line in lines:         
            if 'dataset:' in line:  
                line = line.strip()
                line = (' '+ ' ' + '- {dataset: '+dataset +', '
                                    + 'project: '+ project+', '
                                    + 'mip: '+ mip+', '
                                    + 'exp: '+ experiment+', '
                                    + 'ensemble: '+ensemble+', '
                                    + 'grid: '+ grid+', '
                                    + 'start_year: '+str(start_year)+', '
                                    + 'end_year: '+str(end_year)+'}' +                     
                        '\n')            
                #f.write(re.sub(r'dataset:', 'dataset:'+dd, line))
                print(dataset)               
                f.write(line)
                print(line)
            else:
                f.write(line)

    with open(recipe_file, 'r') as f:
        lines = f.readlines()
    with open(recipe_file, 'w') as f:
        print('changing variable name in the recipe file..')
        for line in lines: 
            if 'short_name:' in line:
                line = line.strip()
                line = ('        '+ 'short_name: '+ var + '\n')
                print(var)
                f.write(line)
                print(line)
            else:
                f.write(line)

    with open(recipe_file, 'r') as f:
        lines = f.readlines()
    with open(recipe_file, 'w') as f:
        print('changing realm in the recipe file..')
        for line in lines: 
            if '##realms needed' in line:
                line = line.strip()
                line = ('      '+ '- '+ realms + '  ##realms needed'+ '\n')
                print(realms)
                f.write(line)                
                print(line)
            else:
                f.write(line)
            
    
    sp.call('esmvaltool run first-recipe.yml > /p/esm/imbalancep/Earth_system_modeling/OSCARv3_drivers_preprocessing/support_files/hh.txt', shell=True) 
    esmval_log_file = '/p/esm/imbalancep/Earth_system_modeling/OSCARv3_drivers_preprocessing/support_files/hh.txt'
    found = False
    with open(esmval_log_file, 'r') as f1: 
       lines = f1.readlines()
       for line in lines:        
         if 'Successfully downloaded' in line: 
            found = True
            break

    if found:
       return print('data download succesfully..')
        #path = '/p/esm/imbalancep/Earth_system_modeling/OSCARv3_drivers_preprocessing/climate-CMIP6/data_raw/' 
        #folder = set()
        #for root, dirs, files in os.walk(path, topdown=False):    
        #    for name in files:
        #        if dataset in name and experiment in name and var in name and '.nc' in name:                       
        #            folder = root
        #file = folder + '/*.nc'
        #print(folder)
        #ds = xr.open_mfdataset(file)
        #ds = ds.groupby('time.year').mean('time')
        #return ds
    else:
        return print('data download failed..')

