import urllib
import requests

# url = 'https://data.ibb.gov.tr/api/3/action/datastore_search?resource_id=52afa9a3-2ea1-420b-a783-505cfe635ece'
# fileobj = requests.get(url,param limit)
# fileobj=fileobj.json()
# print(fileobj)

# importing the requests library
import requests

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

    def get_solar_radiaton_NASA(self):
        URL = "https://api.darksky.net/forecast/992bb820ba82528fffc192c56bf6921e/37.8267,-122.4233"
        r = requests.get(url=URL)
        data = r.json()
        print(data)
    def run(self):
        self.get_solar_radiaton_NASA()

Solar_Generation().run()