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

#define variables
selected_id = ""
selected_unit = ""
selected_city = ""
selected_country = ""
selected_location = ""

#get user preferences from settings.txt file
with open("Settings.txt", 'r') as file:
     for line in file:
          line = line.strip().split() 
          city = line[0][:-1].lower(); country = line[1].lower(); stored_id = int(line[2]); unit = line[3];
          selected_unit = unit; selected_city = city; selected_country = country; selected_id = stored_id;
     file.close()

weatherURL = f"https://www.timeanddate.com/weather/{selected_country}/{selected_city}"
windURL    = f"https://www.timeanddate.com/weather/{selected_country}/{selected_city}/ext"

#functions ------------------------------------------------------------------------------------------------------------------------------------------
#define png file
def getImage(path, x, y):
    Icon = ImageTk.PhotoImage(Image.open(path))
    label = Label(program, image = Icon)
    label.image = Icon
    label.place(x = x, y = y)

#functions that gets weather, date and time info from timeanddate.com
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

#function that save user preferences to settings.txt file
def saveSettings(ID, list):
     with open("Settings.txt", 'w+') as file:
          #file.truncate(0)
          c_location = list.get().strip().split()
          city       = c_location[0][:-1].lower()
          country    = c_location[1].lower()
          data = (city + ", " + country + " " + ID + " " + selected_unit)
          file.writelines(data)
          file.close()

#function that keeps data updated
def updateData():
        dateTime['text'] = getDateTime()

        c_temp = int(getWeatherData("div", "h2", None, weatherURL)[:-3])
        f_temp = ((c_temp * 9/5) + 32)
        if selected_unit == "fahrenheit":
               temperature['text'] = str(f_temp) + " F°"
        else:
               temperature['text'] = str(c_temp) + " C°"
               
        weatherStatus['text'] = getWeatherData(None, None, '//*[@id="qlook"]/p[1]/text()', weatherURL)[:-1]

        c_Htemp = int(getWeatherData(None, None, '//*[@id="qlook"]/p[2]/span[1]/text()', weatherURL)[10:-7])
        c_Ltemp = int(getWeatherData(None, None, '//*[@id="qlook"]/p[2]/span[1]/text()', weatherURL)[15:-3])
        f_Htemp = ((c_Htemp * 9/5) + 32); f_Ltemp = ((c_Ltemp * 9/5) + 32);
        if selected_unit == "fahrenheit":
               HLTemperature['text'] = str(f_Htemp) + " / " + str(f_Ltemp) + " F°"
        else:
               HLTemperature['text'] = str(c_Htemp) + " / " + str(c_Ltemp) + " C°"

        visibilityStatus['text'] = getWeatherData(None, None, '/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[4]/td/text()', weatherURL)
        pressureStatus['text'] = getWeatherData(None, None, '/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[5]/td/text()', weatherURL)
        windStatus['text'] = 'Expect winds today around ' + getWeatherData(None, None, '//*[@id="wt-ext"]/tbody/tr[1]/td[5]/text()', windURL) + ', tomorrow ' + getWeatherData(None, None, '//*[@id="wt-ext"]/tbody/tr[2]/td[5]/text()', windURL) + '.'
        humidityStatus['text'] = getWeatherData(None, None, '/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[6]/td/text()', weatherURL)
        
        c_dp = int(getWeatherData(None, None, '/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[7]/td/text()', weatherURL)[:-3])
        f_dp = ((c_dp * 9/5) + 32)
        if selected_unit == "fahrenheit":
               dewPointStatus['text'] = str(f_dp) + " F°"
        else:
               dewPointStatus['text'] = str(c_dp) + " C°"

#droplist actions
def action(event):
     global weatherURL, windURL
     c_location = dropList.get().strip().split()
     city       = c_location[0][:-1].lower()
     country    = c_location[1].lower()
     weatherURL = f"https://www.timeanddate.com/weather/{country}/{city}"
     windURL    = f"https://www.timeanddate.com/weather/{country}/{city}/ext"
     updateData()
     program.update()     
     saveSettings(format(dropList.current()), dropList)

#settings window
def settingsWindow():
     program.withdraw()                                                                                                 #make main window invisible
     window = Toplevel(program)
     window.title("Weather Information Display Program Settings")
     window.geometry("800x450")

     def l_action(event):
          global selected_city, selected_country, selected_id
          c_location       = locationDropList.get().strip().split()
          city             = c_location[0][:-1].lower()
          country          = c_location[1].lower()
          l_ID             = format(locationDropList.current())
          selected_city    = city
          selected_country = country
          selected_id      = l_ID

     def u_action(event):
          global selected_unit
          selected_unit = unitDropList.get()

     def save():
          updateData()
          program.update()     
          saveSettings(format(locationDropList.current()), locationDropList)
          
          program.deiconify()                                                                                           #make main window visible
          window.destroy()

     Title = Label(window, font = ("Avenir", 25, "normal"), fg = '#FFFFFF', text = "Weather Information Display Program"); Title.place(x = 200, y = 55);
     locationTitle = Label(window, font = ("Avenir", 20, "normal"), fg = '#FFFFFF', text = "Select location:"); locationTitle.place(x = 200, y = 140);
     #location dropdown menu
     options = []
     with open("world.txt", 'r') as file:
          for line in file:
               line = line.strip().split()
               city = line[0][:-1]
               country = line[1]
               location = f"{city}, {country}"
               options.append(location)
          file.close()
     locationDropList = ttk.Combobox(window, value = options, width = 33)
     locationDropList.set("Ex: Izmir, Türkiye")
     locationDropList.bind("<<ComboboxSelected>>", l_action)
     locationDropList.configure(font = ("Avenir", 20))
     locationDropList.place(x = 200, y = 170)

     unitTitle = Label(window, font = ("Avenir", 20, "normal"), fg = '#FFFFFF', text = "Temperature Unite:"); unitTitle.place(x = 200, y = 220);
     #unit dropdown menu
     units = ["celsius", "fahrenheit"]
     unitDropList = ttk.Combobox(window, value = units, width = 33)
     unitDropList.set("Ex: Celsius")
     unitDropList.bind("<<ComboboxSelected>>", u_action)
     unitDropList.configure(font = ("Avenir", 20))
     unitDropList.place(x = 200, y = 250)

     saveButton = Button(window, text = "Save", font = ("Avenir", 16, "normal"), fg = "#000000", borderwidth = 0, width = 4, height = 1, command = save); saveButton.place(x = 375, y = 350);

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

#run setting window only once
with open('run.txt', 'r') as file :
          code = file.read()
          if code == "on":
               settingsWindow()
          code = code.replace('on', 'off')
with open('run.txt', 'w') as file:
          file.write(code)
                                                                                                   

#dropdown menu
options = []
with open("world.txt", 'r') as file:
     for line in file:
          line = line.strip().split()
          city = line[0][:-1]
          country = line[1]
          location = f"{city}, {country}"
          options.append(location)
     file.close()
dropList = ttk.Combobox(program, value = options, width = 15)
dropList.set(options[selected_id])
dropList.bind("<<ComboboxSelected>>", action)
dropList.configure(font = ("Avenir", 20))
dropList.place(x = 350, y = 30)

#labels
location      = Label(program, font = ("Avenir", 25, "normal"), fg = '#FFFFFF', text = "The cureent weather in :"); location.place(x = 75, y = 30);
dateTime      = Label(program, font = ("Avenir", 18, "normal"), fg = '#FFFFFF'); dateTime.place(x = 75, y = 60);
temperature   = Label(program, font = ("Avenir", 100, "bold"), fg = '#FFFFFF'); temperature.place(x = 75, y = 100);
weatherStatus = Label(program, font = ("Avenir", 20, "bold"), fg = '#FFFFFF',  width = 15, anchor = "e", justify = LEFT); weatherStatus.place(x = 535, y = 160);
HLTemperature = Label(program, font = ("Avenir", 20, "bold"), fg = '#FFFFFF', width = 15, anchor = "e", justify = LEFT); HLTemperature.place(x = 535, y = 190);

visibilityTitle = Label(program, text = "Visibility",  font = ("Avenir", 18, "normal"), fg = '#FFFFFF'); visibilityTitle.place(x = 140, y = 255);
pressureTitle   = Label(program, text = "Pressure",    font = ("Avenir", 18, "normal"), fg = '#FFFFFF'); pressureTitle.place(x = 140, y = 324);
windTitle       = Label(program, text = "Wind Speed:", font = ("Avenir", 18, "normal"), fg = '#FFFFFF'); windTitle.place(x = 140, y = 390);
humidityTitle   = Label(program, text = "Humidity",    font = ("Avenir", 18, "normal"), fg = '#FFFFFF'); humidityTitle.place(x = 485, y = 255);
dewPointTitle   = Label(program, text = "Dew Point",   font = ("Avenir", 18, "normal"), fg = '#FFFFFF'); dewPointTitle.place(x = 485, y = 324);

visibilityStatus = Label(program, font = ("Avenir", 18, "normal"), fg = '#FFFFFF', width = 8, anchor = "e", justify = LEFT); visibilityStatus.place(x = 280, y = 255);
pressureStatus   = Label(program, font = ("Avenir", 18, "normal"), fg = '#FFFFFF', width = 8, anchor = "e", justify = LEFT); pressureStatus.place(x = 280, y = 324);
windStatus       = Label(program, font = ("Avenir", 18, "normal"), fg = '#FFFFFF');                                          windStatus.place(x = 255, y = 390);
humidityStatus   = Label(program, font = ("Avenir", 18, "normal"), fg = '#FFFFFF', width = 8, anchor = "e", justify = LEFT); humidityStatus.place(x = 625, y = 255);
dewPointStatus   = Label(program, font = ("Avenir", 18, "normal"), fg = '#FFFFFF', width = 8, anchor = "e", justify = LEFT); dewPointStatus.place(x = 625, y = 324);

#functions that change units
def changetoC():
     global selected_unit
     selected_unit = "celsius"
     celsius['state'] = DISABLED
     fahrenheit['state'] = NORMAL
     with open('Settings.txt', 'r') as file :
          new_data = file.read()
          new_data = new_data.replace('fahrenheit', 'celsius')
     with open('Settings.txt', 'w') as file:
          file.write(new_data)
     updateData()

def changetoF():
     global selected_unit
     selected_unit = "fahrenheit"
     celsius['state'] = NORMAL
     fahrenheit['state'] = DISABLED
     with open('Settings.txt', 'r') as file :
          new_data = file.read()
          new_data = new_data.replace('celsius', 'fahrenheit')
     with open('Settings.txt', 'w') as file:
          file.write(new_data)
     updateData()
     
#buttons
celsius    = Button(program, text = "C°", font = ("Avenir", 18, "normal"), fg = "#000000", borderwidth = 0, width = 1, height = 1, command = changetoC); celsius.place(x = 635, y = 30);
fahrenheit = Button(program, text = "F°", font = ("Avenir", 18, "normal"), fg = "#000000", borderwidth = 0, width = 1, height = 1, command = changetoF); fahrenheit.place(x = 680, y = 30);

if selected_unit == "fahrenheit":
     fahrenheit['state'] = DISABLED
     celsius['state'] = NORMAL
else:
     fahrenheit['state'] = NORMAL
     celsius['state'] = DISABLED

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

program.mainloop()