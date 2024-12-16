import os  # Allows user to interact with the operating system
from manager import PasswordManager

"""The entire code now follows python's PEP 8 standard"""
def clear_screen():
    """Clears the CLI screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Main function to handle the password manager operations."""
    passwords = {
        "gmail": "password1",
        "facebook": "password2",
        "twitter": "password3"
    }

    pm = PasswordManager()

    menu = (
        "What would you like to do?\n"
        "1. Create a new key\n"
        "2. Load an existing key\n"
        "3. Create a new password file\n"
        "4. Load an existing password file\n"
        "5. Add a password\n"
        "6. Get a password\n"
        "c. Clear Screen\n"
        "q. Quit\n"
    )

    print(menu)

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
            pm.create_password_file(path, passwords)
        elif choice == '4':
            path = input("Enter password file path: ").strip()
            pm.load_password_file(path)
        elif choice == '5':
            site = input("Enter site: ").strip()
            password = input("Enter password: ").strip()
            pm.add_password(site, password)
        elif choice == '6':
            site = input("Enter site: ").strip()
            retrieved_password = pm.get_password(site)
            print(f"Password for {site}: {retrieved_password}")
        elif choice == 'c':
            clear_screen()
            print(menu)
            print("Cleared the screen.")
        elif choice == 'q':
            done = True
            print("Goodbye!")
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
