from cryptography.fernet import Fernet


class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.numberoffolders=-1
        self.currentfolder=0
        self.folder=[]
        self.password_dict = {}
        self.folder_dict={}
        isFolder=False
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
                site, encrypted = line.strip().split(":")
                if(site=="folder"):
                    self.folder.append(encrypted)
                    self.numberoffolders=self.numberoffolders+1
                    self.currentfolder=self.numberoffolders
                    self.folder_dict[encrypted]=0
                    isFolder=True
                elif(isFolder):
                    self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
                    self.folder_dict[self.folder[self.numberoffolders]]=self.folder_dict[self.folder[self.numberoffolders]]+1
                else:
                    self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
    def add_folder(self, name):
        self.folder.append(name)
        self.numberoffolders=self.numberoffolders+1
        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = name
                f.write(f"folder:{encrypted}\n")
        self.currentfolder=self.numberoffolders
        self.folder_dict[name]=0
    def access_folder(self, path):
        t=0
        for i in range (len(self.folder)):
            if(self.folder[i]==path):
                self.currentfolder=i
                t=1
        if(t==0):
            print("folder not found")
        
    def add_password(self, site, password):
        if site in self.password_dict:  
            print(f"Warning: A password for the site '{site}' already exists.")  
            return 
        self.password_dict[site] = password
        if self.password_file is not None:
            if (self.currentfolder==self.numberoffolders):
                with open(self.password_file, 'a+') as f:
                    encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                    f.write(f"{site}:{encrypted}\n")
                    self.folder_dict[self.folder[self.numberoffolders]]=self.folder_dict[self.folder[self.numberoffolders]]+1
            else:
                with open(self.password_file, 'r') as f:
                    lines=f.readlines()
                    f.close()
                with open(self.password_file, 'w') as f:
                    count=0
                    l=0
                    for k in range(self.currentfolder+1):
                        l+=self.folder_dict[self.folder[k]]
                        l+=1
                    for line in lines:
                        if(count<l):
                            f.write(line)
                            count+=1
                        elif(count==l):
                            encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                            f.write(f"{site}:{encrypted}\n")
                            count+=1
                            f.write(line)
                        else :
                            f.write(line)

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

