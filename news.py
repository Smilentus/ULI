import requests
import pprint

# Категории: business entertainment general health science sports technology
def getNews():
       url = ('http://newsapi.org/v2/top-headlines?'
              'country=ru&'
              'pageSize=1&'
              'apiKey=f7ec7e428a01475e96852d390e8ce404')
       response = requests.get(url)

       articles = response.json()

       return articles