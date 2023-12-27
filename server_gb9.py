import socket,json
import sys
api_key = "8d782c20ade5ab1413c59a3f9b545516"
IP="192.168.8.101"
port=40000

# Getting data from the WEbsite
def get_data(arr_icao):
    link = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&arr_icao={arr_icao}&limit=100"
    response = response.get(link)
    flight_data = response.json()
    
    #checking if there is an error in the website 
    if 'error' in flight_data:
        print('>>> Error: '+flight_data['error']['message'])
        sys.exit