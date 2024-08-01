# curl https://com-shi-va.barcelona.cat/es/bicicleta?action=planroute&origin_id=ChIJGehS27qipBIRdIyFkC7kqZ8&origin=Carrer%20de%20Massens,%2076,%20Barcelona,%20Espanya&destination_id=ChIJiyQV0QaYpBIRy_3p95r54KE&destination=AV.%20VALLCARCA,%20196&travelMode=BICYCLING&layers=1020
import requests


class = 'float-right duration'
class_2 = '<div class="desc" role="button"><img class="icon" src="/images/icons/bicycle.svg"><span>Av. de Vallcarca <div class="distance">2,2 km</div></span></div>'


def fetch_data(url):
    response = requests.get(url)
    data = response.json()
    return data

def get_information(html):
    result = {'duration': None, 'distance': None}

    return result
    pass

def main():
    pass

if __name__ == '__main__':
    main()


https://com-shi-va.barcelona.cat/es/bicicleta?action=planroute&origin=Carrer%20de%20Massens,%2076,%20Barcelona,%20Espanya&destination=AV.%20VALLCARCA,%20196&travelMode=BICYCLING&layers=1020