#import necessary libraries
import sys
import time
import requests
import tkinter as tk
from tkinter import Tk, ttk
from tkinter import *
from lxml import html
from datetime import datetime
from bs4 import BeautifulSoup
from PIL import ImageTk, Image

weatherURL = f"https://www.timeanddate.com/weather/turkey/izmir"
windURL    = f"https://www.timeanddate.com/weather/turkey/izmir/ext"

#functions ------------------------------------------------------------------------------------------------------------------------------------------
#define png file
def getImage(path, x, y):
    Icon = ImageTk.PhotoImage(Image.open(path))
    label = Label(program, image = Icon)
    label.image = Icon
    label.place(x = x, y = y)

#functions that gets weather info from timeanddate.com, date and time.
def getWeatherData(e_type, e_class, xPath, URL):
    webPage = requests.get(URL)
    if xPath == None:
        return BeautifulSoup(webPage.content, "html.parser").find(e_type, class_= e_class).text
    else: 
        return html.fromstring(webPage.content).xpath(xPath)[0]   

def getTime():
     sunrise = getWeatherData(None, None, '//*[@id="wt-ext"]/tbody/tr[1]/td[11]/text()', windURL)
     sunset = getWeatherData(None, None, '//*[@id="wt-ext"]/tbody/tr[1]/td[12]/text()', windURL)
     currentTime = datetime.now().strftime("%H:%M")
     if currentTime >= sunset or currentTime <= sunrise:
        return "night"
     else:
        return "morning" 
     
def getWeatherIcon(weatherStatus):
     if   ((weatherStatus == "Scattered clouds") or (weatherStatus == "Passing clouds") or (weatherStatus == "Broken clouds") or (weatherStatus == "Partly sunny") or (weatherStatus == "Partly sunny")) and (getTime() == "morning"):
          path = "icons/weather-icons/partly-cloudy.png"  
     elif ((weatherStatus == "Scattered clouds") or (weatherStatus == "Passing clouds") or (weatherStatus == "Broken clouds") or (weatherStatus == "Partly cloudy")) and (getTime() == "night"):
          path = "icons/weather-icons/partly-cloudy(night).png" 
     elif ((weatherStatus == "Sunny") or (weatherStatus == "Clear") or (weatherStatus == "Mostly Clear")) and (getTime() == "morning"):
          path = "icons/weather-icons/clear.png" 
     elif ((weatherStatus == "Mostly Clear") or (weatherStatus == "Clear")) and (getTime() == "night"):
          path = "icons/weather-icons/clear(night).png" 
     elif ((weatherStatus == "Thunderstorms") or (weatherStatus == "Light rain") or (weatherStatus == "Scattered showers") or (weatherStatus == "Rain") or (weatherStatus == "Passing showers")) and (getTime() == "morning"):
          path = "icons/weather-icons/rain.png" 
     elif ((weatherStatus == "Thunderstorms") or (weatherStatus == "Light rain") or (weatherStatus == "Scattered showers") or (weatherStatus == "Rain") or (weatherStatus == "Passing showers")) and (getTime() == "night"):
          path = "icons/weather-icons/rain(night).png" 
     elif ((weatherStatus == "Snow flurries") or (weatherStatus == "Extremely cold") or (weatherStatus == "Snow")):
          path = "icons/weather-icons/snow.png" 
     else: path = "icons/weather-icons/error.png" 
     return path
        
def getDateTime():
    currentDateTime = datetime.now().strftime("As of " + "%I:%M %p - %Y|%m|%d")
    return currentDateTime

#create function that keeps data updated
def updateData():
        #location['text']      = getWeatherData("h1", "headline-banner__title", None, weatherURL)
        dateTime['text']      = getDateTime()
        temperature['text']   = getWeatherData("div", "h2", None, weatherURL)
        weatherStatus['text'] = getWeatherData(None, None, '//*[@id="qlook"]/p[1]/text()', weatherURL)[:-1]
        HLTemperature['text'] = getWeatherData(None, None, '//*[@id="qlook"]/p[2]/span[1]/text()', weatherURL)[10:]

        visibilityStatus['text'] = getWeatherData(None, None, '/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[4]/td/text()', weatherURL)
        pressureStatus['text']   = getWeatherData(None, None, '/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[5]/td/text()', weatherURL)
        windStatus['text']       = 'Expect winds today around ' + getWeatherData(None, None, '//*[@id="wt-ext"]/tbody/tr[1]/td[5]/text()', windURL) + ', tomorrow ' + getWeatherData(None, None, '//*[@id="wt-ext"]/tbody/tr[2]/td[5]/text()', windURL) + '.'
        humidityStatus['text']   = getWeatherData(None, None, '/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[6]/td/text()', weatherURL)
        dewPointStatus['text']   = getWeatherData(None, None, '/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[7]/td/text()', weatherURL)

#droplist action
def click(event):
     global weatherURL, windURL
     c_location = dropList.get().strip().split()
     city       = c_location[0][:-1].lower()
     country    = c_location[1].lower()
     weatherURL = f"https://www.timeanddate.com/weather/{country}/{city}"
     windURL    = f"https://www.timeanddate.com/weather/{country}/{city}/ext"
     updateData()
     program.update()     

#refresh data every minute
def refresh():
     updateData()
     program.after(60000, updateData)
     program.update()


'''
#change themes
def changeTheme(element,color):
'''
'''
program.config(bg = "#D49F4A")                                  # Set the background color of the window
screen_bg = program.tk.call("tk", "windowingsystem")            # Get the background color of the screen
'''

#create the GUI -------------------------------------------------------------------------------------------------------------------------------------
program = Tk()
program.geometry("800x450")
program.title("Weather Information Display Program")
program.resizable(False, False)

#dropdown menu
options = []
with open("world.txt", 'r') as file:
     for line in file:
          line = line.strip().split()
          city = line[0][:-1]
          country = line[1]
          location = f"{city}, {country}"
          options.append(location)

dropList = ttk.Combobox(program, value = options, width = 15)
dropList.current(0)
dropList.bind("<<ComboboxSelected>>", click)
dropList.configure(font = ("Helvetica", 22))
dropList.place(x = 350, y = 30)

#labels
location      = Label(program, font = ("Helvetica", 25, "normal"), fg = '#FFFFFF', text = "The cureent weather in :"); location.place(x = 75, y = 30);
dateTime      = Label(program, font = ("Helvetica", 18, "normal"), fg = '#FFFFFF'); dateTime.place(x = 75, y = 60);
temperature   = Label(program, font = ("Helvetica", 120, "bold"), fg = '#FFFFFF'); temperature.place(x = 75, y = 100);
weatherStatus = Label(program, font = ("Helvetica", 20, "bold"), fg = '#FFFFFF',  width = 15, anchor = "e", justify = LEFT); weatherStatus.place(x = 535, y = 160);
HLTemperature = Label(program, font = ("Helvetica", 20, "bold"), fg = '#FFFFFF'); HLTemperature.place(x = 625, y = 190);

visibilityTitle = Label(program, text = "Visibility",  font = ("Helvetica", 18, "normal"), fg = '#FFFFFF'); visibilityTitle.place(x = 140, y = 255);
pressureTitle   = Label(program, text = "Pressure",    font = ("Helvetica", 18, "normal"), fg = '#FFFFFF'); pressureTitle.place(x = 140, y = 324);
windTitle       = Label(program, text = "Wind Speed:", font = ("Helvetica", 18, "normal"), fg = '#FFFFFF'); windTitle.place(x = 140, y = 390);
humidityTitle   = Label(program, text = "Humidity",    font = ("Helvetica", 18, "normal"), fg = '#FFFFFF'); humidityTitle.place(x = 485, y = 255);
dewPointTitle   = Label(program, text = "Dew Point",   font = ("Helvetica", 18, "normal"), fg = '#FFFFFF'); dewPointTitle.place(x = 485, y = 324);

visibilityStatus = Label(program, font = ("Helvetica", 18, "normal"), fg = '#FFFFFF', width = 8, anchor = "e", justify = LEFT); visibilityStatus.place(x = 280, y = 255);
pressureStatus   = Label(program, font = ("Helvetica", 18, "normal"), fg = '#FFFFFF', width = 8, anchor = "e", justify = LEFT); pressureStatus.place(x = 280, y = 324);
windStatus       = Label(program, font = ("Helvetica", 18, "normal"), fg = '#FFFFFF');                                          windStatus.place(x = 255, y = 390);
humidityStatus   = Label(program, font = ("Helvetica", 18, "normal"), fg = '#FFFFFF', width = 8, anchor = "e", justify = LEFT); humidityStatus.place(x = 625, y = 255);
dewPointStatus   = Label(program, font = ("Helvetica", 18, "normal"), fg = '#FFFFFF', width = 8, anchor = "e", justify = LEFT); dewPointStatus.place(x = 625, y = 324);

#buttons
celsius    = Button(program, text = "C°", font = ("Helvetica", 18, "normal"), fg = "#000000", borderwidth = 0, width = 1, height = 1); celsius.place(x = 635, y = 30);
fahrenheit = Button(program, text = "F°", font = ("Helvetica", 18, "normal"), fg = "#000000", borderwidth = 0, width = 1, height = 1); fahrenheit.place(x = 680, y = 30);

refresh()

#icons
weatherStatusIcon  = getImage(getWeatherIcon(weatherStatus['text']), 655, 90)
visibilityIcon     = getImage("icons/shared-vision.png", 75, 240)
pressureIcon       = getImage("icons/resilience.png", 75, 308)
windIcon           = getImage("icons/wind.png", 75, 375)
humidityIcon       = getImage("icons/humidity.png", 420, 240)
dewPointIcon       = getImage("icons/drop.png", 420, 308)

#lines
horizontalLine1 = Frame(program, bg = '#FFFFFF', height = 1, width = 300); horizontalLine1.place(x = 75, y = 300);
horizontalLine2 = Frame(program, bg = '#FFFFFF', height = 1, width = 300); horizontalLine2.place(x = 75, y = 370);
horizontalLine3 = Frame(program, bg = '#FFFFFF', height = 1, width = 300); horizontalLine3.place(x = 420, y = 300);
horizontalLine4 = Frame(program, bg = '#FFFFFF', height = 1, width = 300); horizontalLine4.place(x = 420, y = 370);

#implementation -------------------------------------------------------------------------------------------------------------------------------------
program.mainloop()