import socket
import csv

print(25 * "=" + "\nThe server has started: ")

ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ss.bind(("localhost", 5522))

with open("Employee_data.csv", "r") as f:
    reader = csv.reader(f)
    employee_list = list(reader)

def get_employee_information(employee_name, by_position=False):
    if by_position:
        return [emp for emp in employee_list 
                if emp[2] == employee_name]
    for employee in employee_list:
        if employee[0] == employee_name:
            return employee
    return None

def handle_request(case, data, address):
    employee_name = data.decode().strip()

    if case == "CASE1":
        employee = get_employee_information(employee_name)
        response = ','.join(employee) if employee else "Employee not found"

    elif case == "CASE2":
        employee = get_employee_information(employee_name)
        response = f"Gender: {employee[1]}, Experience: {employee[4]}" if employee else "Employee not found"

    elif case == "CASE3":
        employee = get_employee_information(employee_name)
        response = f"Position Title: {employee[2]}, Position Number: {employee[3]}" if employee else "Employee not found"

    elif case == "CASE4":
        employees = get_employee_information(employee_name, by_position=True)
        response = "\n".join([f"Employee Name: {emp[0]}, Position Number: {emp[3]}" for emp in employees]) if employees else "No employees found for this position"

    elif case == "CASE5":
        print("Server shutting down...")
        ss.close()
        exit()

    else:
        response = "Invalid case"

    ss.sendto(response.encode(), address)

while True:
    case_data, address = ss.recvfrom(2048)
    case = case_data.decode().strip()
    additional_data, address = ss.recvfrom(2048)
    handle_request(case, additional_data, address)