import requests

response = requests.post('https://stazjava.consdata.com/api/command')
print(response.text) 