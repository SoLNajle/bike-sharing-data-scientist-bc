# Process raw data into new files
import pandas as pd
import os

from helpers import assign_datatypes_month_df, create_folder


PROCCESED_FOLDER = "../data/bicing/processed/months"
RAW_FOLDER = "../data/bicing/raw"
RAW_FILES_NAME = ["2023_01_STATIONS", "2023_02_STATIONS", "2023_03_STATIONS", "2023_04_STATIONS", "2023_05_STATIONS", "2023_06_STATIONS",
                  "2023_07_STATIONS", "2023_08_STATIONS", "2023_09_STATIONS", "2023_10_STATIONS", "2023_11_STATIONS", "2023_12_STATIONS"]


def read_stations_csv(file_name: str) -> pd.DataFrame:
    return pd.read_csv(file_name)


def save_df_to_csv(df: pd.DataFrame, file_name: str) -> None:
    try:
        df.to_csv(file_name, index=False)
        print(f"File {file_name} saved.")
    except Exception as e:
        raise Exception(f"Error saving file: {e}")


def drop_useless_data_columns(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df.drop('ttl', axis=1, inplace=True)
        df.drop('is_charging_station', axis=1, inplace=True)
        df.drop('traffic', axis=1, inplace=True)
        return df
    except Exception as e:
        raise Exception(f"Error dropping columns: {e}")


def format_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df['last_reported'] = pd.to_datetime(df['last_reported'], unit='s')
        # df['last_updated'] = pd.to_datetime(df['last_updated'], unit='s')
        return df
    except Exception as e:
        raise Exception(f"Error formatting date columns: {e}")


def create_new_columns(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df['year'] = df['last_reported'].dt.year
        df['month'] = df['last_reported'].dt.month
        df['day'] = df['last_reported'].dt.day
        df['hour'] = df['last_reported'].dt.hour
        df['minute'] = df['last_reported'].dt.minute
        # group 0-15 --> 15, 16-30 -->30, 31-45 -->45 , 46-59 --> 0
        df['grouped_minute'] = df['minute'].apply(
            lambda x: 0 if x < 15 else 15 if x < 30 else 30 if x < 45 else 45)

        df['day_of_week'] = df['last_reported'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x > 4 else 0)
        df['grouped_date'] = df['year'].astype(str) + '-' + df['month'].astype(str) + '-' + df['day'].astype(str) + ' ' + df['hour'].astype(
            str) + ':' + df['grouped_minute'].astype(str).apply(lambda x: '0' + str(x) if int(x) < 10 else str(x))
        print("New columns created.")
        return df

    except Exception as e:
        raise Exception(f"Error creating new columns: {e}")


def add_is_docking_available_column(df: pd.DataFrame) -> pd.DataFrame:
    df['docking_available'] = df['num_docks_available'].apply(
        lambda x: False if x == 0 else True) & df['is_returning'].apply(lambda x: False if x == 0 else True)
    return df


def add_is_renting_columns(df: pd.DataFrame) -> pd.DataFrame:
    df['bikes_available'] = df['num_bikes_available'].apply(
        lambda x: False if x == 0 else True) & df['is_renting'].apply(lambda x: False if x == 0 else True)
    df['bikes_available.mechanical'] = df['num_bikes_available_types.mechanical'].apply(
        lambda x: False if x == 0 else True) & df['is_renting'].apply(lambda x: False if x == 0 else True)
    df['bikes_available.ebike'] = df['num_bikes_available_types.ebike'].apply(lambda x: False if x == 0 else True) & df['is_renting'].apply(
        lambda x: False if x == 0 else True)
    return df


def drop_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df.drop('last_reported', axis=1, inplace=True)
        #   df.drop('last_updated', axis=1, inplace=True)
        df.drop('minute', axis=1, inplace=True)
    except Exception as e:
        print(f"Error dropping columns: {e}")
    print("Date columns dropped.")
    return df


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df.drop_duplicates(inplace=True)
    except Exception as e:
        print(f"Error dropping duplicates: {e}")
    print("Duplicates dropped.")
    return df


def filter_columns_to_keep(df: pd.DataFrame) -> pd.DataFrame:
    columns_to_keep = ['station_id', 'num_bikes_available',
                       'num_bikes_available_types.mechanical', 'num_bikes_available_types.ebike', 'num_docks_available',
                       'last_reported', 'status', 'is_renting', 'is_returning']
    return df[columns_to_keep]


def drop_na_rows(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()


def create_month_files() -> None:
    total_rows_prune = 0
    total_rows_raw = 0
    create_folder(PROCCESED_FOLDER)
    for file_name in RAW_FILES_NAME:
        processed_rows = 0
        raw_rows = 0
        raw_file_name = os.path.join(RAW_FOLDER, f"{file_name}.csv")
        processed_file_name = os.path.join(
            PROCCESED_FOLDER, f'{file_name}.csv')
        # if file exists skip
        if os.path.exists(processed_file_name):
            print(f"File {processed_file_name} already exists.")
            continue

        df = read_stations_csv(raw_file_name)

        raw_rows = len(df)
        total_rows_raw += raw_rows
        print(f"Processing file {raw_file_name} with {raw_rows} rows.")
        # Processing Starts

        df = filter_columns_to_keep(df)
        df = drop_na_rows(df)
        df = format_date_columns(df)
        df = create_new_columns(df)
        df = drop_date_columns(df)
        df = drop_duplicates(df)
        # count how many records
        df = add_is_docking_available_column(df)
        df = add_is_renting_columns(df)
        processed_rows = len(df)
        total_rows_prune += raw_rows - processed_rows
        df = assign_datatypes_month_df(df)
        save_df_to_csv(df, processed_file_name)

    print("All files processed.")
    print(f"Total rows processed: {total_rows_raw}.")
    print(f"Total rows pruned: {total_rows_prune} from all 2023 months.")
    total_rows_raw = 1 if total_rows_raw == 0 else total_rows_raw
    print(F"Percentage of Data removed: {total_rows_prune/total_rows_raw*100:.2f}%.")


if __name__ == '__main__':
    create_month_files()
