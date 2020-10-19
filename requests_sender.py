import requests

address1 = 'http://127.0.0.1:5000/search_by_query'
address2 = 'http://127.0.0.1:5000/search_by_datasets'

if __name__ == '__main__':
    request = {'search_query': 'image segmentation with YOLO'}
    response = requests.get(address1, json=request)
    print('code:', response)
    print(response.text)
