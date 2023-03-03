#Import necessary packages
#----------------------------------------------------------------------------------------------------
#The packages below need to be installed separately to python (https://geopandas.org/en/stable/getting_started/install.html):
import geopandas as gpd
#The packages below are dependencies of geopandas so do not need to be installed separately
import pandas as pd
from pyproj import Proj, transform
from shapely.geometry import Point
#The packages below are inbuilt python packages:
import json
import os
import datetime as dt
import numpy as np

#----------------------------------------------------------------------------------------------------
#prints a given log message and appends the log file to contain it
#----------------------------------------------------------------------------------------------------
def log(message):
    """Appending all activities/errors as well as the time at which they took place
    to a log file.

    Args:
        message (str): Statement that is appended to the log file briefly describing the activity/error.

    """
    print(message)
    out_file = open('data_prep_log.txt', 'a')
    out_file.write(f'{dt.datetime.now()} - {message}\n')
    out_file.close()

#----------------------------------------------------------------------------------------------------
#creates the output directory if it does not already exist
#----------------------------------------------------------------------------------------------------
def form_outdir(out_dir):
    """The output of the script will need to be added to a directory called "out_dir". 
    This function checks that the directory exists, and if it does not it will be created.

    Args:
        out_dir (str): Name of the output directory folder.

    """
    log(f'checking for {out_dir} directory...')
    try:
        os.mkdir(out_dir)
        log(f'{out_dir} directory constructed')
    except FileExistsError:
        log(f'{out_dir} directory found')

#----------------------------------------------------------------------------------------------------
#loads the input files, returns a polygon and two geodataframes if successful
#returns 3 'NULL' and an empty geodataframe if unsuccessful
#----------------------------------------------------------------------------------------------------
def load_inputs(in_dir, master_geojson, border_geojson, borough_geojson, borough_names_csv):
    """The input files are loaded (). If successful then a polygon and two geodataframs are returned.
    If loading is unsuccessfull, then 3 'NULL' statements and an empty geodataframe are returned.

    Args:
        in_dir (str): {Value in config file} Name of the input directory folder
        master_geojson (str): {Value in config file} Refers to the value of "master_geojson"
        border_geojson (str): {Value in config file} Refers to the value of "border_geojson" 
        borough_geojson (str): {Value in config file} Refers to the value of "borough_geojson" 
        borough_names_csv {Value in config file} Refers to the csv file which is the value of "borough_names_csv"

    Returns:
        if successful loading - >
        cycle_racks (geodataframe): cycle_racks geodataframe
        border (geodataframe): border geodataframe
        borough_geometry (geodataframe): borough_geometry geodataframe
        borough_names (dataframe): Dataframe called borough_names

        if unsuccessful loading - >
        fail_value

    """
    log(f'loading "{in_dir}/{master_geojson}"...')
    fail_value = 'NULL',pd.DataFrame(),'NULL','NULL'
    try:
        cycle_racks = gpd.read_file(f'{in_dir}/{master_geojson}')
        log(f'"{in_dir}/{master_geojson}" loaded - {len(cycle_racks)} rows in dataset')
        log(f'loading "{in_dir}/{border_geojson}"...')
        try:
            border = gpd.read_file(f'{in_dir}/{border_geojson}').loc[0,'geometry']
            log(f'"{in_dir}/{border_geojson}" loaded')
            log(f'loading "{in_dir}/{borough_geojson}"...')
            try:
                borough_geometry = gpd.read_file(f'{in_dir}/{borough_geojson}')
                log(f'"{in_dir}/{borough_geojson}" loaded')
                log(f'loading "{in_dir}/{borough_names_csv}"...')
                try:
                    borough_names = pd.read_csv(f'{in_dir}/{borough_names_csv}')
                    log(f'"{in_dir}/{borough_names_csv}" loaded')
                    return border, borough_names, borough_geometry, cycle_racks
                except:
                    log(f'ERROR - "{in_dir}/{borough_names_csv}" could not be loaded')
                    return fail_value
            except:
                log(f'ERROR - "{in_dir}/{borough_geojson}" could not be loaded')
                return fail_value
        except:
            log(f'ERROR - "{in_dir}/{border_geojson}" could not be loaded')
            return fail_value
    except:
        log(f'ERROR - "{in_dir}/{master_geojson}" could not be loaded')
        return fail_value

#----------------------------------------------------------------------------------------------------
#if a bypass does not exist, changes the crs of all bike rack points and generates a new bypass
#----------------------------------------------------------------------------------------------------
def convert_crs(cycle_racks, in_crs, out_crs, in_dir, out_dir, bypass_fname, bypass_driver):
    """If the bypass file is not present, the 'cycle_racks' geodataframe is checked to ensure that it
    meets the standard UK CRS practises.

    Args:
        cycle_racks (geodataframe): Geodataframe of the cycle racks to be modified
        in_crs (str): {Value in config file} Value representing the "in_crs" parameter in the config
        out_crs (str): {Value in config file} Value representing the "out_crs" parameter in the config
        in_dir (str): {Value in config file} Name of the input directory folder
        out_dir (str): {Value in config file} Name of the output directory folder
        bypass_fname (str): {Value in config file} Value representing the "bypass_fname" parameter in the config 
        bypass_driver (str): {Value in config file} The driver to be used

    Returns:
        cycle_racks (geodataframe): Post-conversion cycle_racks geodataframe if bypass file not present

    """

    if os.path.exists(f'{in_dir}/{bypass_fname}'):
        log(f'bypass file found in "{in_dir}", bypassing crs conversion...')
        processed_points = gpd.read_file(f'{in_dir}/{bypass_fname}')
        point_list = processed_points['geometry'].tolist()
    else:
        in_proj = Proj(init=in_crs)
        out_proj = Proj(init=out_crs)
        log(f'converting crs of points from master geojson... this process takes a lot of time and can be bypassed! See README.md')
        point_list = []
        for i,row in cycle_racks.iterrows():
            cycle_point = row['geometry']
            point_list.append(transform(in_proj, out_proj, cycle_point.x, cycle_point.y))
        point_list = [Point(coord[0],coord[1]) for coord in point_list]
        processed_points = gpd.GeoDataFrame(point_list, columns=['geometry'])
        processed_points.to_file(f'{out_dir}/{bypass_fname}', driver=bypass_driver)
    cycle_racks['geometry'] = gpd.GeoSeries(point_list)
    log(f'crs of master geojson changed to {out_crs}')
    return cycle_racks

#----------------------------------------------------------------------------------------------------
#removes all elements of the geodataframe 'cycle_racks' contain points with values that couldn't exist
#----------------------------------------------------------------------------------------------------
def remove_invalid(border, cycle_racks):
    """Removes all elements of the geodataframe 'cycle_racks' contain points with values that couldn't exist

    Args:
        border (geodataframe): border geodataframe
        cycle_racks (geodataframe): cycle_racks geodataframe pre-modification
    
    Returns:
        cycle_racks (geodataframe): cycle_racks geodataframe post-modification
     
    """
    
    log('searching for invalid data... this make take a while')
    tenth_step = int(np.ceil(len(cycle_racks)/10))
    invalids = 0
    for i in range(len(cycle_racks)):
        point = cycle_racks.loc[i,'geometry']
        if border.contains(point) == False:
            cycle_racks.drop(index=i)
            invalids += 1
            log(f'removed rack: {cycle_racks.loc[i, "FEATURE_ID"]} (outside of border) - listed in master geojson as within {cycle_racks.loc[i, "BOROUGH"]}')
        if (i+1) % tenth_step == 0:
            log(f'{int((i+1)/tenth_step)*10}% searched...')
    log(f'search complete - {invalids} rows removed')
    return cycle_racks

#----------------------------------------------------------------------------------------------------
#this function is called only by clean_nulls checks to see of the value input is a boolean value, if
#it is not it checks to see if a string equivilent to true. If neither it sets the value to False.
#----------------------------------------------------------------------------------------------------
def validate_boolean(value):
    if value == True or value == False:
        return value
    elif value == 'true' or value == 'True' or value == 'TRUE':
        return True
    else:  
        return False
        
#----------------------------------------------------------------------------------------------------
#checks all of the boolean values using the validate_boolean function above. It also checks if the
#integer value is a value that can be converted to integer (either integer already, a decimal or a
#string containing only a number)
#----------------------------------------------------------------------------------------------------
def clean_nulls(rack_data):
    for i in range(len(rack_data)):
        rack_data.loc[i,'PRK_COVER'] = validate_boolean(rack_data.loc[i,'PRK_COVER'])
        rack_data.loc[i,'PRK_SECURE'] = validate_boolean(rack_data.loc[i,'PRK_SECURE'])
        rack_data.loc[i,'PRK_LOCKER'] = validate_boolean(rack_data.loc[i,'PRK_LOCKER'])
        try:
            rack_data.loc[i,'PRK_CPT'] = int(rack_data.loc[i,'PRK_CPT'])
        except:
            rack_data.loc[i,'PRK_CPT'] = 'UNKNOWN'
    return rack_data

#----------------------------------------------------------------------------------------------------
#splits the geodataframe 'cycle_racks' into a geodataframe containing only it's geospacial components
#and a standard dataframe containing everything else
#----------------------------------------------------------------------------------------------------
def split_geoframe(cycle_racks):
    """Splits the geodataframe 'cycle_racks' into a geodataframe containing only it's geospacial components
    and a standard dataframe containing everything else

    Args:
        cycle_racks (geodataframe): Geodataframe of the cycle racks
        out_dir (str): {Value in config file} Name of the output directory folder
        out_data_fname (str): {Value in config file} Value representing the "out_data_fname" parameter in the config 
        out_geometry_fname (str): {Value in config file} Value representing the "out_geometry_fname" parameter in the config 
        out_driver (str): {Value in config file} The driver to be used

    """

    log('splitting master geojson into geospacial and non geospacial components...')
    #rack_data = pd.DataFrame(cycle_racks.drop(['geometry'],axis=1))
    rack_data = pd.DataFrame(cycle_racks[['FEATURE_ID','PRK_COVER','PRK_SECURE','PRK_LOCKER','PRK_CPT','BOROUGH','PHOTO1_URL','PHOTO2_URL']])
    rack_geometry = gpd.GeoDataFrame(cycle_racks[['FEATURE_ID','geometry']])
    return clean_nulls(rack_data), rack_geometry

#----------------------------------------------------------------------------------------------------
#writes the split master file to a geojson and a csv
#----------------------------------------------------------------------------------------------------
def write_rack_files(rack_data,rack_geometry,data_dir,geometry_dir,out_driver):
    """Saves rack_data data frame to csv file and save rack_geometry to geojson file

    Args:
        rack_data (dataframe): Rack data dataframe
        rack_geometry (dataframe): Rack geometry dataframe
        data_dir (str): Output directory file name "cycle_parking_data.csv"
        geometry_dir (str): Output directory file name "borough_geometry.geojson"
        out_driver (str): {Value in config file} The driver to be used


    """    
    rack_data.to_csv(data_dir,index=False)
    rack_geometry.to_file(geometry_dir,driver=out_driver)
    log(f'master geojson split and saved to the "{data_dir}" and "{geometry_dir}"')

#----------------------------------------------------------------------------------------------------
#adds data from a given dataframe (names) to a given geodataframe (shapes), drops 'fid' as these are
#not integers so are less useful than the integer 'ID' value from borough_names
#----------------------------------------------------------------------------------------------------
def combine_dataframes(shapes,names):
    """Adds data from a given dataframe (names) to a given geodataframe (shapes), drops 'fid' as these are
    not integers so are less useful than the integer 'ID' value from borough_names.

    Args:
        names (dataframe): Names dataframe
        shapes (dataframe): Shapes dataframe pre-addition
        
    Returns:
        shapes (dataframe): Shapes dataframe post-addition

    """
    shapes['name'] = names['name']
    shapes.drop(['fid'],axis=1,inplace=True)
    return shapes

#----------------------------------------------------------------------------------------------------
#takes a list of shapely points and returns a tuple of lists, one of eastings, one of northings
#----------------------------------------------------------------------------------------------------
def get_eastings_northings(points):
    """Creates a list of eastings and northing x,y coordinates 
    Args:
        points (dataframe): Rack geometry
        
        
    Returns:
        eastings (list): Easting, x coordinates of bike racks
        northings (list): Northing, y coordinates of bike racks

    """
    eastings = []
    northings = []
    for current_point in points:
        eastings.append(current_point.y)
        northings.append(current_point.x)
    return eastings, northings

#----------------------------------------------------------------------------------------------------
#takes a tuple containing lists of eastings and northings and finds values defining distribution
#these values are returned as a dataframe
#----------------------------------------------------------------------------------------------------
def get_stats(positions):
    """Calculates mean, standard deviation, minimum and maximums of eastings and northings
    Args:
        positions (list): easting and northing data lists
        
        
    Returns:
        stats(dataframe): data frame containing statistical measures
    """
    eastings, northings = positions[0], positions[1]
    e_mean, n_mean = np.mean(eastings), np.mean(northings)
    e_std, n_std = np.std(eastings), np.std(northings)
    e_min, n_min = min(eastings), min(northings)
    e_max, n_max = max(eastings), max(northings)
    stats = {'type':['mean','standard_deviation','lowest_value','highest_value'],'easting':[e_mean,e_std,e_min,e_max],'northing':[n_mean,n_std,n_min,n_max]}
    return pd.DataFrame(stats)

#----------------------------------------------------------------------------------------------------
#calls other functions with values from the config file
#----------------------------------------------------------------------------------------------------
def process_data(config):
    """Calls other functions with values from the config file

    Args:
        config (json file): The dictionary containing configuration file parameters and values. 

    """
    
    form_outdir(config['out_dir'])
    border, borough_names, borough_geometry, cycle_racks = load_inputs(config['in_dir'],config['master_geojson'],config['border_geojson'],config['boroughs_geojson'],config['borough_names_csv'])
    #The statement if borough_names.empty == False: verifies that the load_input fuction was successful
    #and thus acts as a verification step for all values generated by this step, not just borough_names
    if borough_names.empty == False:
        cycle_racks = convert_crs(cycle_racks, config['master_crs'], config['final_crs'], config['in_dir'], config['out_dir'], config["bypass_fname"], config['driver'])
        cycle_racks = remove_invalid(border, cycle_racks)
        rack_data, rack_geometry = split_geoframe(cycle_racks)
        write_rack_files(rack_data, rack_geometry,f'{config["out_dir"]}/{config["out_data_fname"]}',f'{config["out_dir"]}/{config["out_geometry_fname"]}',config['driver'])
        log('creating additional outputs...')
        combine_dataframes(borough_geometry,borough_names).to_file(f'{config["out_dir"]}/{config["out_borough_geometry_fname"]}',driver=config['driver'])
        rack_data['BOROUGH'].value_counts().reset_index().rename(columns={'index':'name','BOROUGH':'count'}).to_csv(f'{config["out_dir"]}/{config["out_borough_count_fname"]}',index=False)
        get_stats(get_eastings_northings(rack_geometry['geometry'].tolist())).to_csv(f'{config["out_dir"]}/{config["out_stats_fname"]}',index=False)
        log(f'additional outputs created successfully and saved to {config["out_dir"]}')

#----------------------------------------------------------------------------------------------------
#checks if the dictionary given contains the required values to enable the script to function if this
#is the case pass_validation is called, sending the config file through the rest of the script
#----------------------------------------------------------------------------------------------------
def validate_config(config):
    """The configuration file is validated by ensuring that the parameters and values are all present.
    On successful validation, the configuration file is then passed on and used by the program.

    Args:
        config (json file): Configuration file data.

    Returns:
        True - > if the configuration file is valid.
        False -> if there are missing parameters or fields in the configuration file.
    """

    log('validating config...')
    if config != 'NULL':
        if 'in_dir' and 'out_dir' and 'master_geojson' and 'border_geojson' and 'boroughs_geojson' and 'borough_names_csv' and 'master_crs' and 'final_crs' and 'out_geometry_fname' and 'out_data_fname' and 'out_boroughs_fname' and 'bypass_fname' and 'driver' in config:
            if os.path.exists(f'{config["in_dir"]}/{config["master_geojson"]}') and os.path.exists(f'{config["in_dir"]}/{config["border_geojson"]}') and os.path.exists(f'{config["in_dir"]}/{config["boroughs_geojson"]}') and os.path.exists(f'{config["in_dir"]}/{config["borough_names_csv"]}'):
                log('config valid')
                return True
            else:
                log(f'ERROR - the "{config["in_dir"]}" directory is missing or the files "{config["in_dir"]}/{config[""]}" are missing!')
                return False
        else:
            log('ERROR - the config file must contain the keys "in_dir","out_dir"!')
            return False
    else:
        log('ERROR - the config file has be incorrectly constructed and thus the script cannot continue!')
        return False
        
#----------------------------------------------------------------------------------------------------
#establishes dictionary of global values from a config file and calls validate_config() on this dictionary
#----------------------------------------------------------------------------------------------------
def get_config():
    """The configuration text file is loaded and a JSON dictionary is created so that parameters
    from the file can be used by the program.

    Returns:
        if successful - >
        config (json): A dictionary containing the parameters from the configuration file.

        if unsuccessful - >
        'NULL'
    """

    log('loading config...')
    with open('data_prep_config.txt') as f:
        config_txt = f.read()
    #tries to reconstruct the data as a dictionary, if this is possible it calls the validate_config function
    try:
        config = json.loads('{'+config_txt+'}')
        log('config loaded')
        return config
    except:
        return 'NULL'

#----------------------------------------------------------------------------------------------------
#calls function to aquire the config dictionary, calls function to validate this dictionary and if 
#----------------------------------------------------------------------------------------------------
def main():
    """Acquires the config dictionary, calls function to validate this dictionary and if the config
    is successfully validated, the main script is then run.

    """
    out_file = open('data_prep_log.txt', 'a')
    out_file.write(f'{"-"*100}\n{dt.datetime.now()} - SCRIPT START\n{"-"*100}\n')
    out_file.close()
    print('--> FOR TIMESTAMPED LOGS RECORDS PLEASE TAIL THE "data_processing_log.txt" FILE <--')
    config = get_config()
    if validate_config(config):
        process_data(config)

#----------------------------------------------------------------------------------------------------
#calls the main function after all the functions have been initialised
#----------------------------------------------------------------------------------------------------
main()