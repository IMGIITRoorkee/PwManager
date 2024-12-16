from cryptography.fernet import Fernet
import random
import string

class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}
        #TODO:need to load a config for passgen from settings once settings pr gets approved
        self.passgen = PasswordGenerator()


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
        if(password==""):
            password = self.passgen.generate_password()
        self.password_dict[site] = password
        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                f.write(f"{site}:{encrypted}\n")

    def get_password(self, site):
        return self.password_dict.get(site, "Password not found.")




class PasswordGenerator():
    def __init__(self,config={"length": 11, "numbers": True, "symbols": True, "uppercase": True, "lowercase": True, "pronouncable_words": True}):
        with open('wordlist.txt') as f:
            self.words = f.readlines()
        self.config = config
        self.length = config['length']
        self.numbers = config['numbers']
        self.special_characters = config['symbols']
        self.uppercase = config['uppercase']
        self.lowercase = config['lowercase']
        self.pronouncable_words = config['pronouncable_words']

    def __generate_random_password(self,custom_length=None):
        temp = self.length

        if custom_length:
            self.length = custom_length
        characters = string.ascii_letters
        if self.numbers:
            characters += string.digits
        if self.special_characters:
            characters += string.punctuation

        password = ''.join(random.choice(characters) for i in range(self.length))
        self.length = temp
        return password

    def __generate_pronouncable_password(self):
        password = ''.join(random.choice(self.words).strip() for _ in range(self.length // 4))
        if self.length % 4 != 0:
            password += self.__generate_random_password(self.length % 4)

        return password

    def generate_password(self):
        if self.pronouncable_words:
            return self.__generate_pronouncable_password()
        else:
            return self.__generate_random_password()
        