import socket,json
import time 

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
