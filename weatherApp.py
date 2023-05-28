#import necessary libraries
import sys
import time
import requests
import subprocess
import tkinter as tk
import urllib.request
from tkinter import *
from lxml import html
from datetime import datetime
from bs4 import BeautifulSoup
from PIL import ImageTk, Image
from tkinter import Tk, ttk, messagebox

#define variables
selected_id = ""; selected_unit = ""; selected_city = ""; selected_country = ""; selected_location = "";

#get user preferences from settings.txt file
with open("Settings.txt", 'r') as file:
     for line in file:
          line = line.strip().split() 
          city = line[0][:-1].lower(); country = line[1].lower(); stored_id = int(line[2]); unit = line[3];
          selected_unit = unit; selected_city = city; selected_country = country; selected_id = stored_id;
     file.close()

weatherURL = f"https://www.timeanddate.com/weather/{selected_country}/{selected_city}"
extendedForecastURL = f"https://www.timeanddate.com/weather/{selected_country}/{selected_city}/ext"

#functions ------------------------------------------------------------------------------------------------------------------------------------------
#define png file and get the path
def getImage(path, x, y):
    Icon = ImageTk.PhotoImage(Image.open(path))
    label = Label(program, image = Icon)
    label.image = Icon
    label.place(x = x, y = y)

#function that check internet connection
def connect(host = 'http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

#check if macOS run on dark or light mode
def check_appearance():
   cmd = 'defaults read -g AppleInterfaceStyle'
   p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
   if bool(p.communicate()[0]):
      return "dark"
   else:
      return "light"

#functions that gets weather, date and time info from timeanddate.com
def getWeatherData(e_type, e_class, xPath, URL):
    webPage = requests.get(URL)
    if xPath == None:
        try: 
          return BeautifulSoup(webPage.content, "html.parser").find(e_type, class_= e_class).text
        except Exception as exception:
            print("An error occurred.", str(exception))
            return "0"
    else: 
        try:
          return html.fromstring(webPage.content).xpath(xPath)[0]   
        except Exception as exception:
            print("xpath did not return any elements.", str(exception))
            return "0"

def getTime():
     sunrise = getWeatherData(None, None, '//*[@id="wt-ext"]/tbody/tr[1]/td[11]/text()', extendedForecastURL)
     sunset = getWeatherData(None, None, '//*[@id="wt-ext"]/tbody/tr[1]/td[12]/text()', extendedForecastURL)
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

        cf_Htemp = getWeatherData(None, None, '//*[@id="wt-ext"]/tbody/tr[2]/td[2]/text()', extendedForecastURL)[:-8]
        cf_Ltemp = getWeatherData(None, None, '//*[@id="wt-ext"]/tbody/tr[2]/td[2]/text()', extendedForecastURL)[5:-3]
        cf_Htemp2 = getWeatherData(None, None, '//*[@id="wt-ext"]/tbody/tr[3]/td[2]/text()', extendedForecastURL)[:-8]
        cf_Ltemp2 = getWeatherData(None, None, '//*[@id="wt-ext"]/tbody/tr[3]/td[2]/text()', extendedForecastURL)[5:-3]
        ff_Htemp = ((int(cf_Htemp) * 9/5) + 32); ff_Ltemp = ((int(cf_Ltemp) * 9/5) + 32);
        ff_Htemp2 = ((int(cf_Htemp2) * 9/5) + 32); ff_Ltemp2 = ((int(cf_Ltemp2) * 9/5) + 32);
        if selected_unit == "fahrenheit":
               f_temperature['text'] = "Tomorrow: " + str(ff_Htemp) + " / " + str(ff_Ltemp) + " F°" + "\nAfter tomorrow: " + str(ff_Htemp2) + " / " + str(ff_Ltemp2) + " F°"
        else:
               f_temperature['text'] = "Tomorrow: " + str(cf_Htemp) + " / " + str(cf_Ltemp) + " C°" + "\nAfter tomorrow: " + str(cf_Htemp2) + " / " + str(cf_Ltemp2) + " C°"

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
        windStatus['text'] = 'Expect winds today around ' + getWeatherData(None, None, '//*[@id="wt-ext"]/tbody/tr[1]/td[5]/text()', extendedForecastURL) + ', tomorrow ' + getWeatherData(None, None, '//*[@id="wt-ext"]/tbody/tr[2]/td[5]/text()', extendedForecastURL) + '.'
        humidityStatus['text'] = getWeatherData(None, None, '/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[6]/td/text()', weatherURL)
        
        c_dp = int(getWeatherData(None, None, '/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[7]/td/text()', weatherURL)[:-3])
        f_dp = ((c_dp * 9/5) + 32)
        if selected_unit == "fahrenheit":
               dewPointStatus['text'] = str(f_dp) + " F°"
        else:
               dewPointStatus['text'] = str(c_dp) + " C°"

#droplist actions
def action(event):
     global weatherURL, extendedForecastURL
     c_location = dropList.get().strip().split()
     city       = c_location[0][:-1].lower()
     country    = c_location[1].lower()
     weatherURL = f"https://www.timeanddate.com/weather/{country}/{city}"
     extendedForecastURL = f"https://www.timeanddate.com/weather/{country}/{city}/ext"
     updateData()
     program.update()     
     saveSettings(format(dropList.current()), dropList)

#settings window
def settingsWindow():
     program.withdraw()                                                                                                 #make main window invisible
     window = Toplevel(program)
     window.title("Weather Information Display Program Settings")
     #to put window in the middle of the screen
     app_width  = 800; screen_width  = window.winfo_screenwidth();  x = (screen_width / 2)  - (app_width / 2);
     app_height = 450; screen_height = window.winfo_screenheight(); y = (screen_height / 2) - (app_height / 2);
     window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
     window.resizable(False, False)

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

     def save():
          if (locationDropList.get() == "Ex: Izmir, Türkiye" or unitDropList.get() == "Ex: Celsius"):
               messagebox.showinfo("Error", f"You should select location and unit.")
          else:
               updateData()
               program.update()     
               saveSettings(format(locationDropList.current()), locationDropList)
          
               program.deiconify()                                                                                           #make main window visible
               window.destroy()

     saveButton = Button(window, text = "Save", font = ("Avenir", 16, "normal"), fg = "#000000", borderwidth = 0, width = 4, height = 1, command = save); saveButton.place(x = 375, y = 350);

     #this function handel dark/light mode in macOS system
     def darkLightTheme():
          if check_appearance() == "light" and sys.platform == "darwin":
               labels = [Title, locationTitle, unitTitle]
               for i in range(len(labels)):
                    labels[i]["fg"] = "#000000"
     darkLightTheme()

#refresh data every minute
def refresh():
     updateData()
     program.after(60000, updateData)
     program.update()

#create the GUI -------------------------------------------------------------------------------------------------------------------------------------
program = Tk()
#to put the app in the middle of the screen
app_width  = 800; screen_width  = program.winfo_screenwidth();  x = (screen_width / 2)  - (app_width / 2);
app_height = 450; screen_height = program.winfo_screenheight(); y = (screen_height / 2) - (app_height / 2);
program.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
program.title("Weather Information Display Program")
program.resizable(False, False)
program.iconbitmap("icons/weather_icon.ico")

#check internet conection
if (connect() == False or getWeatherData("div", "h2", None, weatherURL) == "0"):
     messagebox.showinfo("Error", f"There is no internet connection, please make sure you are connected to the internet.")
     program.after(30000, program.destroy())
else:
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
     dropList.place(x = 350, y = 35)

     #labels
     location      = Label(program, font = ("Avenir", 25, "normal"), fg = '#FFFFFF', text = "The cureent weather in :"); location.place(x = 75, y = 30);
     dateTime      = Label(program, font = ("Avenir", 18, "normal"), fg = '#FFFFFF'); dateTime.place(x = 75, y = 60);
     temperature   = Label(program, font = ("Avenir", 80, "bold"), fg = '#FFFFFF'); temperature.place(x = 75, y = 85);
     f_temperature = Label(program, font = ("Avenir", 16, "normal"), fg = '#FFFFFF', anchor = "e", justify = LEFT); f_temperature.place(x = 75, y = 185);
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

     #this function handel dark/light mode in macOS system
     def darkLightTheme():
          if check_appearance() == "light" and sys.platform == "darwin":
               labels = [location, dateTime, temperature, f_temperature, weatherStatus, HLTemperature, visibilityTitle, pressureTitle, windTitle,
                         humidityTitle, dewPointTitle, visibilityStatus, pressureStatus, windStatus, humidityStatus, dewPointStatus]
               for i in range(len(labels)):
                    labels[i]["fg"] = "#000000"

               lines = [horizontalLine1, horizontalLine2, horizontalLine3, horizontalLine4]
               for i in range(len(lines)):
                    lines[i]["bg"] = "#000000"
               
               global visibilityIcon, pressureIcon, windIcon, humidityIcon, dewPointIcon
               visibilityIcon     = getImage("icons/shared-vision-dark.png", 75, 240)
               pressureIcon       = getImage("icons/resilience-dark.png", 75, 308)
               windIcon           = getImage("icons/wind-dark.png", 75, 375)
               humidityIcon       = getImage("icons/humidity-dark.png", 420, 240)
               dewPointIcon       = getImage("icons/drop-dark.png", 420, 308)
    
     darkLightTheme()
     program.mainloop()