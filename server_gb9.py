import socket,json
import sys
import threading

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
    # checking if there is no data available on the website
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
        info = {
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
    delayed_flights = []
    for flight in data:
        info = {
            'Departure Airport': flight['departure']['airport'],
            'Flight IATA': flight['flight']['iata'],
            'Origin Departure Time': flight['departure']['Scheduled'],
            'Estimated Arrival Time': flight['arrival']['estimated'],
            'Arrival Delay': flight['arrival']['delay'],
            'Arival Terminal': flight['arrival']['terminal'],
            'Arival Gate': flight['arrival']['gate'] 
        }
        #Checking out if the flight is delayed, either during arrival or departure.
        # If there is a delay, it appends the flight information to the flight_info list.
        if flight["arrival"].get("delay") or flight["departure"].get("delay"):
            delayed_flights.append(info)
    return delayed_flights
# End of extract_flight_delayed function

#option number 3: Extract specific airport from the data
def extract_specific_airport(data,icao):
    spcific_airport=[]
    for flight in data:
        info ={
            "Flight IATA": flight["flight"]["iata"],
            "Flight Status": flight["flight_status"],
            "Departure Airport": flight["departure"]["airport"],
            "Departure Gate": flight["departure"]["gate"],
            "Original Departure Time": flight["departure"]["scheduled"],
            "Estimated Arrival Time": flight["arrival"]["estimated"],
            "Arrival Gate": flight["arrival"]["gate"]  
        }
        #If a flight's ICAO code matches the provided one, the flight's information is added to the specific_airport list.
        if flight["flight"].get("icao") == icao:
                spcific_airport.append(info)
    return spcific_airport
# End of extract_specific_airport function

#option number 4: Extract specific flight from the data
def extract_specific_flight(data,iata):
    spcific_flight=[]
    for flight in data:
        if flight['flight']['iata'] == iata:
            info = {
                'Flight IATA': flight['flight']['iata'],
                'Flight Status': flight['flight_status'],
                'Departure Airport': flight['departure']['airport'],
                'Departure Terminal': flight['departure']['terminal'],
                'Departure Gate': flight['departure']['gate'] ,
                'Arrival Airport': flight['arrival']['airport'],
                'Arival Terminal': flight['arrival']['terminal'],
                'Arival Gate': flight['arrival']['gate'] ,
                'Scheduled departure time': flight['departure']['scheduled'],
                'Scheduled arrival time': flight['arrival']['scheduled']
            }
            # if the IATA code matches the provided one, the flight's information is added to the specific_flight list.
            # So , this function is gathering information about flights that match a specific IATA code.
            if flight["flight"].get("iata") == iata:
                spcific_flight.append(info)
            return spcific_flight
# End of extract_specific_airport function

# Handling the client requests
def handle_client(client_socket, addr, client_name, flight_data):
    print(f"[NEW CONNECTION] {client_name} connected from {addr}")
    # Receive the request
    data = client_socket.recv(1024).decode("ascii")
    request = json.loads(data)
    print(f"[REQUEST] {client_name}: {request['type']}")
    # Handle the request
    handlers = {
        "Arrived": lambda: extract_flight_arrived(flight_data["data"]),
        "Delayed": lambda: extract_flight_delayed(flight_data["data"]),
        "Specific Airport": lambda: extract_specific_airport(flight_data["data"], request["parameters"]),
        "Specific Flight": lambda: extract_specific_flight(flight_data["data"], request["parameters"])
    }
    response = handlers.get(request["type"], lambda: {"error": "Invalid request"})()

    #sending the response to the client    
    client_socket.send(json.dumps(response).encode("ascii"))
    print("[DISCONNECTED] {}".format(client_name))
    client_socket.close()   
     
# End of handle_client function        
# Managing airport erros
while True:
    airport_code = input("Please input the airport code: ")
    flight_info = retrieve_data(airport_code)
    if flight_info is not None:
        break  
    
# Create a server socket
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((IP, port))
server_sock.listen(3)
print(f"[SERVER] Server is listening on {IP} : { port}")    

while True:
    client_sock, address = server_sock.accept()
    client_identity = client_sock.recv(1024).decode("utf-8")
    client_thread = threading.Thread(target=handle_client, args=(client_sock, address, client_identity, flight_info))
    client_thread.start()        

    