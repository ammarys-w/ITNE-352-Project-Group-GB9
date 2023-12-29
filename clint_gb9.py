import socket,json
import time 
import tkinter as tk
from tkinter import ttk

server_ip = "192.168.8.101"
server_port = 50000

# to send request and receve response from the server
def send_req(request):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sc:
            sc.connect((server_ip, server_port))
            name = name_entry.get()
            sc.send(name.encode("ascii"))
            time.sleep(5)
            sc.send(json.dumps(request).encode("ascii"))

            response = b""
            while True:
                data = sc.recv(4096)
                if not data:
                    break
                response += data
            response = response.decode("ascii")
            return json.loads(response)
    except ConnectionError:
        return None

# to handle Errors in the request from GUI
def manage_request(): 
# Check for name error 
    if name_entry.get() == "" : 
        rs_window("Please Provide a Valid Name !!") 
        return 
# Check for request type error 
    request_type = request_type_combobox.get()
    if request_type in ["Arrived", "Delayed"]:
        parameters = {}
    elif request_type == "Specific Airport": 
        if airport_icao_entry.get() == "": 
            rs_window("Please Provide the ICAO of the Airport !!") 
            return 
        parameters = airport_icao_entry.get().upper().replace(" ","")
    elif request_type == "Specific Flight": 
        if flight_iata_entry.get() == "": 
            rs_window("Please Provide the IATA of the Flight !!") 
            return 
        parameters = flight_iata_entry.get().upper().replace(" ","") 
    else: 
            rs_window("Invalid Request Type \n Please Choose One From The Options !!") 
            return 
    request = {"type": request_type, "parameters": parameters} 
    response = send_req(request) 
# Check for response error 
    if response == []: 
        rs_window("No Results Found for Your Query !!") 
    elif response is None: 
        rs_window("Server is Unreachable :(")
    else: rs_window(text_form(json.dumps(response, indent=3)))

    # to modify the look of the text
def text_form(text):
    new_text= text.replace('''   },
{''', "********************************************************************************")
    remove = '"[{]},'
    for sympol in remove:
        new_text= new_text.replace(sympol, "")
    return new_text

# to refresh the response window
def res_window(response):
    res_text.set(response)
    res_display = tk.Text(mainframe, wrap="word")
    res_display.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
    res_scrollbar = ttk.Scrollbar(mainframe, command=res_display.yview)
    res_scrollbar.grid(row=6, column=2, sticky=(tk.N, tk.S))
    res_display.insert(tk.END, res_text.get())
    res_display.config(state=tk.DISABLED)
    res_display.config(yscrollcommand=res_scrollbar.set)    
