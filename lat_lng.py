import requests
import json

# replace YOUR_API_KEY with your Google Maps API key
api_key = 'AIzaSyAu7nMq5SJrSC2OmYnish8yHQ-fpW0qLQU'

# replace PLACE_ID with the Place ID you want to retrieve the latitude and longitude for
place_id = 'ChIJT8Nz4jHcW04RXX-4Bfodnng'

# create the API url with the api_key and place_id
url = f'https://maps.googleapis.com/maps/api/place/details/json?key={api_key}&place_id={place_id}'

# send a GET request to the url and get the response
response = requests.get(url)

# convert the response to json format
data = json.loads(response.text)

# retrieve the latitude and longitude from the response
latitude = data['result']['geometry']['location']['lat']
longitude = data['result']['geometry']['location']['lng']

# print the latitude and longitude
print(f'Latitude: {latitude}, Longitude: {longitude}')
