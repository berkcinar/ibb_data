import urllib
import requests

# url = 'https://data.ibb.gov.tr/api/3/action/datastore_search?resource_id=52afa9a3-2ea1-420b-a783-505cfe635ece'
# fileobj = requests.get(url,param limit)
# fileobj=fileobj.json()
# print(fileobj)
import json
# importing the requests library
import requests
from darksky import forecast
from datetime import datetime as dt

class Solar_Generation():
    def get_ikitelli_generation(self):
        # api-endpoint
        URL = "https://data.ibb.gov.tr/api/3/action/datastore_search?resource_id=52afa9a3-2ea1-420b-a783-505cfe635ece"

        r = requests.get(url=URL)
        data = r.json()
        # location given here
        param_limit = data['result']['total']
        # defining a params dict for the parameters to be sent to the API
        PARAMS = {'limit': param_limit}
        # sending get request and saving the response as response object
        r = requests.get(url=URL, params=PARAMS)
        # extracting data in json format
        data = r.json()
        data['result']['total']
        print(data['result']['records'])

        for i in data['result']['records']:
            print(i['Tarih'],i['Uretim (kWh)'])

    # def get_solar_radiaton_NASA(self):
    #     # URL = "https://api.darksky.net/forecast/992bb820ba82528fffc192c56bf6921e/41.086903,28.765224"
    #     URL = "https://api.darksky.net/forecast/"
    #
    #     api_key='992bb820ba82528fffc192c56bf6921e'
    #     params = {'latitude':41.086903,
    #               'longitude':28.765224,
    #               'language':'uk'}
    #     # params = {'SomeParam': x,
    #     #           'SomeOtherParam': y,
    #     #           'AnotherOne': z}
    #
    #     URL+=api_key+'/'
    #
    #     for i in params:
    #         URL+=str(params[i])+','
    #     print(URL)
    #     r = requests.get(url=URL[:-1])
    #     data = r.json()
    #     print(data)

    def get_from_darksky(self):
        api_key = '992bb820ba82528fffc192c56bf6921e'
        latitude= 41.086903
        longitude=28.765224


        energypool_latitude=41.086400
        energypool_longitude=29.020917


        t = dt(2013, 5, 6, 12).isoformat()
        energypool = forecast(api_key, energypool_latitude, energypool_longitude,time=t)
        print(energypool)
        print(energypool['currently']['temperature'])
        print(energypool['hourly']['data'])
    def run(self):
        self.get_from_darksky()

Solar_Generation().run()