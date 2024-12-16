from cryptography.fernet import Fernet
from datetime import datetime

class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)
    def showDate(self):
        if self.password_file is not None:
            if self.password_dict.get("last_updated") is not None:
                print("Last updated: " + self.password_dict.get("last_updated"))

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()

    def create_password_file(self, path, initial_values=None):
        self.password_file = path
        with open(self.password_file,"a+") as f:
            encryptedDate = Fernet(self.key).encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode()).decode()
            f.write(f"last_updated:{encryptedDate}\n")
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
        return "the password for " + site + " is "+  self.password_dict.get(site, "Password not found.") + " and was Last updated: " + self.password_dict.get("last_updated", "date not found")
