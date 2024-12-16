from cryptography.fernet import Fernet


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
            for site, data in initial_values.items():
                self.add_password(site, data["password"], data.get("category"))

    def load_password_file(self, path):
        self.password_file = path
        with open(path, 'r') as f:
            for line in f:
                site, encrypted, category = line.strip().split(":")
                password = Fernet(self.key).decrypt(encrypted.encode()).decode()
                self.password_dict[site] = {"password": password, "category": category}

    def add_password(self, site, password, category="uncategorized"):
        self.password_dict[site] = {"password": password, "category": category}
        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode()).decode()
                f.write(f"{site}:{encrypted}\n")

    def get_password(self, site):
        data = self.password_dict.get(site)
        if data:
            return f"Password: {data['password']}, Category: {data['category']}"
        return "Password not found."

    def list_passwords_by_category(self):
        selected_category = input("Enter the category you want to view: ").strip()
        found = False
        for site, data in self.password_dict.items():
            if data["category"] == selected_category:
                if not found:
                    print(f"\nCategory: {selected_category}")
                    found = True
                print(f"{site}: {data['password']}")
        if not found:
            print(f"No passwords found for category: {selected_category}")
