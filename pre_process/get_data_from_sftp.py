"""
This program downloads data from TRENDY-SFTP server.
"""

##======================================================##
'''              SFTP connection                       '''
##------------------------------------------------------##
import pysftp
import os
from pre_process import variables_TRENDYv8 as vars

def access_server(model, simu, var):
    """
    Inputs
    ----------------
        model: Name of the TRENDY model
        simu : Simulation 
        var  : TRENDY variable for which data is needed

    Additional inputs:
    -----------------
        SFTP server details: coming from vars file (variables for TRENDYv8)
        host : hostname of the server
        port : port of the server
        username: username for login to the server
        password: password for login to the server 

    Return:
    ----------------
        Downloads data at the location defined in vars file (dest_folder)
    """
    
    ##---- connect------
    
    try: 
        connect = pysftp.Connection(host = vars.host, port = vars.port, username = vars.username, password = vars.password)
        print('connection established successfully')
        connected = True

    except:
        print('connection failed')
        connected = False

    if connected: ## proceed only when successful connection establishes--
        print('current working dir: ', connect.pwd)

        ##-- create destination directory..
        path_dest = vars.dest_dir #+ '/' + model + '/' + 'raw_data/'
        if not os.path.exists(path_dest):os.makedirs(path_dest)

        os.chdir(path_dest)    
        if simu is not None:
            if model == 'CLM5.0': model = model + '_Corrected'

            if model == 'CLASS-CTEM_Corrected':
                             
                if simu == 'S0':
                   simu_folder = 'S0-forS4toS6-ResubmitSept2020'
                else:
                   simu_folder = simu + '-ResubmitSept2020'

                host_path  = os.path.join(vars.host_dir , 'CLASS-CTEM', simu_folder)
                folder     = simu_folder
                check_host = os.path.join(vars.host_dir, 'CLASS-CTEM')
               
            else:
                host_path  = os.path.join(vars.host_dir, model, simu)
                folder     = simu
                check_host = os.path.join(vars.host_dir, model)
            
        else:
            if model == 'CLM5.0': model = model + '_Corrected'
            host_path  = os.path.join(vars.host_dir, model) 
            check_host = vars.host_dir
            folder     = model
        
        if folder in connect.listdir(check_host):            
            with connect.cd(host_path):
                connect.listdir()
               
                if simu is not None:  
                      
                    if model == 'CLM5.0_Corrected': model = 'CLM5.0'

                    if model == 'CLASS-CTEM_Corrected':                         
                        file = 'CLASS-CTEM_' + simu + '_' + var + '.nc'  
                    elif model == 'JULES-ES-1.0':
                        file = 'JULES-ES.1p0.vn5.4.50.CRUJRA2.TRENDYv8.365.' + simu + '_Annual_' + var + '.nc'
                    else:         
                        file = model + '_' + simu + '_' + var + '.nc'
                   
                else:
                    file = model + '_' + var + '.nc'   

                if model == 'DLEM' and var == 'landArea': ## special for DLEM
                    file = model + '_' + var + '.nc'

                if model == 'JULES-ES-1.0' and var == 'landAreaFrac': ## special for JULES
                    file = 'JULES-ES.1p0.vn5.4.50.CRUJRA2.TRENDYv8.365.' + var + '.nc'

                if model in ['LPX-Bern', 'CABLE-POP']  and var == 'landmask': ## special for LPX-Bern
                    file = model + '_' + var + '.nc'
                
                

                if file in connect.listdir():
                    
                    if model == 'JULES-ES-1.0':
                        dest_file = model + '_' + simu + '_' + var + '.nc'
                        connect.get(file, dest_file)

                    if model == 'CLASS-CTEM_Corrected':
                        
                        dest_file = model + '_' + simu + '_' + var + '.nc'
                        connect.get(file, dest_file)

                    else:
                        connect.get(file)
                    print('data downloaded successfully')
        
                elif model + '_' + simu + '_' + var + '.nc.gz' in connect.listdir():
                    connect.get(model + '_' + simu + '_' + var + '.nc.gz')
                    print('data downloaded successfully')
        
                else:
                    print('** file ' + model + '_' + simu + '_' + var + '.nc/.nc.gz' +' not found **')

            connect.close()
            return  print('=== downloading ' + var + ' fertig!!-- connection closed ===')
        
        else:           
            return print('===== ' + simu + ' folder does not exit.. time to move on')
    
    else:
        return print('=== downloading interrupted' + var + ' not fertig!!-- connection closed ===')

##================ file download ends ==================##