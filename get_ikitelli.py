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
from datetime import datetime as dt,timedelta
import pandas as pd
import time

class Solar_Generation():

    def get_ikitelli_generation(self):
        generation_df = pd.DataFrame()
        # api-endpoint
        URL = "https://data.ibb.gov.tr/api/3/action/datastore_search?resource_id=52afa9a3-2ea1-420b-a783-505cfe635ece"
        r = requests.get(url=URL)
        data = r.json()
        param_limit = data['result']['total']
        PARAMS = {'limit': param_limit}
        r = requests.get(url=URL, params=PARAMS)
        data = r.json()
        data['result']['total']
        for i in data['result']['records']:
            generation_df = generation_df.append({'timeslot': dt.strptime(i['Tarih'].replace("T"," "), '%Y-%m-%d %H:%M:%S'),'uretim': i['Uretim (kWh)'],},ignore_index=True)
            # df2 = df2.append({'timeslot': dt.fromtimestamp((i['Tarih']).strftime('%Y-%m-%d %H:%M:%S')),'uretim': i['Uretim (kWh)'],},ignore_index=True)

        print(generation_df)
        generation_df.set_index('timeslot', inplace=True)
        generation_df.resample('1H').mean()
        print(generation_df)
        return generation_df

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
        print(t)
        energypool = forecast(api_key, energypool_latitude, energypool_longitude,time=t)
        print(energypool)
        print(energypool['currently']['temperature'])
        print(energypool['hourly']['data'])
        print(energypool['hourly']['summary'])
        # print(energypool['hourly']['data'][0]['time'])
        time=energypool['hourly']['data'][0]['time']

        for i in energypool['hourly']['data']:
            print(dt.fromtimestamp(i['time']).strftime('%Y-%m-%d %H:%M:%S'))
            print(i['windSpeed'])
        print(dt.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'))

    def get_from_darksky_now(self,startdate=None,enddate=None):
        darksky_df=pd.DataFrame()
        api_key = '992bb820ba82528fffc192c56bf6921e'
        energypool_latitude=41.086400
        energypool_longitude=29.020917

        # print(dt(2020, 1, 28, 12))
        # print(dt(2020, 1, 28, 12)+timedelta(hours=10))

        # t = (dt(2020, 1, 28, 12).isoformat())
        # t=(dt(2020, 1, 29, 12)+timedelta(hours=15)).isoformat()
        startdate=dt(2019, 5, 1)
        enddate=dt(2019, 5, 31)
        t = dt(2019, 5, 31, 1).isoformat()
        while startdate<enddate:
            print(startdate)
            energypool = forecast(api_key, energypool_latitude, energypool_longitude,units='si',lang='tr',time=startdate.isoformat())
            for i in energypool['hourly']['data']:
                darksky_df = darksky_df.append({'timeslot': dt.fromtimestamp(i['time']).strftime('%Y-%m-%d %H:%M:%S'),
                                  'summary': i['summary'],
                                  'precipIntensity': i['precipIntensity'],
                                  'precipProbability': i['precipProbability'],
                                  'temperature': i['temperature'],
                                  'apparentTemperature': i['apparentTemperature'],
                                  'dewPoint': i['dewPoint'],
                                  'humidity': i['humidity'],
                                  # 'pressure': i['pressure'],
                                  'windSpeed': i['windSpeed'],
                                  'windBearing': i['windBearing'],
                                  'cloudCover': i['cloudCover'],
                                  'uvIndex': i['uvIndex'],
                                  'visibility': i['visibility'],
                                  },
                                 ignore_index=True)

            startdate=startdate+timedelta(hours=24)

        darksky_df.set_index('timeslot', inplace=True)
        return darksky_df

    def merge_dataframe(self):
        generation_df=self.get_ikitelli_generation()
        # darksky_df=self.get_from_darksky_now()
        # merged_inner = pd.merge(left=generation_df, right=darksky_df, left_index=True, right_index=True)
        # print(merged_inner)
    def run(self):
        # self.get_from_darksky()
        # self.get_from_darksky_now()
        # self.get_ikitelli_generation()
        self.merge_dataframe()
        # self.get_from_darksky_now()
Solar_Generation().run()