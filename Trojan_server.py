import socket
import ssl
from cryptography.fernet import Fernet

def generate_and_save_key(client_ip):
    key = Fernet.generate_key() 
    path = f"C:/ServerStorage/Keys/{client_ip}.key"
    
    with open(path, "wb") as key_file:
        key_file.write(key)
    return key

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 8080))
sock.listen(1)

print("Server is running...")

while True:
    connection, address = sock.accept()
    try:
        ssl_conn = ssl.wrap_socket(
            connection, 
            server_side=True, 
            certfile="server.crt", 
            keyfile="server.key"
        )
        
        client_ip = ssl_conn.getpeername()[0]
        key = generate_and_save_key(client_ip)
        
        ssl_conn.sendall(key)
        ssl_conn.close()
    except Exception as e:
        print(f"Connection error: {e}")