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

    # checking if there is an error on the website
    if 'error' in data_of_flight:
        print('>>> Error: '+data_of_flight['error']['message'])
        sys.exit()
    # checking if there is no data available on the website
    if data_of_flight['data'] == []:
        print('>>> There is No Data Matching This Airport Code from the [SERVER]')
        return None
    # Save the data to a JSON file
    with open('GB9.json', 'w') as f:
        json.dump(data_of_flight, f, indent=4)
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
            spcific_airport.append(info)
    return spcific_airport
# End of extract_specific_airport function

# option number 4: Extract specific flight from the data


def extract_specific_flight(data, iata):
    spcific_flight = []
    for flight in data:
        if flight['flight']['iata'] == iata:
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

def process_client(client_sock, client_addr, client_id, flight_info):
    print(f"[NEW CONNECTION] Client {client_id} connected from {client_addr}")
    # Receive the client request
    received_data = client_sock.recv(1024).decode("ascii")
    client_request = json.loads(received_data)
    print(f"[REQUEST] Client {client_id}: {client_request['type']}")
    
    # Process the client request
    if client_request["type"] == "Arrived":
        server_response = extract_flight_arrived(flight_info["data"])
    elif client_request["type"] == "Delayed":
        server_response = extract_flight_delayed(flight_info["data"])
    elif client_request["type"] == "Specific Airport":
        server_response = extract_specific_airport(flight_info["data"],client_request["parameters"])
    elif client_request["type"] == "Specific Flight":
        server_response = extract_specific_flight (flight_info["data"],client_request["parameters"])
    else:
        server_response = {"error": "Invalid request"}

    # Send the response to the client
    client_sock.send(json.dumps(server_response).encode("ascii"))
    print(f"[DISCONNECTED] Client {client_id}")
    client_sock.close()
# End of handle_client function

# Managing airport erros
while True:
    arr_icao = input("Please input the airport code: ")
    flight_info = retrieve_data(arr_icao)
    if flight_info is not None:
        break

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, port))
server_socket.listen(5)
print("[SERVER] Listening on {} : {}".format(IP, port))

while True:
    client_sock, address = server_socket.accept()
    client_identity = client_sock.recv(1024).decode("utf-8")
    client_thread = threading.Thread(target=process_client, args=(client_sock, address, client_identity, flight_info))
    client_thread.start()
