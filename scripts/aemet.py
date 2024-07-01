import requests
import os
import pandas as pd


BASE_URL = "https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/"
API_KEY = os.environ['AEMET_API_KEY']
AEMET_CSV_FILE_PATH = "data/aemet/aemet.csv"

def get_data(start_date, end_date, station):
    url = BASE_URL + \
        f"fechaini/{start_date}/fechafin/{end_date}/station/{station}"
    headers = {'Accept': 'application/json',
               'api_key': API_KEY
               }

    response = requests.request("GET", url, headers=headers)
    data = response.json()
    
    if data['estado'] == 200 and data['datos']:
        return fetch_data(data['datos'])
    return data


def fetch_data(url):
    response = requests.get(url)
    data = response.json()
    return data


def main():
    start_date = '2023-05-06T00:00:00UTC'
    end_date = '2024-03-31T00:00:00UTC'
    station = '0201D'
    aemet_df = pd.DataFrame()
    # call api for intervals of 30 days
    df = pd.date_range(start_date, end_date, freq='160D')

    for i in range(0, len(df)-1):
        start_date = df[i]

        start_date = start_date.strftime('%Y-%m-%dT%H:%M:%SUTC')
        end_date = df[i+1]
        end_date = end_date.strftime('%Y-%m-%dT%H:%M:%SUTC')
        data = get_data(start_date, end_date, station)
        partial_df = pd.DataFrame(data)
        aemet_df = pd.concat([aemet_df, partial_df], ignore_index=True)
    aemet_df.to_csv(AEMET_CSV_FILE_PATH, index=False)


if __name__ == '__main__':
    print('Fetching data...')
    main()
