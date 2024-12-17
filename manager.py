from cryptography.fernet import Fernet
import hashlib
import base64

class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)
        
        backup_key = Fernet.generate_key()

        print("Set a security question to recover your key:")
        question = input("Enter security question: ").strip()
        answer = input("Enter answer to the question: ").strip()

        recovery_key = hashlib.sha256(answer.encode()).digest()
        recovery_key = base64.urlsafe_b64encode(recovery_key)  
        recovery_fernet = Fernet(recovery_key)  

        encrypted_backup = recovery_fernet.encrypt(backup_key)

        with open("backup_key.txt", 'w') as f:
            f.write(f"{question}\n")
            f.write(encrypted_backup.decode())  

        print("Backup created successfully!")

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()

    def create_password_file(self, path, initial_values=None):
        self.password_file = path
        if initial_values is not None:
            for site, password in initial_values.items():
                self.add_password(site, password)

    def load_password_file(self, path):
        self.password_file = path
        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, site, password):
        self.password_dict[site] = password
        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                f.write(f"{site}:{encrypted}\n")

    def get_password(self, site):
        return self.password_dict.get(site, "Password not found.")
    
    #the recovery function

    def recover_key(self, backup_path):
        try:
            with open(backup_path, 'r') as f:
                question = f.readline().strip()
                encrypted_backup_key = f.readline().strip()

            print(f"Security Question: {question}")
            answer = input("Enter your answer: ").strip()

            recovery_key = hashlib.sha256(answer.encode()).digest()
            recovery_key = base64.urlsafe_b64encode(recovery_key)  # URL-safe encoding for Fernet

            recovery_fernet = Fernet(recovery_key)
            decrypted_key = recovery_fernet.decrypt(encrypted_backup_key.encode())  # Decrypt the key
          
            self.key = decrypted_key
            print("Key recovered successfully!")

        except Exception as e:
            print(f"Error: {e}\nFailed to recover the key.")

    
   
