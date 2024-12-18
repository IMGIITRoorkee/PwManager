from cryptography.fernet import Fernet

class PasswordManager:

    def __init__(self, cloud_manager=None):
        self.key = None
        self.password_file = None
        self.password_dict = {}
        self.cloud_manager = cloud_manager

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()

    def create_password_file(self, path, initial_values=None):
        self.password_file = path
        if initial_values:
            for site, password in initial_values.items():
                self.add_password(site, password)

    def load_password_file(self, path):
        self.password_file = path
        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.strip().split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, site, password):
        self.password_dict[site] = password
        if self.password_file:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                f.write(f"{site}:{encrypted}\n")

    def get_password(self, site):
        return self.password_dict.get(site, "Password not found.")

    def upload_password_file(self):
        if self.cloud_manager and self.password_file:
            file_name = self.password_file
            file_id = self.cloud_manager.upload_file(self.password_file, file_name)
            print(f"File uploaded. File ID: {file_id}")

    def download_password_file(self, file_name):
        if self.cloud_manager:
            destination = f"downloaded_{file_name}"
            self.cloud_manager.download_file(file_name, destination)
            self.load_password_file(destination)
            print(f"File downloaded and loaded: {destination}")