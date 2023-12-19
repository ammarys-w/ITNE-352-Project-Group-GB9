# Ammar Yaser Marhoon   202103261  section:2
# Hussain Ali Mubarak   202104263  section:1

import socket

def create_client_socket():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
        print(f"Error creating socket: {e}")
        return None
    return client

def send_request(client, request, data):
    try:
        client.sendto(request.encode(), ("localhost", 5522))
        client.sendto(data.encode(), ("localhost", 5522))
        response, _ = client.recvfrom(2048)
        return response.decode()
    except socket.error as e:
        print(f"Error sending/receiving data: {e}")
        return None

def main_menu(client):
    while True:
        print()
        print("Main Menu")
        print(20 * "=")
        print(" 1 for full information about a single employee")
        print(" 2 for the Gender and the Experience of an employee")
        print(" 3 for the Position Title and Position # of an employee")
        print(" 4 for a list of employee names and their Position # by specified Position Title")
        print(" 5 to Exit the program")
        print(20 * "=")

        choice = input("Enter your choice: ")
        print(20 * "=")

        if choice == '1':
            process_request(client, "CASE1", "Please Enter an Employee Name: ")
        elif choice == '2':
            process_request(client, "CASE2", "Please Enter an Employee Name: ")
        elif choice == '3':
            process_request(client, "CASE3", "Please Enter an Employee Name: ")
        elif choice == '4':
            process_request(client, "CASE4", "Please enter a Position Title: ")
        elif choice == '5':
            print("Goodbye!")
            client.close()
            break
        else:
            print("Please enter a valid input!")

def process_request(client, case, prompt):
    data = input(prompt)
    response = send_request(client, case, data)
    if response:
        print("Employee's Information:")
        print()
        print(15 * "*")
        print()
        print(response)
        print()
        print(15 * "*")
    else:
        print("Failed to get response from server")
        print()

if __name__ == "__main__":
    client = create_client_socket()
    if client:
        main_menu(client)