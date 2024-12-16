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

        password, expiry_date = self.password_dict[site]
        if self._is_expired(expiry_date):
            print(f"The password for {site} has expired.")
            self.handle_expired_password(site, password, expiry_date)
            return "Password has expired and is no longer available."
        return password
    
    def handle_expired_password(self, site, password=None, expiry_date=None):
        user_choice = input("Would you like to update (u) or remove (r) it? ").strip().lower()
        if user_choice == 'u':
            new_password = input("Enter new password: ").strip()
            new_expiry = input("Enter new expiration date (YYYY-MM-DD): ").strip()
            if not self._is_expired(new_expiry):
                self.add_password(site, new_password, new_expiry)
            else:
                print("New expiration date is also invalid. No changes made.")
        elif user_choice == 'r':
            self.password_dict.pop(site, None)
            self._rewrite_password_file()
            print(f"Password for {site} has been removed.")
        else:
            print("Invalid choice. No changes made.")

    def _rewrite_password_file(self):
        if self.password_file is not None:
            with open(self.password_file, 'w') as f:
                for site, (password, expiry_date) in self.password_dict.items():
                    encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                    f.write(f"{site}:{encrypted}:{expiry_date}\n")

    def _is_expired(self, expiry_date):
        try:
            expiry_date_obj = datetime.strptime(expiry_date, "%Y-%m-%d").date()
            current_date = datetime.now().date()
            is_expired = expiry_date_obj < current_date
            return is_expired
        except ValueError:
            print("Invalid date format encountered in _is_expired.")
            return True  # Treat invalid dates as expired