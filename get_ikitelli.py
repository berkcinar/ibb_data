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
import os.path
import numpy
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
            # generation_df = generation_df.append({'timeslot': dt.strptime(i['Tarih'].replace("T", " ")[:13] + ':00:00', '%Y-%m-%d %H:%M:%S'),'uretim': i['Uretim (kWh)'],},ignore_index=True)
            generation_df = generation_df.append({'timeslot': dt.strptime(i['Tarih'].replace("T", " "), '%Y-%m-%d %H:%M:%S'),'uretim': i['Uretim (kWh)'],},ignore_index=True)
            # df2 = df2.append({'timeslot': dt.fromtimestamp((i['Tarih']).strftime('%Y-%m-%d %H:%M:%S')),'uretim': i['Uretim (kWh)'],},ignore_index=True)

        #eksik değerleri tamamlamam lazım.
        print(generation_df)
        # generation_df=self.check_and_fill_zeros(generation_df)
        generation_df.set_index('timeslot', inplace=True)

        generation_df=generation_df.groupby('timeslot').mean()
        # generation_df=generation_df.groupby(pd.TimeGrouper(freq='15Min')).aggregate(numpy.sum)
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
        # enddate = dt(2019,5,2)
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

        # darksky_df.set_index('timeslot', inplace=True)
        darksky_df.to_csv('darksky.csv', sep=',', encoding='utf-8',header='true')
        return darksky_df

    def csv_to_df(self):

        darksky_pd = pd.read_csv("darksky.csv",encoding='utf-8')
        darksky_pd.set_index('timeslot', inplace=True)
        return darksky_pd

    def merge_dataframe(self):
        generation_df=self.get_ikitelli_generation()
        if os.path.isfile('darksky.csv'):
            print("File exist")
            darksky_df = self.csv_to_df()
        else:
            print("File not exist")
            darksky_df = self.get_from_darksky_now()

        merged_inner = pd.merge(left=generation_df, right=darksky_df, left_index=True, right_index=True)
        merged_inner.to_csv('merged_inner.csv', sep=',', encoding='utf-8', header='true')


    def check_and_fill_zeros(self,generation_df):
        liste = pd.DataFrame()
        print(generation_df['timeslot'])

        print(generation_df['timeslot'].iloc[0],generation_df['timeslot'].iloc[-1])


        startdate=generation_df['timeslot'].iloc[0] - timedelta(hours=generation_df['timeslot'].iloc[0].hour, minutes=generation_df['timeslot'].iloc[0].minute)

        enddate=generation_df['timeslot'].iloc[-1]-timedelta(hours=generation_df['timeslot'].iloc[-1].hour,minutes=generation_df['timeslot'].iloc[-1].minute)

        print(startdate,enddate)

        idx = pd.date_range(startdate, periods=(enddate+timedelta(hours=1)-startdate).total_seconds()*4/3600, freq='15Min')

        for timeslot in idx:
            if timeslot in generation_df.values:
                pass
            else:
                generation_df=generation_df.append({'timeslot': timeslot,'uretim': 0 }, ignore_index=True)


        generation_df.sort_values("timeslot", axis=0, ascending=True,
                         inplace=True, na_position='first')

        return generation_df


    def run(self):
        # self.get_from_darksky()
        # self.get_from_darksky_now()
        self.get_ikitelli_generation()
        # self.get_from_darksky_now()
        # self.merge_dataframe()
        # self.csv_to_df()
        # self.get_from_darksky_now()
        # self.check_and_fill_zeros()
Solar_Generation().run()
