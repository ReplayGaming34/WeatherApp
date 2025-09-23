#WeatherApp
#Grayson Beamesderfer
#September 19th 2025

import tkinter as tk
import requests
import json

def main():
    api_key = "98265f2c4fbe417589063907251909"
    base_url = "http://api.weatherapi.com/v1"
    api_call = "/current.json?"

    city_name = input("Enter city name: ")
    complete_url = base_url + api_call + "key=" + api_key + "&q=" + city_name

    response = requests.get(complete_url)
    data = response.json()


    print(data)

if __name__ == "__main__":
    main()
