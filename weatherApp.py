#import necessary libraries
import sys
import requests
import tkinter as tk
from tkinter import *
from bs4 import BeautifulSoup
from PIL import ImageTk, Image

'''
#linear-gradient color function
def createLinearGradient(color1, color2, width, height):
    gradient = tk.Canvas(width = width, height = height)
    for i in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * i / height)
        g = int(color1[1] + (color2[1] - color1[1]) * i / height)
        b = int(color1[2] + (color2[2] - color1[2]) * i / height)
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        gradient.create_line(0, i, width, i + 1, fill = hex_color, width = 1)
    return gradient
'''

#define png file
def getImage(program, path, x, y):
    Icon = ImageTk.PhotoImage(Image.open(path))
    label = Label(program, image = Icon)
    label.image = Icon
    label.place(x = x, y = y)

'''
#change themes
def changeTheme(element,color):
'''

#create the GUI
program = Tk()
program.geometry("800x450")
program.title("Weather Information Display Program")
program.config(bg = "#D49F4A")
program.resizable(False, False)
'''

#background color
color1 = (33, 92, 178)    # Starting color (red)
color2 = (127, 187, 236)  # Ending color   (blue)
gradient = createLinearGradient(color1, color2, 800, 450)
gradient.pack()
'''

#labels
location = Label(program, text = "Izmir, Türkiye Weather", font = ("Helvetica", 30, "bold"), fg = '#FFFFFF').place(x = 75, y = 30)
time = Label(program, text = "As of 4:15 am GMT +03:00", font = ("Helvetica", 15, "bold"), fg = '#FFFFFF').place(x = 75, y = 70)
temperature = Label(program, text = "16°", font = ("Helvetica", 120, "bold"), fg = '#FFFFFF').place(x = 75, y = 100)
weatherStatus = Label(program, text = "Partly Cloudy°", font = ("Helvetica", 20, "bold"), fg = '#FFFFFF').place(x = 575, y = 160)
highestTemperature = Label(program, text = "H:22°", font = ("Helvetica", 20, "bold"), fg = '#FFFFFF').place(x = 575, y = 190)
lowestTemperature = Label(program, text = "L:13°", font = ("Helvetica", 20, "bold"), fg = '#FFFFFF').place(x = 640, y = 190)

visibilityTitle = Label(program, text = "Visibility", font = ("Helvetica", 18, "normal"), fg = '#FFFFFF').place(x = 140, y = 255)
cloudCoverTitle  = Label(program, text = "Cloud Cover", font = ("Helvetica", 18, "normal"), fg = '#FFFFFF').place(x = 140, y = 324)
pressureTitle   = Label(program, text = "Pressure", font = ("Helvetica", 18, "normal"), fg = '#FFFFFF').place(x = 140, y = 390)
humidityTitle   = Label(program, text = "Humidity", font = ("Helvetica", 18, "normal"), fg = '#FFFFFF').place(x = 485, y = 255)
windTitle       = Label(program, text = "Wind", font = ("Helvetica", 18, "normal"), fg = '#FFFFFF').place(x = 485, y = 324)
UVIndexTitle    = Label(program, text = "UV Index", font = ("Helvetica", 18, "normal"), fg = '#FFFFFF').place(x = 485, y = 390)

#icons
visibilityIcon  = getImage(program, "icons/shared-vision.png", 75, 240)
cloudCoverIcon  = getImage(program, "icons/cloudy-night.png", 75, 308)
pressureIcon    = getImage(program, "icons/resilience.png", 75, 375)
humidityIcon    = getImage(program, "icons/humidity.png", 420, 240)
windIcon        = getImage(program, "icons/wind.png", 420, 308)
UVIndexIcon     = getImage(program, "icons/uv-index.png", 420, 375)

#lines
horizontalLine1 = Frame(program, bg = '#FFFFFF', height = 1, width = 300).place(x = 75, y = 300)
horizontalLine2 = Frame(program, bg = '#FFFFFF', height = 1, width = 300).place(x = 75, y = 370)
horizontalLine3 = Frame(program, bg = '#FFFFFF', height = 1, width = 300).place(x = 420, y = 300)
horizontalLine4 = Frame(program, bg = '#FFFFFF', height = 1, width = 300).place(x = 420, y = 370)

#create function to get weather info from the accuweather.com
def getWeatherData(countryID, cityName, cityCode):
    url = "https://www.accuweather.com/en/tr/izmir/318290/current-weather/318290"

program.mainloop()