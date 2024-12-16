from manager import PasswordManager  


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
          7. Usage Guide
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
        elif choice == '3':
            path = input("Enter password file path: ").strip()
            pm.create_password_file(path, password)
        elif choice == '4':
            path = input("Enter password file path: ").strip()
            pm.load_password_file(path)
        elif choice == '5':
            site = input("Enter site: ").strip()
            password = input("Enter password: ").strip()
            pm.add_password(site, password)
        elif choice == '6':
            site = input("Enter site: ").strip()
            print(f"Password for {site}: {pm.get_password(site)}")
        elif choice == '7':
            print("""
            Usage Guide:
            1. Create a new key: Generates a new encryption key and saves it to a file.
            2. Load an existing key: Loads a previously generated encryption key from a file.
            3. Create a new password file: Creates a password file and adds a few default passwords.
            4. Load an existing password file: Loads an existing password file to access encrypted passwords.
            5. Add a password: Adds a new password to the password file for a specific site.
            6. Get a password: Retrieves the password for a given site from the password file.
            7. Usage Guide: Displays this usage guide to help you understand how to use the program.
            q. Quit: Exits the program.
            """)
        elif choice == 'q':
            done = True
            print("Goodbye!")
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
