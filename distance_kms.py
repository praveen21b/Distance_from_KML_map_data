import logging
from pickletools import long1
import bs4
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
from dist_exception import DistanceException
#from dist_log import logging
import os,sys
import lxml
import matplotlib.pyplot as plt

def parse_kml_data(file_name)->bs:
    """ This functions reads kml data file and returns BeautifulSoup object"""
    try:
        logging.info(f'{file_name} reading and parsing commenced.')
        with open(file_name) as file:
            soup = bs(file,'xml') # lxml or html.parser for web
            #print(soup.prettify())
            logging.info(f'The file execution has been completed successfully.')
            return soup
    except Exception as e:
        raise DistanceException(e,sys) from e


def get_coord_details(parsed_page:bs)->list:
    """ This functions reads BeautifulSoup object and returns list of coordinates from the page"""
    try:

        coord_string = (('').join((parsed_page.find_all('coordinates'))[0])).strip(' \n ')
        coord_list = coord_string.split(' ')
        logging.info(f'The list of coordinates are generated.')
        return coord_list

        
    except Exception as e:
        raise DistanceException(e,sys) from e 

def get_dataframe_and_filter_data(co_list:list) -> pd.DataFrame:
    """ This functions coverts list of cordinate tuple into dataframe 
        and removes duplicate value.
    """
    try:
        df = pd.DataFrame({'coordinates':co_list})
        df.drop_duplicates(inplace=True, ignore_index=True)
        logging.info(f'Filtering has been performed successfully.')
        return df

    except Exception as e:
        raise DistanceException(e,sys) from e 

def get_df_with_coord_names(data: pd.DataFrame) -> pd.DataFrame:
    """
        Function recieves a dataframe with one column of coordination details 
        and returns a dataframe with seperate columns for longitude, lattitude,
        and altitude with keeping all as numercial data type.

    """
    try:
        df = data['coordinates'].str.split(',', expand=True)
        df.columns = ['longitude', 'latitude', 'altitude']
        # type cast columns (string -> float)
        df = df.astype(float)
        #df.describe()

        # visualization
        #plt.figure(figsize=(20,20))
        #plt.scatter(df_out['longitude'],df_out['latitude'])
        #plt.show()
        logging.info(f'Final dataframe obatined')
        return df

    except Exception as e:
        raise DistanceException(e,sys) from e


def get_row_shifted_df(df:pd.DataFrame) -> tuple:
    """ 
        This helper function provides input to calculate the distance.
        The dataframes shifts rows to calculates the distance.
        retuns tuple of dataframes.
    
    """
    try:
        point1_long = df['longitude'].shift()
        point1_lat = df['latitude'].shift()
        point2_long = df.loc[1:, 'longitude']
        point2_lat = df.loc[1:, 'latitude']
        logging.info(f'The inputs for calculating distance is calculated.')
        return point1_long, point1_lat, point2_long, point2_lat

    except Exception as e:
        raise DistanceException(e,sys) from e



def calculate_distance(lon1:pd.DataFrame, lat1:pd.DataFrame, 
                        lon2:pd.DataFrame, lat2:pd.DataFrame, 
                        to_radians:bool=True, earth_radius:int=6371) -> float:
    """
    This function calcualtes distance in kms between two coordinate points.
    and retuns distance in km

    """
    try:
        if to_radians:
            lon1, lat1, lon2, lat2 = map(np.radians,[lon1,lat1,lon2,lat2])

        a = np.sin((lat2-lat1)/2.0)**2 + \
             np.cos(lat1) * np.cos(lat2) * np.sin((lon2-lon1)/2.0)**2

        logging.info(f'The distance between 2 consective coordinate points are calculated.')
        return earth_radius * 2 * np.arcsin(np.sqrt(a))

    except Exception as e:
        raise DistanceException(e,sys) from e


