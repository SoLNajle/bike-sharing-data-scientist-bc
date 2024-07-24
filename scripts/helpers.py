import pandas as pd
import os

def assign_datatypes_month_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.astype({
        'station_id': int,
        'num_bikes_available': int,
        'num_bikes_available_types.mechanical': int,
        'num_bikes_available_types.ebike': int,
        'num_docks_available': int,
        'status': str,
        'is_renting': int,
        'is_returning': int,
        'year': int,
        'month': int,
        'day': int,
        'hour': int,
        'minute': int,
        'grouped_minute': int,
        'day_of_week': int,
        'is_weekend': int,
    })
    return df


def create_folder(folder_path: str) -> None:
    # create processed folder inside data if it does not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")