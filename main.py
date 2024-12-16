from manager import PasswordManager

def print_user_guide():
    print("""
    📚 === Password Manager User Guide === 📚

    This Password Manager allows you to securely store and retrieve your passwords using encryption.
    Follow the instructions below to use the application effectively.

    Options Menu:
    1. 🗝️  Create a New Key:
       - This option generates a new encryption key and saves it to a file.
       - Use this if you don't have an existing key.
       - Example: Enter '1' and provide a file path (e.g., 'key.key').

    2. 🔑  Load an Existing Key:
       - Load a previously created encryption key.
       - This is necessary to encrypt or decrypt passwords.
       - Example: Enter '2' and provide the path to your key file (e.g., 'key.key').

    3. 📄  Create a New Password File:
       - Create a new file to store encrypted passwords.
       - Initial passwords can be provided in the code.
       - Example: Enter '3' and provide a file path (e.g., 'passwords.txt').

    4. 📂  Load an Existing Password File:
       - Load an existing password file and decrypt stored passwords.
       - Example: Enter '4' and provide the path to your password file (e.g., 'passwords.txt').

    5. ➕  Add a Password:
       - Add a new password for a specific site.
       - The password is encrypted and stored in the password file.
       - Example: Enter '5', then provide the site name (e.g., 'github') and password (e.g., 'mypassword123').

    6. 🔍  Get a Password:
       - Retrieve a stored password for a specific site.
       - Example: Enter '6' and provide the site name (e.g., 'github').

    q. 🚪 Quit:
       - Exit the program.

    ⚠️ **Important Notes**:
    - Always **keep your key file secure**. Without the key, you cannot decrypt your passwords.
    - If you lose the key, all your stored passwords will be irrecoverable.
    - Make sure to use **strong, unique passwords** for each of your accounts.

    ============================================
    """)

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
          7. Print User Guide
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
            print_user_guide()
        elif choice == 'q':
            done = True
            print("Goodbye!")
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
