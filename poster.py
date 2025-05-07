import requests
import json   

#DENNE BRUKER JEG FOR Å ENDRE PÅ TEMPERATUREN I SENSOREN 
#DERRETTER REFRESHER JEG TEMPERATUREN I DASHBOARDET FÅR Å SJEKKE OM DEN FUNKER

BASE_URL   = "http://localhost:8000"        
SENSOR_ID  = "4d8b1d62-7921-4917-9b70-bbd31f6e2e8e"

payload = {
    "value": 23.6,     
    "unit":  "°C"
}

r = requests.post(
    f"{BASE_URL}/smarthouse/sensor/{SENSOR_ID}/current",
    json=payload,
    timeout=5,         
)
r.raise_for_status()   

print("Server replied:", json.dumps(r.json(), indent=2))