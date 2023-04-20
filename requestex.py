import requests
import json

x = requests.get("http://localhost:8000/state_district_wise.json")
y = json.loads(x.text)
activeEx = y['Andaman and Nicobar Islands']['districtData']['South Andaman']['active']
print("Active cases in South Andaman:", activeEx)