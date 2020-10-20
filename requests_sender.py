import requests
import json

address = 'http://127.0.0.1:8000/'
address1 = 'http://127.0.0.1:8000/search_by_query'
#address2 = 'http://127.0.0.1:7000/search_by_datasets'
address3 = 'https://damp-meadow-03187.herokuapp.com/hello'
address4 = 'https://localhost:7777/hello'

if __name__ == '__main__':

    #request = {'query': 'spatial'}
    print(requests.get(address3))
    # response = requests.get(address1, params=request)
    # print('code:', response)
    # print(response.text)
    # download_url = json.loads(response.text)['result'][1]['link']
    # print(download_url)
    # response = requests.get(address+download_url)
    # open('hoba.pdf', 'wb').write(response.content)
