import requests
import pandas as pd
# months = {"gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "decembre" }
# cities = {"ascoli-piceno", "asti", "barberino-di-mugello", "bari", "biella", "bologna", "brescia", "como", "catania", "ottobre", "gradisca-d'isonzo", \
#           "genova", "milano", "modena", "mondovi", "napoli", "padova", "palermo", "parma", "pavia", "pordenone", "ravenna", "roma", "rovigo", "san-pietro-in-casale", \
#           "torino", "varese", "verona" }
cities = {"turin"}
for x in cities:
    for y in range(1):
        z = str(y+1)
        url = 'https://www.timeanddate.com/sun/italy/'+x+'?month='+z+'&year=2026'
        print("URL \n", url)
        response = requests.get(url)
        print("RESPONSE \n", response)
        df = pd.read_html(response.content)[-1]
        # Eliminate last row
        table = df.iloc[:-1 ,:]
        print("DATAFRAME \n", table)
        table.to_csv('table_data.csv', mode='a', index=False, header=False)