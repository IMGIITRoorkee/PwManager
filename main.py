from manager import PasswordManager
import pyperclip




def validate_key_loaded(pm : PasswordManager):
    if not pm.keyloaded:
        print("Key not loaded. Please load a key first.")
        return False
    return True

def main():
    password = {
        "gmail": "password1",
        "facebook": "password2",
        "twitter": "password3"
    }
    
    pm = PasswordManager()

    print("""What would you like to do?
          1. Create a new key
          2. Load an existing key
          3. Create a new password file
          4. Load an existing password file
          5. Add a password
          6. Get a password
          7. List all sites
          q. Quit
          """)
    
    done = False
    while not done:
        choice = input("Enter choice: ").strip().lower()
        if choice == '1':
            path = input("Enter key file path: ").strip()
            pm.create_key(path)
        elif choice == '2':
            path = input("Enter key file path: ").strip()
            pm.load_key(path)
        elif choice == '3' and validate_key_loaded(pm):
            path = input("Enter password file path: ").strip()
            pm.create_password_file(path, password)
        elif choice == '4' and validate_key_loaded(pm):
            path = input("Enter password file path: ").strip()
            pm.load_password_file(path)
        elif choice == '5' and validate_key_loaded(pm):
            site = input("Enter site: ").strip()
            password = input("Enter password: ").strip()
            if pm.validate_strength(password):
                print("added successfully")
            else:
                print("WARNING: This password is weak, It is recommended to set a stronger password")
                print("- Password should be more than 8 characters long")
                print("- Password should have alphanumeric characters, capital letters and special characters")
            pm.add_password(site, password)

        elif choice == '6' and validate_key_loaded(pm):

            site = input("Enter site: ").strip()
            print(f"Password for {site}: {pm.get_password(site)}")
        elif choice == '10':
            path = input("Enter CSV file path for backup: ").strip()
            pm.export_to_CSV(path) 
            res = pm.get_password(site)
            print(f"Password for {site}: {res}")
            if(res != "Password not found."):
                pyperclip.copy(pm.get_password(site))
                print("Password copied to clipboard.")

        elif choice == '7':
            print("Saved Sites:")
            for site in pm.password_dict:
                print(site)
        elif choice == 'q':
            done = True
            print("Goodbye!")
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
