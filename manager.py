from cryptography.fernet import Fernet


class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}
    # Checks if keys and passwords are present or not and prompts to do so if not before
    def is_key(self):
        if (self.key is not None):
            return True
        else:
            print("Create/Add a key file first!")
            return False
    def is_file(self):
        if (self.password_file is not None):
            return True
        else:
            print("Create/Add a password file first!")
            return False

    
    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()

    def create_password_file(self, path, initial_values=None):
        if(self.is_key()):
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
        if(self.is_file() and self.is_key()): 
            with open(self.password_file, 'a+') as f:
                if site not in self.password_dict.keys():
                    self.password_dict[site] = password
                    encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                    f.write(f"{site}:{encrypted}\n")
                    print(f"Password for {site} added")
                else:
                    print(f"site: {site} is already present!")
                    print("No changes made!")
        else:
            print("Error Occured: Password not added!")

    def rename_site(self, site, new_site):

        if site in self.password_dict:
            # Rename the site in the dictionary
            self.password_dict[new_site] = self.password_dict.pop(site)
            # Update the password file if it exists
            if self.password_file is not None:
                with open(self.password_file, 'r+') as f:
                    lines = f.readlines()
                    f.seek(0)
                    for line in lines:
                        # Replace the old site name with the new one in the file
                        if site in line:
                            line = line.replace(site, new_site)
                        f.write(line)
                    f.truncate()  # Remove any remaining characters after the last line
        else:
            print("Site not found.")

    def get_password(self, site):
        return self.password_dict.get(site, "Password not found.")

