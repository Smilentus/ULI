import requests
import pprint

def initWeather():
       url = ('https://api.openweathermap.org/data/2.5/'
              'weather?id=1508291&'
              'units=metric&'
              'appid=fb14129095fe1575c356b77ffb55e40d')

       response = requests.get(url)

       return response.json()

def getWeather():
       response = initWeather()

       return 'Погода в {}. Температура {} градуса по Цельсию, ощущается как {} градуса по Цельсию. Влажность {}%. Давление {} миллиметров ртутного столба. Ветер по направлению {} градусов со скоростью {} метров в секунду'.format(
              response['name'],
              response['main']['temp'] , 
              response['main']['feels_like'], 
              response['main']['humidity'], 
              response['main']['pressure'], 
              response['wind']['deg'], 
              response['wind']['speed'] 
       ) 