from database import Database
from user_handler import UserHandler
from manager import PasswordManager
import pyperclip

def main():
    db = Database()
    session = db.get_session()
    user_handler = UserHandler(session)

    print("Welcome to the Multi-User Password Manager!")
    current_user = None

    while not current_user:
        print("\n1. Register\n2. Login\nq. Quit")
        choice = input("Enter choice: ").strip().lower()

        if choice == '1':
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            try:
                user_handler.register_user(username, password)
                print("Registration successful!")
            except:
                print("Username already exists. Try a different one.")

        elif choice == '2':
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            user = user_handler.authenticate_user(username, password)
            if user:
                print(f"Welcome, {username}!")
                current_user = user
            else:
                print("Invalid credentials. Please try again.")

        elif choice == 'q':
            print("Goodbye!")
            return

        else:
            print("Invalid choice. Try again.")

    pm = PasswordManager(session, current_user)

    while True:
        print("""
        1. List Available Keys
        2. Select a Key
        3. Add a New Key
        4. Add Password (Using Selected Key)
        5. Retrieve Password
        6. List Sites
        q. Quit
        """)
        choice = input("Enter choice: ").strip().lower()

        if choice == '1':
            pm.list_keys()

        elif choice == '2':
            keys = pm.list_keys()
            if keys:
                key_id = input("Enter the Key ID to select: ").strip()
                pm.load_key(key_id)

        elif choice == '3':
            pm.add_new_key()

        elif choice == '4':
            path = input("Enter password file path: ").strip()
            pm.load_password_file(path)

        elif choice == '4':
            site = input("Enter site: ").strip()
            # Password conditions
            print("Password must be at least 8 characters long.")
            print("Password must contain at least one lowercase letter.")
            print("Password must contain at least one uppercase letter.")
            print("Password must contain at least one digit.")
            print("Password must contain at least one special character.")
            
            password = input("Enter password: ").strip()
            if pm.validate_strength(password):
                print("added successfully")
            else:
                print("WARNING: This password is weak, It is recommended to set a stronger password")
                print("- Password should be more than 8 characters long")
                print("- Password should have alphanumeric characters, capital letters and special characters")
            pm.add_password(site, password)


        elif choice == '5':
            site = input("Enter site name to retrieve password: ").strip()
            password = pm.get_password(site)
            print(f"Password for {site}: {password}")

        elif choice == '6':
            pm.list_sites()

        elif choice == 'q':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
