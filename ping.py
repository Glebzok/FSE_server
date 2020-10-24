import requests
from time import sleep

ping_address = 'https://damp-meadow-03187.herokuapp.com/hello'

if __name__ == '__main__':
    while True:
        try:
            print(requests.get(ping_address))
            sleep(20*60)
        except Exception as e:
            print(e)

