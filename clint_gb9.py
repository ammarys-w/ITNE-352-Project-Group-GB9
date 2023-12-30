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
            name = nm_entry.get()
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
    if nm_entry.get() == "" : 
        rs_window("Please Provide a Valid Name !!") 
        return 
# Check for request type error 
    request_type = req_type_combobox.get()
    if request_type in ["Arrived", "Delayed"]:
        parameters = {}
    elif request_type == "Specific Airport": 
        if ap_icao_entry.get() == "": 
            rs_window("Please Provide the ICAO of the Airport !!") 
            return 
        parameters = ap_icao_entry.get().upper().replace(" ","")
    elif request_type == "Specific Flight": 
        if f_iata_entry.get() == "": 
            rs_window("Please Provide the IATA of the Flight !!") 
            return 
        parameters = f_iata_entry.get().upper().replace(" ","") 
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

#create GUI interface
root = tk.Tk()
root.title("Flight Information App")
mainframe = ttk.Frame(root, padding="10")
mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# create name box
nm_label = ttk.Label(mainframe, text="Enter your name:")
nm_label.grid(row=0, column=0, sticky=tk.W)
nm_entry = ttk.Entry(mainframe)
nm_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

# create request type box
req_type_label = ttk.Label(mainframe, text="Select request type:")
req_type_label.grid(row=1, column=0, sticky=tk.W)
req_types = ["Arrived", "Delayed", "Specific Airport", "Specific Flight"]
req_type_combobox = ttk.Combobox(mainframe, values=req_types)
req_type_combobox.grid(row=1, column=1, sticky=(tk.W, tk.E))

# create ICAO box
ap_icao_label = ttk.Label(mainframe, text="ICAO code (Specific Airport only):")
ap_icao_label.grid(row=2, column=0, sticky=tk.W)
ap_icao_entry = ttk.Entry(mainframe)
ap_icao_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

# create IATA box
f_iata_label = ttk.Label(mainframe, text="IATA code (Specific Flight only):")
f_iata_label.grid(row=3, column=0, sticky=tk.W)
f_iata_entry = ttk.Entry(mainframe)
f_iata_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))
