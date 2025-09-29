#WeatherApp
#Grayson Beamesderfer
#September 19th 2025

from logging import root
from tkinter import *
import tkinter as tk
from tkinter import ttk
import requests
import customtkinter as ctk
import time

class WeatherApp(ctk.CTk):
    global api_key
    api_key = "98265f2c4fbe417589063907251909"
    global base_url
    base_url = "http://api.weatherapi.com/v1"
    global api_call
    api_call = "/current.json?"

    def displayData(self, info):
        if info is None:
            label = ctk.CTkLabel(self, text="City not found.")
            label.pack()
        else:
            name, country, temperature, weather, icon = info
            label = ctk.CTkLabel(self, text=f"City: {name}, {country}\n"
                                 f"Temperature: {temperature}°F\nWeather: {weather}").place(relx=0.5, rely=0.4, anchor=CENTER)
            # You can add code to display the icon if needed

    def displayLoadingBar(self, info):
        label = ctk.CTkLabel(self, text="Loading...", font=ctk.CTkFont(size=20, weight="bold"))
        label.place(relx=0.5, rely=0.4, anchor=CENTER)

        progress = ctk.CTkProgressBar(self, mode = "indeterminate", indeterminate_speed=0.1, width=200, fg_color="#c22121")

        self.after(2000, lambda: [progress.configure(indeterminate_speed=0.4, fg_color="#c2ad21")])
        self.after(5000, lambda: [progress.configure(indeterminate_speed=0.7, fg_color="#67c221"), label.configure(text="Almost there...")])
        
        progress.place(relx=0.5, rely=0.5, anchor=CENTER)
        progress.start()

        self.after(7000, lambda: [progress.stop(), progress.destroy(), label.destroy(), self.displayData(info)])

    def get_info(self, city_name):
        complete_url = base_url + api_call + "key=" + api_key + "&q=" + str(city_name)

        response = requests.get(complete_url)
        data = response.json()
        try:
            name = data["location"]["name"]
            country = data["location"]["country"]
            temperature = data["current"]["temp_f"]
            weather = data["current"]["condition"]["text"]
            icon = data["current"]["condition"]["icon"]

            for widget in self.winfo_children():
                widget.destroy()

            info = [name, country, temperature, weather, icon]
            self.displayLoadingBar(info)
        except KeyError:
            self.entry.delete(0, 'end')
            invalidLabel = ctk.CTkLabel(self, text="City not found. Please try again.", font=ctk.CTkFont(size=12, weight="bold"), text_color="red")
            invalidLabel.place(relx=0.5, rely=0.85, anchor=CENTER)

    def on_press(self, city_name):
        self.get_info(city_name)

    def __init__(self):
        ctk.CTk.__init__(self)

        self.title("Weather App")
        self.geometry("300x250")
        self.resizable(False, False)

        self.root = self

        self.frame = ctk.CTkFrame(master=self.root, height=100, width=100, fg_color="#2174c2")
        self.frame.pack(fill="both", padx=20, pady=10)

        self.title_label = ctk.CTkLabel(master=self.frame, text="Weather App", font=ctk.CTkFont(size=20, weight="bold"), 
                                        text_color="white").pack()

        self.city_label = ctk.CTkLabel(master=self.root, text="Enter City Name:", font=ctk.CTkFont(size=15))
        self.city_label.place(relx=0.5, rely=0.4, anchor=E)

        self.city_name = StringVar()
        self.entry = ctk.CTkEntry(master=self.root, textvariable=self.city_name, width=200, 
                                  corner_radius=10)
        self.entry.place(relx=0.5, rely=0.55, anchor=CENTER)

        self.button = ctk.CTkButton(self.root, text="Get Weather", corner_radius=32, hover_color="#2495ff",
                               command=lambda: self.on_press(self.city_name.get()))
        self.button.place(relx=0.5, rely=0.7, anchor=CENTER)


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
