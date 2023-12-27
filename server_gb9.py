import socket,json
import sys
api_key = "8d782c20ade5ab1413c59a3f9b545516"
IP="192.168.8.101"
port=50000

# Getting data from the WEbsite
def retrieve_data(arr_icao):
    url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&arr_icao={arr_icao}&limit=100"
    server_response = server_response.get(url)
    data_of_flight  = server_response.json()
    
    #checking if there is an error on the website 
    if 'error' in data_of_flight :
        print('>>> Error: '+data_of_flight ['error']['message'])
        sys.exit()
    # if there is no data available on the website
    if data_of_flight['data'] ==[]:
        print('>>> There is No Data Matching This Airport Code from the [SERVER]')
        return None
    with open ('group_B9.json','w') as f:
        json.dump(data_of_flight , f, indent=4)
    return data_of_flight    
# End of retrieve_data function


# option number 1:Extract flight arrived from the data
def extract_flight_arrived(data):
    flight_info = []
    for flight in data:
        info ={
            'Departure Airport': flight['departure']['airport'],
            'Flight IATA': flight['flight']['iata'],
            'Arrival Time': flight['arrival']['Scheduled'],
            'Arival Terminal': flight['arrival']['terminal'],
            'Arival Gate': flight['arrival']['gate'] 
        }
        flight_info.append(info)
    return flight_info
# End of extract_flight_arrived function

# option number 2:Extract flight Delayed from the data
def extract_flight_delayed(data):
    flight_info = []
    for flight in data:
        info ={
            'Departure Airport': flight['departure']['airport'],
            'Flight IATA': flight['flight']['iata'],
            'Origin Departure Time': flight['departure']['Scheduled'],
            'Estimated Arrival Time': flight['arrival']['estimated'],
            
            
            
            
            
            
            
            
        }

    