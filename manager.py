from cryptography.fernet import Fernet
import json

class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

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
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                for site, encrypted in data.items():
                    decrypted = Fernet(self.key).decrypt(encrypted.encode()).decode()
                    self.password_dict[site] = decrypted
        except FileNotFoundError:
            print(f"Password file {path} not found.")
        except json.JSONDecodeError:
            print(f"Error reading the password file {path}. It may be corrupted.")

    def add_password(self, site, password):
        encrypted = Fernet(self.key).encrypt(password.encode()).decode()
        self.password_dict[site] = encrypted
        if self.password_file is not None:
            with open(self.password_file, 'w') as f:
                json.dump(self.password_dict, f, indent=4)
                

    def get_password(self, site):
        return self.password_dict.get(site, "Password not found.")