from manager import PasswordManager
import os


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
          7. Display password file size
          8.Help
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
            if pm.password_file:
                try:
                    file_size=os.path.getsize(pm.password_file)
                    print("Password file size:", file_size,"bytes")
                except FileNotFoundError:
                    print("Password file not found.")
            else:
                print("No password file loaded.")
        elif choice=="8":
            print("""
            Choose an action:
            1. Generate a new encryption key - Create a new key to secure passwords.
            2. Load an existing encryption key - Retrieve and use an existing key to encrypt/decrypt passwords.
            3. Create a new password storage file - Initialize a fresh password file with predefined data.
            4. Load an existing password file - Open and read an already saved password file.
            5. Add a new password - Save a password for a website or service.
            6. Retrieve a password - Get the stored password for a given site.
            7. Check password file size - Display the current size of the password file.
            h. Help - Show detailed instructions for all actions available.
            q. Exit - Close the program.
            """)
        elif choice == 'q':
            done = True
            print("Goodbye!")
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
