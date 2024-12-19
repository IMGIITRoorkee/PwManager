from cryptography.fernet import Fernet
import re

class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}
        self.keyloaded = False

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)
        self.keyloaded = True

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()
        self.keyloaded = True


    def create_password_file(self, path, initial_values=None):
        self.password_file = path
        if initial_values is not None:
            for site in initial_values:
                print(initial_values[site])
                self.add_password(site, initial_values[site])

    def load_password_file(self, path):
        self.password_file = path
        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, site, password):

        strength_check = self.check_password_strength(password)
        if "Weak" in strength_check:
            print(strength_check)
            return  # Exit if the password is weak

        self.password_dict[site] = password
        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                f.write(f"{site}:{encrypted}\n")

    def get_password(self, site):
        return self.password_dict.get(site, "Password not found.")


    def check_password_strength(self, password):
        """Check the strength of a password."""
        if len(password) < 8:
            return "Weak: Password must be at least 8 characters long."
        if not re.search(r"[a-z]", password):
            return "Weak: Password must contain at least one lowercase letter."
        if not re.search(r"[A-Z]", password):
            return "Weak: Password must contain at least one uppercase letter."
        if not re.search(r"[0-9]", password):
            return "Weak: Password must contain at least one digit."
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return "Weak: Password must contain at least one special character."
        
        return "Strong: Password meets all criteria."
