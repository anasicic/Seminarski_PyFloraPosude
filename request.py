import requests
from bs4 import BeautifulSoup


url = 'https://api.open-meteo.com/v1/forecast?latitude=45.8150&longitude=15.9819&hourly=temperature_2m'
response = requests.get(url)



if response.status_code == 200:
    data = response.json()
    temperature = data['hourly']['temperature_2m']
    length = len(temperature)
    print('Trenutna temperatura u Zagrebu je:', temperature[length-1], '°C')
else:
    print('Došlo je do pogreške prilikom dohvaćanja temperature.')

