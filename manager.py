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

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()

    def create_password_file(self, path, initial_values=None):
        self.password_file = path
        if initial_values is not None:
            for site, (password, expiry_date) in initial_values.items():
                self.add_password(site, password, expiry_date)

    def load_password_file(self, path):
        self.password_file = path
        with open(path, 'r') as f:
            for line in f:
                site, encrypted, expiry_date = line.strip().split(":")
                decrypted_password = Fernet(self.key).decrypt(encrypted.encode()).decode()
                self.password_dict[site] = (decrypted_password, expiry_date)

    def add_password(self, site, password, expiry_date):
        
        if self._is_expired(expiry_date):
            print(f"The password for {site} has already expired.")
            self.handle_expired_password(site, password, expiry_date)
            return

        self.password_dict[site] = (password, expiry_date)
        if self.password_file is not None:
            try:
                with open(self.password_file, 'a+') as f:
                    encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                    f.write(f"{site}:{encrypted}:{expiry_date}\n")
                print(f"Password for {site} added successfully.")
            except Exception as e:
                print(f"Error writing to password file: {e}")

    def get_password(self, site):
        if site not in self.password_dict:
            return "Password not found."

        # Handle expired passwords
        password_data = self.password_dict[site]
        if isinstance(password_data, tuple):  # To check if expiry date is present
            password, expiry_date = password_data
            if self._is_expired(expiry_date):
                print(f"The password for {site} has expired.")
                self.handle_expired_password(site, password, expiry_date)
                return "Password has expired and is no longer available."
        else:
            password = password_data  # If no expiry date, just return password

        return password

    def validate_strength(self, password):
        # A password is strong if it has length > 8, special chars, numbers, and mixed-case letters
        special_chars = '!@#$%^&*'
        has_good_length = len(password) > 8
        has_special_char = any(char in special_chars for char in password)
        has_numeric_characters = any(char.isdigit() for char in password)
        has_capital_letters = any(char.isupper() for char in password)
        has_small_letters = any(char.islower() for char in password)

        return (has_good_length and has_special_char and 
                has_numeric_characters and has_capital_letters and has_small_letters)

    def handle_expired_password(self, site, password=None, expiry_date=None):
        user_choice = input("Would you like to update (u) or remove (r) it? ").strip().lower()
        if user_choice == 'u':
            new_password = input("Enter new password: ").strip()
            new_expiry = input("Enter new expiration date (YYYY-MM-DD): ").strip()
            if self.validate_strength(new_password):
                if not self._is_expired(new_expiry):
                    self.add_password(site, new_password, new_expiry)
                else:
                    print("New expiration date is also invalid. No changes made.")
            else:
                print("Password is too weak. Update aborted.")
        elif user_choice == 'r':
            self.password_dict.pop(site, None)
            self._rewrite_password_file()
            print(f"Password for {site} has been removed.")
        else:
            print("Invalid choice. No changes made.")

    def _rewrite_password_file(self):
        if self.password_file is not None:
            with open(self.password_file, 'w') as f:
                for site, data in self.password_dict.items():
                    if isinstance(data, tuple):  # Handle expiry date
                        password, expiry_date = data
                        encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                        f.write(f"{site}:{encrypted}:{expiry_date}\n")
                    else:
                        password = data
                        encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                        f.write(f"{site}:{encrypted}\n")

    def _is_expired(self, expiry_date):
        try:
            expiry_date_obj = datetime.strptime(expiry_date, "%Y-%m-%d").date()
            current_date = datetime.now().date()
            return expiry_date_obj < current_date
        except ValueError:
            print("Invalid date format encountered in _is_expired.")
            return True  # Treat invalid dates as expired

