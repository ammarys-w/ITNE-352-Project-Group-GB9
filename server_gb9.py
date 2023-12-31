import socket
import json
import sys
import threading
import requests

api_key = "8d782c20ade5ab1413c59a3f9b545516"
IP = "192.168.8.101"
port = 50000

# Getting data from the WEbsite

def retrieve_data(arr_icao):
    url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&arr_icao={arr_icao}&limit=100"   
    server_response = requests.get(url)
    data_of_flight = server_response.json()
    # Save the data to a JSON file
    with open('GB9.json', 'w') as f:
        json.dump(data_of_flight, f, indent=4)
    # checking if there is an error on the website
    if 'error' in data_of_flight:
        print('>>> Error: '+data_of_flight['error']['message'])
        sys.exit()
    # checking if there is no data available on the website
    if data_of_flight['data'] == []:
        print('>>> There is No Data Matching This Airport Code from the [SERVER]')
        return None
    
    return data_of_flight
# End of retrieve_data function

# option number 1:Extract flight arrived from the data
def extract_flight_arrived(data):
    flight_info = []
    for flight in data:
            info = {
                'Departure Airport': flight['departure']['airport'],
                'Flight IATA': flight['flight']['iata'],
                'Arrival Time': flight['arrival']['scheduled'],
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
            'Origin Departure Time': flight['departure']['scheduled'],
            'Estimated Arrival Time': flight['arrival']['estimated'],
            'Arrival Delay': flight['arrival']['delay'],
            'Arival Terminal': flight['arrival']['terminal'],
            'Arival Gate': flight['arrival']['gate']
        }
        # Checking out if the flight is delayed, either during arrival or departure.
        # If there is a delay, it appends the flight information to the flight_info list.
        if flight["arrival"].get("delay") or flight["departure"].get("delay"):
            delayed_flights.append(info)
    return delayed_flights
# End of extract_flight_delayed function

# option number 3: Extract specific airport from the data

def extract_specific_airport(data, icao):
    spcific_airport = []
    for flight in data:
        info = {
            "Flight IATA": flight["flight"]["iata"],
            "Flight Status": flight["flight_status"],
            "Departure Airport": flight["departure"]["airport"],
            "Departure Gate": flight["departure"]["gate"],
            "Original Departure Time": flight["departure"]["scheduled"],
            "Estimated Arrival Time": flight["arrival"]["estimated"],
            "Arrival Gate": flight["arrival"]["gate"]
        }
        # If a flight's ICAO code matches the provided one, the flight's information is added to the specific_airport list.
        if flight["flight"].get("icao") == icao:
            extract_specific_airport.append(info)
    return spcific_airport
# End of extract_specific_airport function

# option number 4: Extract specific flight from the data

def extract_specific_flight(data, iata):
    spcific_flight = []
    for flight in data:
            info = {
                'Flight IATA': flight['flight']['iata'],
                'Flight Status': flight['flight_status'],
                'Departure Airport': flight['departure']['airport'],
                'Departure Terminal': flight['departure']['terminal'],
                'Departure Gate': flight['departure']['gate'],
                'Arrival Airport': flight['arrival']['airport'],
                'Arival Terminal': flight['arrival']['terminal'],
                'Arival Gate': flight['arrival']['gate'],
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

def handling_client(sock, addr, client_identifier, flight_data):
    print(f"[NEW CLIENT] {client_identifier} has established a connection from {addr}")
    # Receive the request
    data_received = sock.recv(1024).decode("ascii")
    client_req = json.loads(data_received)
    print(f"[CLIENT REQUEST] Client {client_identifier} requested: {client_req['type']}")
    
    # Process the request
    if client_req["type"] == "Arrived":
        response = extract_flight_arrived(flight_data["data"])
    elif client_req["type"] == "Delayed":
        response = extract_flight_delayed(flight_data["data"])
    elif client_req["type"] == "Specific Airport":
        response = extract_specific_airport(flight_data["data"], client_req["parameters"] )
    elif client_req["type"] == "Specific Flight":
        response = extract_specific_airport(flight_data["data"], client_req["parameters"] )
    else:
        response = {"error": "Invalid request"}

    # Send the response to the client
    sock.send(json.dumps(response).encode("ascii"))
    print(f"[CLIENT DISCONNECTED] {client_identifier}")
    sock.close()
# End of handle_client function

# Managing airport erros
while True:
    arr_icao = input(">> Please input the airport code: ")
    flight_info = retrieve_data(arr_icao)
    if flight_info is not None:
        break

# Create a new socket using the Internet address and Stream socket type

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((IP, port))
# Set the socket to listen for incoming connections with a backlog of 4 connections at most' You can change it to 3 if u want'
server_sock.listen(4)
print(f"[SERVER STATUS] Server is now listening on {IP} : {port}")

try:
    while True:
        client_sock, address = server_sock.accept()
        client_identity = client_sock.recv(1024).decode("ascii")
        client_thread = threading.Thread(target=handling_client, args = (client_sock, address, client_identity, flight_info))
        client_thread.start()
        
except KeyboardInterrupt: 
    # to handle the keyboard interrupt
    print("\n[SERVER SHUTDOWN] Server is shutting down...")
    server_sock.close()