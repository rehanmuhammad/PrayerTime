# Script to calculate prayer timing by data received from website: https://www.sunrise-and-sunset.com/it/sun/italia/
import sys
import requests
import pandas as pd
import numpy as np
from datetime import timedelta, datetime

# Lists definition
# months and city names(spellings) are same as on the website
months = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", \
          "settembre", "ottobre", "novembre", "dicembre"]
cities = ["ascoli-piceno", "asti", "barberino-di-mugello", "bari", "biella", "bologna", \
          "brescia", "como", "catania", "gradisca-d'isonzo", "genova", "milano", "modena", \
          "mondovi", "napoli", "padova", "palermo", "parma", "pavia", "pordenone", "ravenna", \
          "roma", "rovigo", "san-pietro-in-casale", "torino", "varese", "verona" ]
# Dictionary to hold final data to be transfered to CSV
PrayerHead = {'Data':[''],'Fajr':[''], 'Sunrise':[''],'Zuhr':[''], 'Asr':[''], 'Maghrib':[''], 'Isha':[''], 'City Name':['']}
# Offsets to calculate prayers timings
FAJR_OFFSET = timedelta(hours=1, minutes=30, seconds=0)    # 01:30
ZUHR_OFFSET = timedelta(hours=0, minutes=15, seconds=0)    # 00:15
MAGHRIB_OFFSET = timedelta(hours=0, minutes=5, seconds=0)  # 00:05
ISHA_OFFSET = timedelta(hours=1, minutes=30, seconds=0)    # 01:30
# Global variable to hold number of days in the month
NumDays= 0
# Numpy data array to hold copied data from website
PrayerArray = []
# Create main dataframe to hold all data 
HeadDf = pd.DataFrame(PrayerHead)
# Year string initialized as 2024 
year = ''
# Default CSV filename
CsvName = ""
# Method definition to get current year from user input e.g "2024" without quotation marks
def GetYear():
    global year 
    year = input("Please enter current year[yyyy]: ")
    global CsvName 
    CsvName = "PrayerTiming"+year+".csv"
    print("Save all Namaz TimeTable in ", CsvName)

def SetInitHeader(HeadDataframe):
    try:
        # Remove empty line
        HeadDataframe = HeadDataframe.iloc[:-1 ,:]
        # Create CSV and write the column names on the CSV file
        HeadDataframe.to_csv(CsvName, mode='a', index=False, header=True)
        # Check for all cities present in the list
    except:
        # print error
        print('Exception error')
        # Get sytem error
        errors = sys.exc_info()
        # Print error to screen
        for e in errors: 
            print(str(e)) 
            input('\nPress key to exit.') 
            exit()

def ReadTablesAndWriteCsv(HeadDataframe):
    # Check for all cities present in the list
    for x in cities:
        # All months of the year
        for y in months:
            # Reading the website link for tables and copy data to dataframe
            while True:
                try:
                    # Read website
                    df = pd.read_html(requests.get('https://www.sunrise-and-sunset.com/it/sun/italia/'+ x + '/'+year+'/'+ y).content)[-1]
                    # Eliminate last row
                    table = df.iloc[:-1 ,:]
                    # Calculate number of days in the month
                    NumDays = len(table.index)
                    # Convert data to numpy data array
                    PrayerArray = table.to_numpy()
                except requests.exceptions.ConnectionError:
                    print("WARNING:Connection error, Website link is not responding. Retrying again")
                    # Continue to open link 
                    continue
                except ValueError:
                    print("ERROR:Value error, please check spellings,",year, y,"or", x, "is not found... Exiting code!!!")
                    input('\nPress key to exit.')
                    # System exit
                    sys.exit()
                except:
                    input('\nGeneric error or user interrupt...Press key to exit.')
                    # System exit
                    sys.exit()
                break
            # Process the read data for prayer timings
            # [i,0]= Data, [i,1]= Alba, [i,2]= Tramonto, [i,3]= Lunghezza del giorno
            for i in range(NumDays):
                NamazStr = []
                NamazDelta = []
                # Sunrise time data 
                SunriseTime = datetime.strptime(PrayerArray[i,1], '%H:%M').time()
                NamazDelta.insert(0, timedelta(hours=SunriseTime.hour, minutes=SunriseTime.minute, seconds=SunriseTime.second))
                # Fajr prayer time calculation
                NamazDelta.insert(1, NamazDelta[0] - FAJR_OFFSET)
                # Total daylight hours
                DayTime = datetime.strptime(PrayerArray[i,3], '%H:%M').time()
                HalfDaytime_delta = timedelta(hours=DayTime.hour, minutes=DayTime.minute, seconds=DayTime.second) /2
                # Zuhr prayer time calculation
                NamazDelta.insert(2, NamazDelta[0] + HalfDaytime_delta + ZUHR_OFFSET)
                # Asr prayer time calculation
                NamazDelta.insert(3, NamazDelta[2] + (HalfDaytime_delta/2))
                # Sunset time data
                SunsetTime = datetime.strptime(PrayerArray[i,2], '%H:%M').time()
                MaghribTime_delta = timedelta(hours=SunsetTime.hour, minutes=SunsetTime.minute, seconds=SunsetTime.second)
                # Maghrib prayer time calculation
                NamazDelta.insert(4, MaghribTime_delta + MAGHRIB_OFFSET )
                # Isha prayer time calculation
                NamazDelta.insert(5, NamazDelta[4] + ISHA_OFFSET )
                for k in range(6):
                    NamazStr.insert(k,':'.join(str(NamazDelta[k]).split(':')[:3]))
                    # print(NamazStr[k])
                # Copy all data(add new row) to the dictionary
                # [0]= Date, [1]= Fajr, [2]= Sunrise, [3]= Zuhr, [4]= Asr, [5]= Maghrib, [6]= Isha, [7]= City Name
                HeadDataframe.loc[i, :] = [PrayerArray[i,0], NamazStr[1], NamazStr[0], NamazStr[2], NamazStr[3], NamazStr[4], NamazStr[5], x]
            # Print dictionary
            print(HeadDataframe)
            try:
                # Save table on CSV file
                HeadDataframe.to_csv(CsvName, mode='a', index=False, header=False)
            except:
                input('\nCSV write error... Press key to exit.')
            # Remove last three lines
            HeadDataframe = HeadDataframe.iloc[:-3 ,:]
########################### Main code starts here ###########################

# Get the year from user
GetYear()
# Set initialized header
SetInitHeader(HeadDf)
# Read from weblink and process time data to save into CSV
ReadTablesAndWriteCsv(HeadDf)

########################### Main code ends here ############################