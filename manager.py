from cryptography.fernet import Fernet


class PasswordManager:
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        """Generates and saves a new key to the specified path."""
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        """Loads the key from the specified path."""
        with open(path, 'rb') as f:
            self.key = f.read()

    def create_password_file(self, path, initial_values=None):
        """Creates a password file and optionally adds initial passwords."""
        self.password_file = path
        if initial_values is not None:
            for site, password in initial_values.items():
                self.add_password(site, password)

    def load_password_file(self, path):
        """Loads passwords from a file and decrypts them."""
        self.password_file = path
        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(
                    encrypted.encode()).decode()

    def add_password(self, site, password):
        """Adds a password for a site, ensuring it is at least 8 characters long."""
        while len(password) < 8:  # Ensures that password is at least 8 characters long
            print("Error: Password must be at least 8 characters long.")
            password = input("Please enter a valid password: ").strip()  # Will continue prompting user
        self.password_dict[site] = password
        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                f.write(f"{site}:{encrypted}\n")

    def get_password(self, site):
        """Returns the password for a site, or a message if not found."""
        return self.password_dict.get(site, "Password not found.")
