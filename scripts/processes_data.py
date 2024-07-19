# Process raw data into new files
import pandas as pd
import os

LOCATIONS_FILE_NAME = "../data/bicing/processed/2024_STATION_LOCATIONS.csv"
PROCCESED_FOLDER = "../data/bicing/processed"
RAW_FILE_NAME = "../data/bicing/raw/2024_INFO.csv"


def read_stations_csv() -> pd.DataFrame:
    return pd.read_csv(RAW_FILE_NAME)


def get_max_capacity_by_station(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[df.groupby('station_id')['capacity'].idxmax()]


def remove_incorrect_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df['station_id'] != 535]
    # post_code for station 35 is incorrect the correct one is C/ SANT RAMON DE PENYAFORT, 1, 08019 Barcelona
    df.loc[df['station_id'] == 35, 'post_code'] = 8019
    return df


def remove_unnecessary_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df[['station_id', 'lat', 'lon', 'altitude', 'post_code', 'capacity', 'address']]


def fix_types(df: pd.DataFrame) -> pd.DataFrame:
    df['station_id'] = df['station_id'].astype(int)
    df['capacity'] = df['capacity'].astype(int)
    # post_code should be string removing the .0 and add a 0 at the beginning
    df['post_code'] = "0" + df['post_code'].astype(str).str.replace('.0', '')
    return df


def map_post_code_to_district(df: pd.DataFrame) -> pd.DataFrame:
    barcelona_postal_codes = {
        "08001": "Ciutat Vella", "08002": "Ciutat Vella", "08003": "Ciutat Vella",
        "08004": "Sants-Montjuïc", "08005": "Sant Martí", "08006": "Sarrià-Sant Gervasi",
        "08007": "Eixample", "08008": "Eixample", "08009": "Eixample",
        "08010": "Eixample", "08011": "Eixample", "08012": "Gràcia",
        "08013": "Eixample", "08014": "Sants-Montjuïc", "08015": "Eixample",
        "08016": "Nou Barris", "08017": "Sarrià-Sant Gervasi", "08018": "Sant Martí",
        "08019": "Sant Martí", "08020": "Sant Martí", "08021": "Sarrià-Sant Gervasi",
        "08022": "Sarrià-Sant Gervasi", "08023": "Sarrià-Sant Gervasi", "08024": "Gràcia",
        "08025": "Horta-Guinardó", "08026": "Sant Martí", "08027": "Sant Andreu",
        "08028": "Les Corts", "08029": "Les Corts", "08030": "Sant Andreu",
        "08031": "Nou Barris", "08032": "Horta-Guinardó", "08033": "Nou Barris",
        "08034": "Les Corts", "08035": "Horta-Guinardó", "08036": "Eixample",
        "08037": "Eixample", "08038": "Sants-Montjuïc", "08039": "Sants-Montjuïc",
        "08040": "Sant Martí", "08041": "Horta-Guinardó", "08042": "Nou Barris",
        "08043": "Sarrià-Sant Gervasi", "08044": "Nou Barris", "08045": "Sant Andreu",
        "08046": "Sant Andreu", "08047": "Nou Barris", "08048": "Sant Martí",
        "08049": "Nou Barris"
    }
    return df['post_code'].map(barcelona_postal_codes)


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    if df['district'].isnull().sum() > 0:
        # raise ValueError('There are null values in district column')
        print('ERROR: There are null values in district column',
              df[df['district'].isna()])


def create_folder():
    # create processed folder inside data if it does not exist
    if not os.path.exists(PROCCESED_FOLDER):
        os.makedirs(PROCCESED_FOLDER)
        print(f"Folder '{PROCCESED_FOLDER}' created.")
    else:
        print(f"Folder '{PROCCESED_FOLDER}' already exists.")


def create_station_location_file():
    df = read_stations_csv()
    df = get_max_capacity_by_station(df)
    df = remove_incorrect_data(df)
    df = remove_unnecessary_columns(df)
    df = fix_types(df)
    df['district'] = map_post_code_to_district(df)
    validate_data(df)
    create_folder()
    df.to_csv(LOCATIONS_FILE_NAME, index=False)
    print(f'file {LOCATIONS_FILE_NAME} created successfully')


def main():
    create_station_location_file()


if __name__ == '__main__':
    main()
