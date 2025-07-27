import requests
import pandas as pd
months = {"gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "decembre" }
cities = {"ascoli-piceno", "asti", "barberino-di-mugello", "bari", "biella", "bologna", "brescia", "como", "catania", "ottobre", "gradisca-d'isonzo", \
          "genova", "milano", "modena", "mondovi", "napoli", "padova", "palermo", "parma", "pavia", "pordenone", "ravenna", "roma", "rovigo", "san-pietro-in-casale", \
          "torino", "varese", "verona" }

for x in cities:
    for y in months:
        df = pd.read_html(requests.get('https://www.sunrise-and-sunset.com/it/sun/italia/'+ x + '/2025/'+ y).content)[-1]
        print(df)
        df.to_csv('table_data.csv', mode='a', index=False, header=False)