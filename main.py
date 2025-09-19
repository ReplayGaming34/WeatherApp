# WeatherApp
#Grayson Beamesderfer
#September 19th 2025

import tkinter as tk
import requests
import json

def main():
    api_key = "98265f2c4fbe417589063907251909"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    city_name = input("Enter city name: ")
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    response = requests.get(complete_url)
    data = response.json()

    print(data)

    if data["cod"] != "404":
        y = data["main"]

        current_temperature = y["temp"]
       
        current_humidity = y["humidity"]

        z = data["weather"]

        weather_description = z[0]["description"]

        print(" Temperature (in kelvin unit) = " +
            str(current_temperature) + 

        "\n humidity (in percentage) = " +
            str(current_humidity) +

        "\n description = " +
            str(weather_description))

    else:
        print(" City Not Found ")


if __name__ == "__main__":
    main()
