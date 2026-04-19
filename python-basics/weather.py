import requests

apikey = "6b970fab4b35817499b86ddcf0b2b437"
zipcode = input("Enter your zip code: ")
countrycode = input("Enter your country code: ")

weather_url = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode},{countrycode}&appid={apikey}"

response = requests.get(weather_url)
print(response.status_code)
print(response.json())