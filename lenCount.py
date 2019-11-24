import requests

URL = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
response = requests.get(URL)
obj = response.json()
print("length:", len(obj['applist']['apps']) )

# Result : 87333