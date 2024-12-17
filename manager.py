from cryptography.fernet import Fernet
import os

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
    def validate_strength(self, password):
        # a password is strong if it has length greater than 8
        # it has special characters such as !@#$%^&*
        # it is a mix of letters, numbers
        SpecialChar = '!@#$%^&*'
        has_good_length = False
        has_special_char = False
        has_numeric_characters = False
        has_capital_letters = False
        has_small_letters = False
        if len(password) > 8: 
            has_good_length = True
        for chr in password:
            if chr in SpecialChar:
                has_special_char = True
            if chr.isupper():
                has_capital_letters = True
            if chr.islower():
                has_small_letters = True
            if chr.isdigit():
                has_numeric_characters = True
        return has_numeric_characters and has_good_length and\
              has_capital_letters and has_special_char and has_small_letters
    def reEncrypt(self, path):
        if self.key is None:
            raise Exception("KeyNotLoadedError")

        old_key = self.key
        self.create_key(path)

        temp_file_path = self.password_file + '.tmp'
        

        with open(self.password_file, 'r') as orig_file, \
             open(temp_file_path, 'w') as temp_file:

            for line in orig_file:
                site, encrypted_password = line.strip().split(':')
                decrypted_password = Fernet(old_key).decrypt(encrypted_password.encode()).decode()
                new_encrypted_password = Fernet(self.key).encrypt(decrypted_password.encode()).decode()
                
                temp_file.write(f"{site}:{new_encrypted_password}\n")


        os.replace(temp_file_path, self.password_file)
        
        print("Passwords re-encrypted successfully with new key.")

