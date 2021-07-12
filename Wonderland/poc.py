
import requests
import string
import time
url= 'http://10.10.82.181/'
# This will loop forever, stop it when you see it doesn't find anything new
while True:
	for letter in list(string.ascii_lowercase[:26]): # loops through the alphabet in lowercase starting with a
		print(url)
		r = requests.post(url+letter+'/')
		if r.status_code == 200:
			#print('NICE! ',r.status_code)
			url = url + letter +'/'
			letter = string.ascii_lowercase[0]
		else:
			#print(r.status_code)
			time.sleep(0)