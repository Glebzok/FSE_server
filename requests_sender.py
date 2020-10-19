import requests
import json

address = 'http://127.0.0.1:5000/'
address1 = 'http://127.0.0.1:5000/search_by_query'
address2 = 'http://127.0.0.1:5000/search_by_datasets'

if __name__ == '__main__':
    request = {'query': 'spatial'}
    response = requests.get(address1, json=request)
    print('code:', response)
    print(response.text)
    download_url = json.loads(response.text)['result'][0]['link']
    response = requests.get(address+download_url)
    print(response)
    open('hoba.pdf', 'wb').write(response.content)