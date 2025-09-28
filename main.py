#WeatherApp
#Grayson Beamesderfer
#September 19th 2025

from logging import root
from tkinter import *
import tkinter as tk
from tkinter import ttk
import requests
import json

def getInfo(root, city_name):
    api_key = "98265f2c4fbe417589063907251909"
    base_url = "http://api.weatherapi.com/v1"
    api_call = "/current.json?"

    complete_url = base_url + api_call + "key=" + api_key + "&q=" + str(city_name.get())

    response = requests.get(complete_url)
    data = response.json()

    #if data["error"]:                      error handling later, testing will always work
        #print("City not found.")
        #return None
    
    #else:
    name = data["location"]["name"]
    country = data["location"]["country"]
    temperature = data["current"]["temp_f"]
    weather = data["current"]["condition"]["text"]
    icon = data["current"]["condition"]["icon"]

    for widget in root.winfo_children():
        widget.destroy()

    info = [name, country, temperature, weather, icon]

    displayData(info, root)

def displayData(info, root):
    if info is None:
        label = Label(root, text="City not found.")
        label.pack()
    else:
        name, country, temperature, weather, icon = info
        label = Label(root, text=f"City: {name}, {country}\nTemperature: {temperature}°F\nWeather: {weather}")
        label.pack()
        # You can add code to display the icon if needed

def main():
    # Display the weather information in a GUI window
    root = tk.Tk()

    root.title("Weather App")
    root.geometry("300x200")

    frame = Frame(root, bg="white", highlightbackground="black", highlightthickness=2)
    frame.place(relwidth=1, relheight=1, relx=0.5, rely=0.5, anchor=CENTER)

    city_name = tk.StringVar()

    entry = ttk.Entry(frame, textvariable=city_name)
    entry.grid(row=0, column=0)

    button = ttk.Button(frame, text="Get Weather", command=lambda: getInfo(root, city_name))
    button.grid(row=3, column=2)

    root.mainloop()

if __name__ == "__main__":
    main()
