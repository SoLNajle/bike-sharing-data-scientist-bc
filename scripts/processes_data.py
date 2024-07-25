# Process raw data into new files
import pandas as pd
import os

from processes_data_busiest_day_per_month import create_busiest_days_files
from processes_data_monthly import create_month_files
from processes_data_station_location import create_station_location_file
from helpers import create_folder
ascii_message = """
                                                                                
8 888888888o.          ,o888888o.     b.             8 8 8888888888             
8 8888    `^888.    . 8888     `88.   888o.          8 8 8888                   
8 8888        `88. ,8 8888       `8b  Y88888o.       8 8 8888                   
8 8888         `88 88 8888        `8b .`Y888888o.    8 8 8888                   
8 8888          88 88 8888         88 8o. `Y888888o. 8 8 888888888888           
8 8888          88 88 8888         88 8`Y8o. `Y88888o8 8 8888                   
8 8888         ,88 88 8888        ,8P 8   `Y8o. `Y8888 8 8888                   
8 8888        ,88' `8 8888       ,8P  8      `Y8o. `Y8 8 8888                   
8 8888    ,o88P'    ` 8888     ,88'   8         `Y8o.` 8 8888                   
8 888888888P'          `8888888P'     8            `Yo 8 888888888888           
                                                                                
                                                                      
Data preprocessing is done!
check out jupyter --> http://localhost:1111/lab/tree/work/exploratory/stations.ipynb
"""
PROCCESED_FOLDER = "../data/bicing/processed"


def show_done_message():
    print(ascii_message)


def main():
    start_time = pd.Timestamp.now()
    create_folder(PROCCESED_FOLDER)
    create_station_location_file()
    create_month_files()
    create_busiest_days_files()
    show_done_message()
    end_time = pd.Timestamp.now()
    print(f"Total time: {end_time - start_time}")


if __name__ == '__main__':
    main()
