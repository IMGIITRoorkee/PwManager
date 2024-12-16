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
        try:
            with open(path, 'r') as f:
                for line in f:
                    site, encrypted = line.split(":")
                    self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
        except:
            print("Sorry, But looks like there is no file")

    def add_password(self, site, password):
        self.password_dict[site] = password
        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                files = f.read()
                if len(files)<8:
                    print("Password muust be of minimum 8 characters.")
                else:
                    encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                    f.write(f"{site}:{encrypted}\n")

    def get_password(self, site):
        return self.password_dict.get(site, "Password not found.")
