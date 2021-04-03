import argparse
import time

import geopy.distance
import requests

import pyttsx3
engine = pyttsx3.init()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Align scan with STAR body model.')
    parser.add_argument('--latitude', default=37.68206012403199, type=float, help='Query latitude')
    parser.add_argument('--longitude', default=-121.77050639636045, type=float, help='Query longitude')
    parser.add_argument('--state', default='CA', help='US state of location (2-letter abbreviation -- ex. CA)')
    parser.add_argument('--radius', default=50, type=float, help='Radius of search (miles)')
    args = parser.parse_args()

    query_coordinates = (args.latitude, args.longitude)

    prev_ids = []
    while True:
        announce = False
        cur_ids = []
        api_request = requests.get('https://www.vaccinespotter.org/api/v0/states/' + args.state + '.json')
        assert api_request.status_code == 200, 'Erroneous API response, check that input state is valid'
        api_data = api_request.json()
        for f in api_data['features']:
            if not f['properties']['appointments_available']: continue
            f_coordinates = (f['geometry']['coordinates'][1], f['geometry']['coordinates'][0])
            query_dist = geopy.distance.distance(query_coordinates, f_coordinates).miles
            if query_dist < args.radius:
                cur_ids.append(f['properties']['id'])
                if f['properties']['id'] not in prev_ids:
                    print(f)
                    announce = True
        if announce:
            engine.say("New appointments available")
            engine.runAndWait()
        prev_ids = cur_ids
        time.sleep(1)



