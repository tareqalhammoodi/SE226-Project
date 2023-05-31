# SE226-Project
<b>SE226 - Advanced Programming Final project, Izmir University of Economics 2023 spring semester</b>

<b>Project Title:</b> Weather Information Display Program

<b>Project Description:</b> Create a weather information displaying program with a graphical user interface (GUI) using Python. The program will allow users to select a city from a `dropdown list` and display the weather information for the chosen city. The weather data will be gathered from the internet using the `“requests”` and `“beautifulsoup4”` modules. Python data structures will be utilized to store and present the weather data. Additionally, the program will include a button to toggle between `Celsius` and `Fahrenheit` temperature units. It will also implement functionality to save and load user preferences, including the selected city and temperature unit, from a `Settings.txt` file.

## Tasks:
## GUI Development
1. Use Tkinter or any other suitable GUI library to create the graphical interface for the program.
2. Design and implement a dropdown list to allow users to select a city.
3. Create an area in the GUI to display the weather information.

## Retrieve Weather Data
1. Utilize the `“requests”` library to send HTTP requests and fetch the weather information from the internet. Choose a website as your resource.
2. Use the `“beautifulsoup4”` library to parse the HTML content and extract the necessary weather data for the chosen city.

## Store and Display Weather Information
1. Utilize Python data structures, such as lists and dictionaries, to store the weather data retrieved from the internet.
2. Create a display area in the GUI to present the weather information.
3. Show the weather information for the chosen city, including the temperature (day and night) and wind speed for the next three days.

## Temperature Conversion
1. Implement a button in the GUI that allows users to toggle between `Celsius` and `Fahrenheit` temperature units.
2. Include the necessary logic to convert the temperature values and update the displayed weather information accordingly.

## Save and Load User Preferences
1. Implement functionality to save the selected city and temperature unit to a `Settings.txt` file when the program is closed.
2. When the program starts, check if the `Settings.txt` file exists.
3. If the file exists, read the city and temperature unit preferences from the file and set them
as the default.
4. If the file does not exist or the preferences cannot be read, start with an empty city and
the default temperature unit.

## Additional Considerations
- Provide error handling mechanisms to handle situations where the internet connection is unavailable, or the weather data cannot be retrieved.
- Enhance the GUI by including appropriate labels, buttons, and user-friendly elements to improve the overall user experience.
- Consider adding additional features, such as displaying weather icons, sunrise/sunset times, or extended forecasts, to make the program more comprehensive and informative. <b>Better GUI may result in bonus points up to 15.</b>

<b>Important:</b> If you can not retrieve the weather data from the internet for some reason. Use same logic as User Preferences. Write some data you have generated to a text file to be read in the program and simulate the program. <b>However, do not forget, this will make your group lose points from Retrieve Weather Data task.</b>

### Initial design: 

<img width="850" alt="Screenshot" src="https://github.com/tareqalhammoodi/SE226-Project/assets/44919941/9dc11fbf-0dc3-4c72-99db-e11c0aaaae80">

### Modified design: 

<img width="850" alt="Screenshot" src="https://github.com/tareqalhammoodi/SE226-Project/assets/44919941/0ce9c59f-8468-4b16-9973-a40da9d76cd6">

### Final:

![ezgif com-gif-maker](https://github.com/tareqalhammoodi/SE226-Project/assets/44919941/47a95172-2b2d-4ede-ad2e-8b74c2f36611)
![ezgif com-gif-maker-2](https://github.com/tareqalhammoodi/SE226-Project/assets/44919941/00e3396e-03d6-4564-8ed3-4b21e0629d4f)

### Note: 
The implementation of this application could have been done  in a better way by using a weather API. However, in order to adhere to the given instructions, we opted for an alternative approach that serves our project's requirements.  Nonetheless, it is important to note that this method is not the most efficient, as it tends to be slow and is depending on any changes that may occur on the website that we're getting the data from.


## Contributors
Team Members:

&ensp;&ensp;&ensp;[Barkın Mercan](https://github.com/Barkinmercann)

&ensp;&ensp;&ensp;[Özgür Selağzı](https://github.com/ozgursselagzi)

&ensp;&ensp;&ensp;[Tareq Alhammoodi](https://www.linkedin.com/in/tareq-alhammoodi-290519183/)

Course Assistan(s):

&ensp;&ensp;&ensp;[Res. Asst. Erdem Okur](https://people.ieu.edu.tr/en/erdemokur/main)

SE-226 Course Coordinator and Lecturer, [Assoc. Prof. Senem KUMOVA METİN](https://people.ieu.edu.tr/en/senemkumovametin/main)
