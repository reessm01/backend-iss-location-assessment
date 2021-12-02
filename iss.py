#!/usr/bin/env python

import requests
from turtle import Turtle, Screen
import time
import pprint

indy_lat = 39.7684
indy_long = -86.1581

pp = pprint.PrettyPrinter(indent=4)

__author__ = 'Scott Reese'

def fetch_astronauts():
    r = requests.get("http://api.open-notify.org/astros.json")
    astro_data = r.json()['people']
    astronauts = [(astronaut['craft'], astronaut['name']) for astronaut in astro_data]
    msg = "There are {} astronauts in space: ".format(len(astro_data))
    for i, astronaut in enumerate(astronauts):
        if i == len(astronauts)-1:
            msg += "and {} (aboard the {}).".format(astronaut[1], astronaut[0])
        else: 
            msg += "{} (aboard the {}), ".format(astronaut[1], astronaut[0])
    print(msg)

def fetch_iss_loc():
    r = requests.get("http://api.open-notify.org/iss-now.json")
    return r.json()['iss_position']

def fetch_next_flyby(longitude, latitude):
    url = 'http://api.open-notify.org/iss-pass.json'
    params = {'lat': latitude, 'lon': longitude}
    r = requests.get(url, params=params)
    r.raise_for_status()
    print("Next time ISS is visible from your coordinates: " + time.ctime(r.json()['response'][0]['risetime']) + ".")

def draw_canvas(longitude, latitude):
    screen = Screen()
    screen.setup(width=720,height=360)
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.bgpic('map.gif')
    
    screen.register_shape("iss.gif")
    iss = Turtle(shape="iss.gif")
    iss.goto(longitude, latitude)
    iss.penup()
    iss.tracer(False)

    marker = Turtle()
    marker.goto(indy_long, indy_lat)
    marker.dot(5, "red")

    screen.exitonclick()

def main():
    fetch_astronauts()
    iss_location = fetch_iss_loc()
    fetch_next_flyby(indy_long, indy_lat)

    iss_lon = float(iss_location['longitude'].decode())
    iss_lat = float(iss_location['latitude'].decode())
    draw_canvas(iss_lon, iss_lat)

if __name__ == '__main__':
    main()
