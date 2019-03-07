import requests
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

API_KEY = os.getenv('API_KEY')
api = 'https://newsapi.org/v2/top-headlines?sources=cnn&apiKey={key}'

url = api.format(key=API_KEY)
r = requests.get(url)
data = json.loads(r.text)

print(datas)
