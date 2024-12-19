from database import Password, Key
from cryptography.fernet import Fernet


class PasswordManager:
    def __init__(self, session, user):
        self.session = session
        self.user = user
        self.key = None

    def load_key(self, key_id):
        key = self.session.query(Key).filter_by(key_id=key_id, user_id=self.user.user_id).first()
        if key:
            self.key = key.key_value.encode()
            print(f"Key {key.key_id} selected successfully.")
            return True
        else:
            print("Invalid key ID. Please try again.")
            return False

    def add_new_key(self):
        new_key_value = Fernet.generate_key().decode()
        new_key = Key(key_value=new_key_value, user_id=self.user.user_id)
        self.session.add(new_key)
        self.session.commit()
        print(f"New key created successfully! Key ID: {new_key.key_id}")

    def add_password(self, site, password_value):
        if not self.key:
            print("No key selected. Please select a key first.")
            return
        encrypted_password = Fernet(self.key).encrypt(password_value.encode()).decode()
        new_password = Password(
            site=site,
            password_value=encrypted_password,
            key_id=self.get_current_key_id(),
            user_id=self.user.user_id
        )
        self.session.add(new_password)
        self.session.commit()
        print("Password added successfully.")

    def get_password(self, site):
        password_entry = self.session.query(Password).filter_by(site=site, user_id=self.user.user_id).order_by(Password.created_date.desc()).first()
        if password_entry:
            key_entry = self.session.query(Key).filter_by(key_id=password_entry.key_id).first()
            fernet = Fernet(key_entry.key_value.encode())
            decrypted_password = fernet.decrypt(password_entry.password_value.encode()).decode()
            return decrypted_password
        else:
            return "Password not found."

    def get_current_key_id(self):
        if not self.key:
            return None
        key = self.session.query(Key).filter_by(key_value=self.key.decode()).first()
        return key.key_id
    
    def list_keys(self):
        keys = self.session.query(Key).filter_by(user_id=self.user.user_id).all()
        if not keys:
            print("No keys available. Please create a new key.")
        else:
            print("Available Keys:")
            for idx, key in enumerate(keys):
                print(f"{idx + 1}. Key ID: {key.key_id}")
        return keys
    
    def list_sites(self):
        passwords = self.session.query(Password).filter_by(user_id=self.user.user_id).all()
        passwords = set([password.site for password in passwords])
        if not passwords:
            print("No passwords stored yet.")
        else:
            print("Stored Sites:")
            for idx, password in enumerate(passwords):
                print(f"{idx + 1}. {password}")
