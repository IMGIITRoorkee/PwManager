from cryptography.fernet import Fernet


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
    def delete_password(self, site):
        if site in self.password_dict:
            # Remove from the dictionary
            del self.password_dict[site]
            # Update the password file
            if self.password_file is not None:
                with open(self.password_file, 'r') as f:
                    lines = f.readlines()
                with open(self.password_file, 'w') as f:
                    for line in lines:
                        if not line.startswith(site + ":"):  # Skip the line with the site to delete
                            f.write(line)
        else:
            print("Site not found.")
