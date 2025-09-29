#WeatherApp
#Grayson Beamesderfer
#September 19th 2025

from logging import root
from tkinter import *
import tkinter as tk
import os
import requests
import customtkinter as ctk
import urllib.request
from PIL import Image
import time

class WeatherApp(ctk.CTk):
    global api_key
    api_key = "98265f2c4fbe417589063907251909"
    global base_url
    base_url = "http://api.weatherapi.com/v1"
    global api_call
    api_call = "/current.json?"

    def onClose(self):
        self.clean()
        self.root.destroy()

    def clean(self):
        for widget in self.winfo_children():
            widget.destroy()
        if os.path.exists("Icon\\gfg.png"):
            os.remove("Icon\\gfg.png")

    def displayData(self, info):
        name, country, temperature, weather, icon = info

        urllib.request.urlretrieve(f"http:{icon}", "Icon\\gfg.png")

        if temperature <= 32:
            color = "2174c2"  # Cold color
        elif 32 < temperature <= 70:
            color = "67c221"  # Mild color
        elif 70 < temperature <= 90:
            color = "c2ad21"  # Warm color
        else:
            color = "ba1e1e"  # Hot color

        displayFrame = ctk.CTkFrame(self, height=100, width=100)
        displayFrame.pack(fill="both", padx=20, pady=10, expand=True)

        image = Image.open("Icon\\gfg.png")

        img = ctk.CTkImage(image, size=(100, 100))

        lab = ctk.CTkLabel(displayFrame, image=img, text="")
        lab.place(relx=0.8, rely=0.45, anchor=CENTER)
        lab.image = img #reference for garbage collection

        cityLabel = ctk.CTkLabel(displayFrame, text=f"{name}", font=ctk.CTkFont(size=20, weight="bold"),
                                text_color="white").place(relx=0.5, rely=0.1, anchor=CENTER)
        
        label = ctk.CTkLabel(displayFrame, text_color="white",font=ctk.CTkFont(size=15, weight="bold"), 
                             text=f"Country: {country}").place(relx=0.5, rely=0.2, anchor=CENTER)
        
        tempLabel = ctk.CTkLabel(displayFrame, text = "Temperature: ", font=ctk.CTkFont(size=15, weight="bold"), 
                                 text_color="white").place(relx=0.4, rely=0.4, anchor=E)
        
        temp = ctk.CTkLabel(displayFrame, text=f"{temperature}°F", font=ctk.CTkFont(size=15, weight="bold"),
                            text_color=f"#{color}").place(relx=0.5, rely=0.4, anchor=CENTER)
        
        conditionLabel = ctk.CTkLabel(displayFrame, text="Condition: ", font=ctk.CTkFont(size=15, weight="bold"),
                                    text_color="white").place(relx=0.315, rely=0.6, anchor=E)
        
        condition = ctk.CTkLabel(displayFrame, text=f"{weather}", 
                                 font=ctk.CTkFont(size=15, weight="bold")).place(relx=0.5, rely=0.6, anchor=CENTER)
        
        button = ctk.CTkButton(displayFrame, text="Check Another City", corner_radius=32, hover_color="#2495ff",
                               command=lambda: self.constructHome())
        button.place(relx=0.5, rely=0.8, anchor=CENTER)

    def displayLoadingBar(self, info):
        label = ctk.CTkLabel(self, text="Loading...", font=ctk.CTkFont(size=20, weight="bold"))
        label.place(relx=0.5, rely=0.4, anchor=CENTER)

        progress = ctk.CTkProgressBar(self, mode = "indeterminate", indeterminate_speed=0.1, width=200, fg_color="#c22121")

        self.after(2000, lambda: [progress.configure(indeterminate_speed=0.3, fg_color="#c2ad21")])
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

    def constructHome(self):
        self.clean()
        time.sleep(0.7) #to allow time for cleaning

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

    def __init__(self):
        ctk.CTk.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.onClose)

        self.title("Weather App")
        self.geometry("300x250")
        self.resizable(False, False)

        self.root = self

        self.constructHome()


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
