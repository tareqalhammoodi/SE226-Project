#import necessary libraries
import sys
import time
import requests
import tkinter as tk
from tkinter import *
from lxml import html
from datetime import datetime
from bs4 import BeautifulSoup
from PIL import ImageTk, Image

#functions ------------------------------------------------------------------------------------------------------------------------------------------
#define png file
def getImage(path, x, y):
    Icon = ImageTk.PhotoImage(Image.open(path))
    label = Label(program, image = Icon)
    label.image = Icon
    label.place(x = x, y = y)

#get date and time
def getDateTime():
    currentDateTime = datetime.now().strftime("As of " + "%I:%M %p - %Y|%m|%d")
    return currentDateTime

country    = 'turkey'
city       = 'izmir'
weatherURL = f"https://www.timeanddate.com/weather/{country}/{city}"
windURL    = f'https://www.timeanddate.com/weather/{country}/{city}/ext'

#create function that gets weather info from timeanddate.com
def getWeatherData(e_type, e_class, xPath, URL):
    webPage = requests.get(URL)
    if xPath == None:
        return BeautifulSoup(webPage.content, "html.parser").find(e_type, class_= e_class).text
    else: 
        return html.fromstring(webPage.content).xpath(xPath)[0]    

#create function that keeps data updated
def updateData():
        location['text']      = getWeatherData("h1", "headline-banner__title", None, weatherURL)
        dateTime['text']      = getDateTime()
        temperature['text']   = getWeatherData("div", "h2", None, weatherURL)
        weatherStatus['text'] = getWeatherData(None, None, '//*[@id="qlook"]/p[1]/text()', weatherURL)[:-1]
        HLTemperature['text'] = getWeatherData(None, None, '//*[@id="qlook"]/p[2]/span[1]/text()', weatherURL)[10:]

        visibilityStatus['text'] = getWeatherData(None, None, '/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[4]/td/text()', weatherURL)
        pressureStatus['text']   = getWeatherData(None, None, '/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[5]/td/text()', weatherURL)
        windStatus['text']       = 'Expect winds today around ' + getWeatherData(None, None, '//*[@id="wt-ext"]/tbody/tr[1]/td[5]/text()', windURL) + ', tomorrow ' + getWeatherData(None, None, '//*[@id="wt-ext"]/tbody/tr[2]/td[5]/text()', windURL) + '.'
        humidityStatus['text']   = getWeatherData(None, None, '/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[6]/td/text()', weatherURL)
        dewPointStatus['text']   = getWeatherData(None, None, '/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[7]/td/text()', weatherURL)

        location.after(60000, updateData)
        program.update()

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
location      = Label(program, font = ("Helvetica", 30, "bold"), fg = '#FFFFFF'); location.place(x = 75, y = 30);
dateTime      = Label(program, font = ("Helvetica", 15, "bold"), fg = '#FFFFFF'); dateTime.place(x = 75, y = 70);
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
Fahrenheit = Button(program, text = "F°", font = ("Helvetica", 18, "normal"), fg = "#000000", borderwidth = 0, width = 1, height = 1); Fahrenheit.place(x = 680, y = 30);

#icons
weatherStatusIcon  = getImage("icons/weather-icons/clear.png", 655, 90)
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

updateData()
program.mainloop()