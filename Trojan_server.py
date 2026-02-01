import socket
import ssl
from cryptography.fernet import Fernet

def start_server():

    key = Fernet.generate_key()
    print(f"Generated Key: {key.decode()}")


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(5)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    print("Fernet Server is listening on 127.0.0.1:8080...")

    while True:
        client_sock, addr = server_socket.accept()
        try:
            with context.wrap_socket(client_sock, server_side=True) as securesock:
                print(f"Connection from {addr}")
                securesock.send(key)
                print("Key sent successfully.")
        except Exception as e:
            print(f"SSL Error: {e}")

if __name__ == "__main__":
    start_server()