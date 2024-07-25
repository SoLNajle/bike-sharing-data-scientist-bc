# Process raw data into new files
import pandas as pd
import os

from helpers import assign_datatypes_month_df, create_folder


DAYS_FOLDER = "../data/bicing/processed/months/days"
MONTH_FOLDER = "../data/bicing/processed/months/"
STATION_FILE = '../../data/bicing/processed/2024_STATION_LOCATIONS.csv'
MONTH_FILES_NAME = ["2023_01_STATIONS", "2023_02_STATIONS", "2023_03_STATIONS", "2023_04_STATIONS", "2023_05_STATIONS", "2023_06_STATIONS",
                    "2023_07_STATIONS", "2023_08_STATIONS", "2023_09_STATIONS", "2023_10_STATIONS", "2023_11_STATIONS", "2023_12_STATIONS"]
FILE_NAME = '_busiest_day.csv'

def read_stations_csv(file_name: str) -> pd.DataFrame:
    return pd.read_csv(file_name)


def save_df_to_csv(df: pd.DataFrame, file_name: str) -> None:
    try:
        df.to_csv(file_name, index=False)
        print(f"File {file_name} saved.")
    except Exception as e:
        raise Exception(f"Error saving file: {e}")


def calculate_diff_between_rows(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df['bike_available_diff'] = df.groupby(
            ['station_id'])['num_bikes_available'].diff()
        df['bike_available_diff'] = df['bike_available_diff'].apply(
            lambda x: abs(x))
        return df
    except Exception as e:
        raise Exception(f"Error calculating diff between rows: {e}")


def order_by_date(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values(by=['year', 'month', 'day', 'hour', 'grouped_minute'], ascending=True)


def find_busiest_day(df: pd.DataFrame) -> int:
    try:
        df_month_busiest_days = df.groupby('day').agg(
            {'bike_available_diff': 'sum'}).reset_index()
        busiest_day = df_month_busiest_days.sort_values(
            by='bike_available_diff', ascending=False).head(1)
        return busiest_day['day'].values[0]
    except Exception as e:
        raise Exception(f"Error finding busiest day: {e}")


def filter_df_by_day(df: pd.DataFrame, day: int) -> pd.DataFrame:
    return df[df['day'] == day]


def add_station_info(df: pd.DataFrame, station_df: pd.DataFrame) -> pd.DataFrame:
    return pd.merge(df, station_df, on='station_id', how='left')




def validate_file_does_not_exits(file_name: str) -> bool:
    #find files inside days folder
    files = os.listdir(DAYS_FOLDER)
    month = file_name.split('_')[1]
    year = file_name.split('_')[0]
    ending_file_name = f'{year}_{month}{FILE_NAME}'
    for file in files:
        if file.endswith(ending_file_name):
            print(f"File {file} already exists.")
            return True
    return False

def create_busiest_days_files() -> None:
    print("Creating busiest days files...")
    start_time = pd.Timestamp.now()
    create_folder(DAYS_FOLDER)
    for file_name in MONTH_FILES_NAME:
        if validate_file_does_not_exits(file_name):
            #skip processing because file already exists
            continue
        print(f"Processing file {file_name}")
        df = read_stations_csv(os.path.join(MONTH_FOLDER, file_name + ".csv"))
        df = assign_datatypes_month_df(df)
        df = order_by_date(df)
        df = calculate_diff_between_rows(df)
        busiest_day = find_busiest_day(df)
        df = filter_df_by_day(df, busiest_day)
        df = add_station_info(df, read_stations_csv(STATION_FILE))
        month = file_name.split('_')[1]
        year = file_name.split('_')[0]
        new_file_name = f'{month}{busiest_day}_{year}_{month}{FILE_NAME}'
        save_df_to_csv(df, os.path.join(DAYS_FOLDER, new_file_name))
        print(f"File {new_file_name} saved with {len(df)} rows.")
    end_time = pd.Timestamp.now()
    print(f"Execution time: {end_time - start_time}")
    print("Process finished.")
if __name__ == '__main__':
    create_busiest_days_files()
