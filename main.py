import argparse
import time

import geopy.distance
import requests

import pyttsx3
engine = pyttsx3.init()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Align scan with STAR body model.')
    parser.add_argument('--latitude', default=37.68206012403199, help='Query latitude')
    parser.add_argument('--longitude', default=-121.77050639636045, help='Query longitude')
    parser.add_argument('--radius', default=50, help='Radius of search (miles)')
    args = parser.parse_args()

    query_coordinates = (args.latitude, args.longitude)

    prev_ids = []
    while True:
        announce = False
        cur_ids = []
        ca_data = requests.get('https://www.vaccinespotter.org/api/v0/states/CA.json').json()
        for f in ca_data['features']:
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



