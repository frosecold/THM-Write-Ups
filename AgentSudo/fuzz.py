import requests
import string
import time

url = 'http://10.10.121.186/'

response_length = []
for element in list(string.ascii_uppercase[:26]): #Loops uppercase letters for User-Agent
    print("Trying: " + element)
    headers = {'User-Agent': element }
    response = requests.get(url, headers=headers)
    if len(response.text) not in response_length:
        print("--------------------------------------")
        response_length.append(len(response.text))
        print("Agent " + element + "\r\n")
        print(response.text)
        time.sleep(2)
        print("--------------------------------------")
    else:
        time.sleep(0)
        