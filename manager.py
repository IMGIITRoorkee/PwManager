from cryptography.fernet import Fernet

from logger import ActionLogger

class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}
        self.logger = ActionLogger()

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)
        self.logger.log_action(f"CREATE_KEY {path}")

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()
        self.logger.log_action(f"LOAD_KEY {path}")

    def create_password_file(self, path, initial_values=None):
        self.password_file = path
        if initial_values is not None:
            for site, password in initial_values.items():
                self.add_password(site, password)
        self.logger.log_action(f"CREATE_PASSWORD_FILE {path}")

    def load_password_file(self, path):
        self.password_file = path
        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
        self.logger.log_action(f"LOAD_PASSWORD_FILE {path}")

    def add_password(self, site, password):
        self.password_dict[site] = password
        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                f.write(f"{site}:{encrypted}\n")
        self.logger.log_action(f"ADD_PASSWORD {site}")

    def get_password(self, site):
        self.logger.log_action(f"GET_PASSWORD {site}")
        return self.password_dict.get(site, "Password not found.")

    def verify_log_integrity(self):
        return self.logger.verify_log_integrity()

    def print_logs(self):
        self.logger.print_logs()
