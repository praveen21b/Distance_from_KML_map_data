from pkg_resources import get_default_cache
from dist_exception import DistanceException
from dist_log import logging
import sys, os
from distance_kms import calculate_distance, get_dataframe_and_filter_data, get_df_with_coord_names, get_row_shifted_df, parse_kml_data,get_coord_details

def get_distance(file)->float:
    try:
        logging.info(f'The file execution has been started.')
        soup = parse_kml_data(file)
        coord_list = get_coord_details(soup)
        df_no_duplicates = get_dataframe_and_filter_data(coord_list)
        df = get_df_with_coord_names(df_no_duplicates)
        lon1,lat1,lon2,lat2 = get_row_shifted_df(df)
        df['distance_km'] = calculate_distance(lon1,lat1,lon2,lat2)
        logging.info(f'The file execution has been completed.')
        #return df.fillna(0)['distance_km'].sum() ## has outliers
        threshold_distnace = 0.06 #km assuming distance between 2 coord points is ~50m-60m
        return df['distance_km'][df['distance_km'].sort_values(ascending=False) < threshold_distnace].sum()
    except Exception as e:
        raise DistanceException(e,sys) from e


if __name__ == '__main__':
    print(f"Total of {get_distance('task_2_sensor.kml')} km of distance travelled by the vehicle")