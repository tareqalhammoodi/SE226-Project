#import necessary libraries
import sys
import requests
import tkinter as tk
from tkinter import *
from lxml import html
from datetime import datetime
from bs4 import BeautifulSoup
from PIL import ImageTk, Image

#functions ------------------------------------------------------------------------------------------------------------------------------------------
#define png file
def getImage(program, path, x, y):
    Icon = ImageTk.PhotoImage(Image.open(path))
    label = Label(program, image = Icon)
    label.image = Icon
    label.place(x = x, y = y)

#get date and time
def getDateTime():
    currentDateTime = datetime.now().strftime("As of " + "%I:%M %p - %Y-%m-%d")
    return currentDateTime

url = "https://www.timeanddate.com/weather/turkey/izmir"

#create function to get weather info from the timeanddate.com
def getWeatherData(e_type, e_class, xPath):
    webPage = requests.get(url)
    if xPath == None:
        return BeautifulSoup(webPage.content, "html.parser").find(e_type, class_= e_class).text
    else: 
        print(html.fromstring(webPage.content).xpath(xPath)[0])
        return html.fromstring(webPage.content).xpath(xPath)[0]

'''
#change themes
def changeTheme(element,color):
'''

#create the GUI -------------------------------------------------------------------------------------------------------------------------------------
program = Tk()
program.geometry("800x450")
program.title("Weather Information Display Program")
program.resizable(False, False)

'''
program.config(bg = "#D49F4A")                                  # Set the background color of the window
screen_bg = program.tk.call("tk", "windowingsystem")            # Get the background color of the screen
'''

#labels
location = Label(program, text = getWeatherData("h1", "headline-banner__title", None), 
                 font = ("Helvetica", 30, "bold"), fg = '#FFFFFF').place(x = 75, y = 30)
dateTime = Label(program, text = getDateTime(), 
                 font = ("Helvetica", 15, "bold"), fg = '#FFFFFF').place(x = 75, y = 70)
temperature = Label(program, text = getWeatherData("div", "h2", None), 
                    font = ("Helvetica", 120, "bold"), fg = '#FFFFFF').place(x = 75, y = 100)
weatherStatus = Label(program, text = getWeatherData(None, None, '//*[@id="qlook"]/p[1]/text()'), 
                      font = ("Helvetica", 20, "bold"), fg = '#FFFFFF',  width = 15, anchor = "e", justify = LEFT).place(x = 535, y = 160)
highloweTemperature = Label(program, text = getWeatherData(None, None, '//*[@id="qlook"]/p[2]/span[1]/text()'), 
                            font = ("Helvetica", 20, "bold"), fg = '#FFFFFF').place(x = 525, y = 190)

visibilityTitle = Label(program, text = "Visibility",  font = ("Helvetica", 18, "normal"), fg = '#FFFFFF').place(x = 140, y = 255)
cloudCoverTitle = Label(program, text = "Cloud Cover", font = ("Helvetica", 18, "normal"), fg = '#FFFFFF').place(x = 140, y = 324)
pressureTitle   = Label(program, text = "Pressure",    font = ("Helvetica", 18, "normal"), fg = '#FFFFFF').place(x = 140, y = 390)
humidityTitle   = Label(program, text = "Humidity",    font = ("Helvetica", 18, "normal"), fg = '#FFFFFF').place(x = 485, y = 255)
windTitle       = Label(program, text = "Wind",        font = ("Helvetica", 18, "normal"), fg = '#FFFFFF').place(x = 485, y = 324)
UVIndexTitle    = Label(program, text = "UV Index",    font = ("Helvetica", 18, "normal"), fg = '#FFFFFF').place(x = 485, y = 390)

visibilityStatus = Label(program, text = getWeatherData(None, None, '/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[4]/td/text()'), font = ("Helvetica", 18, "normal"), fg = '#FFFFFF', width = 8, anchor = "e", justify = LEFT).place(x = 280, y = 255)
cloudCoverStatus = Label(program, text = "None", font = ("Helvetica", 18, "normal"), fg = '#FFFFFF', width = 8, anchor = "e", justify = LEFT).place(x = 280, y = 324)
pressureStatus   = Label(program, text = getWeatherData(None, None, '/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[5]/td/text()'), font = ("Helvetica", 18, "normal"), fg = '#FFFFFF', width = 8, anchor = "e", justify = LEFT).place(x = 280, y = 390)
humidityStatus   = Label(program, text = getWeatherData(None, None, '/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[6]/td/text()'), font = ("Helvetica", 18, "normal"), fg = '#FFFFFF', width = 8, anchor = "e", justify = LEFT).place(x = 625, y = 255)
windStatus       = Label(program, text = getWeatherData(None, None, None), font = ("Helvetica", 18, "normal"), fg = '#FFFFFF', width = 8, anchor = "e", justify = LEFT).place(x = 625, y = 324)
UVIndexStatus    = Label(program, text = "None", font = ("Helvetica", 18, "normal"), fg = '#FFFFFF', width = 8, anchor = "e", justify = LEFT).place(x = 625, y = 390)

#buttons
celsius    = Button(program, text = "C°", font = ("Helvetica", 18, "normal"), fg = "#000000", borderwidth = 0, width = 1, height = 1).place(x = 635, y = 30)
Fahrenheit = Button(program, text = "F°", font = ("Helvetica", 18, "normal"), fg = "#000000", borderwidth = 0, width = 1, height = 1).place(x = 680, y = 30)

#icons
weatherStatusIcon  = getImage(program, "icons/weather-icons/clear.png", 655, 90)
visibilityIcon     = getImage(program, "icons/shared-vision.png", 75, 240)
cloudCoverIcon     = getImage(program, "icons/cloudy-night.png", 75, 308)
pressureIcon       = getImage(program, "icons/resilience.png", 75, 375)
humidityIcon       = getImage(program, "icons/humidity.png", 420, 240)
windIcon           = getImage(program, "icons/wind.png", 420, 308)
UVIndexIcon        = getImage(program, "icons/uv-index.png", 420, 375)

#lines
horizontalLine1 = Frame(program, bg = '#FFFFFF', height = 1, width = 300).place(x = 75, y = 300)
horizontalLine2 = Frame(program, bg = '#FFFFFF', height = 1, width = 300).place(x = 75, y = 370)
horizontalLine3 = Frame(program, bg = '#FFFFFF', height = 1, width = 300).place(x = 420, y = 300)
horizontalLine4 = Frame(program, bg = '#FFFFFF', height = 1, width = 300).place(x = 420, y = 370)

#implementation -------------------------------------------------------------------------------------------------------------------------------------


    

program.mainloop()