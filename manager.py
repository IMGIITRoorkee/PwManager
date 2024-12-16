import time
from datetime import datetime,timedelta

from cryptography.fernet import Fernet

class PasswordManager:

    def __init__(self, expiration_days=30):
        self.key = None
        self.password_file = None
        self.password_dict = {}
        self.key_creation_date = None
        self.key_expiration_days = expiration_days

    def create_key(self, path):
        self.key = Fernet.generate_key()
        self.key_creation_date = datetime.now()

        with open(path, 'wb') as f:
            f.write(self.key)
            f.write(b"\n")
            f.write(self.key_creation_date.isoformat().encode())

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.readline().strip()  # first line for the key
            creation_date_str = f.readline().strip().decode()  # second line for the key creation date
            self.key_creation_date = datetime.fromisoformat(creation_date_str)
        
        if self.is_key_expired():
            return False
        return True

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
        encrypted = Fernet(self.key).encrypt(password.encode()).decode()
        self.password_dict[site] = encrypted
        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                f.write(f"{site}:{encrypted}\n")
                

    def get_password(self, site):
        return self.password_dict.get(site, "Password not found.")
    
    def is_key_expired(self):
        expiration_date = self.key_creation_date + timedelta(days=self.key_expiration_days)
        return datetime.now() > expiration_date

    def rotate_key(self,path,password_file):
        self.load_password_file(password_file)
        self.create_key(path)

        if self.password_dict is not None:
            with open(password_file, "w") as f:
                for site, password in self.password_dict.items():
                    self.password_dict[site] = password
                    encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                    f.write(f"{site}:{encrypted}\n")