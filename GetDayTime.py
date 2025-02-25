import requests
import pandas as pd
months = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre" \
            ]
cities = ["ascoli-piceno", "asti", "barberino-di-mugello", "bari", "biella", "bologna", "brescia", "como", "catania", "gradisca-d'isonzo", \
          "genova", "milano", "modena", "mondovi", "napoli", "padova", "palermo", "parma", "pavia", "pordenone", "ravenna", "roma", "rovigo", \
          "san-pietro-in-casale", "torino", "varese", "verona" \
          ]
Headings = {'Data':[], 'Alba':[], 'Tramonto':[], 'Lunghezza di giorno':[], 'City Name':[]}
year = '2024'

def GetYear():
    year = input("Pleas enter current year: ")
    df = pd.DataFrame(Headings)
    df.to_csv('DayTimeData.csv', mode='a', index=False, header=True)
GetYear()
for x in cities:
    for y in months:
        city = pd.DataFrame({'City': [x]})
        while True:
            try:
                df = pd.read_html(requests.get('https://www.sunrise-and-sunset.com/it/sun/italia/'+ x + '/'+year+'/'+ y).content)[-1]
                table = df.iloc[:-1 ,:]
                TimeData = table.assign(cityName=city)
                print(TimeData)
                TimeData.to_csv('DayTimeData.csv', mode='a', index=False, header=False)
            except requests.exceptions.ConnectionError:
                print("Connection Error")
                continue
            except ValueError:
                print("Value Error")
            break