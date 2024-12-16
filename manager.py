from cryptography.fernet import Fernet


class PasswordManager:
    """
    A class to manage passwords securely using encryption.
    """

    def __init__(self):
        """
        Initializes the manager with no key, no file, and an empty password list.
        """
        self.key = None  # No encryption key initially
        self.password_file = None  # No file for passwords yet
        self.password_dict = {}  # Empty dictionary to store passwords

    def create_key(self, path):
        """
        Creates and saves a new encryption key to a file.
        Args:
            path (str): The path to save the key.
        """
        self.key = Fernet.generate_key()  # Generate a new key
        with open(path, 'wb') as f:
            f.write(self.key)  # Save the key to the file

    def load_key(self, path):
        """
        Loads an existing encryption key from a file.
        Args:
            path (str): The path to the key file.
        """
        with open(path, 'rb') as f:
            self.key = f.read()  # Load the key from the file

    def create_password_file(self, path, initial_values=None):
        """
        Creates a password file and adds initial passwords if given.
        Args:
            path (str): The path for the password file.
            initial_values (dict, optional): Initial site-password pairs to add.
        """
        self.password_file = path  # Set the file path
        if initial_values is not None:
            for site, password in initial_values.items():
                self.add_password(site, password)  # Add initial passwords

    def load_password_file(self, path):
        """
        Loads passwords from a file and decrypts them.
        Args:
            path (str): The password file path.
        """
        self.password_file = path  # Set the file path
        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.strip().split(":")  # Split the site and encrypted password
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()  # Decrypt and store the password

    def add_password(self, site, password):
        """
        Adds a new password for a site. Warns if the site already exists.
        Args:
            site (str): The site name.
            password (str): The password for the site.
        """
        if site in self.password_dict:
            print(f"Warning: '{site}' already has a password.")  # Warn if site already exists
            return  # Do not add the password again

        self.password_dict[site] = password  # Add the new password

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode()).decode()  # Encrypt the password
                f.write(f"{site}:{encrypted}\n")  # Save the encrypted password to the file

    def get_password(self, site):
        """
        Gets the password for a site.
        Args:
            site (str): The site name.
        Returns:
            str: The password or a message if not found.
        """
        return self.password_dict.get(site, "Password not found.")  # Return password or 'not found'

