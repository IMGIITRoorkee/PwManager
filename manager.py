from cryptography.fernet import Fernet


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
        if site in self.password_dict:  
            print(f"Warning: A password for the site '{site}' already exists.")  
            return 
        while len(password) < 8: #ENSURES THAT PASSWORD IS ATLEAST 8 CHARACTERS LONG
            print("Error: Password must be at least 8 characters long.")
            password = input("Please enter a valid password: ").strip()#WILL CONTINUE PROMPTING USER TO ENTER THE PASSWORD IN THE CORRECT FORMAT
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

