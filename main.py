from manager import PasswordManager  # Importing the PasswordManager class to handle password operations


def main():
    # Initial set of passwords for testing (will be added to the password file)
    password = {
        "gmail": "password1",
        "facebook": "password2",
        "twitter": "password3"
    }
    
    pm = PasswordManager()  # Creating an instance of PasswordManager to manage passwords

    # Displaying a menu of options to the user
    print("""What would you like to do?
          1. Create a new key
          2. Load an existing key
          3. Create a new password file
          4. Load an existing password file
          5. Add a password
          6. Get a password
          q. Quit
          """)
    
    done = False  # Variable to control the loop and terminate the program when set to True
    while not done:
        # Asking the user to input their choice from the menu
        choice = input("Enter choice: ").strip().lower()
        
        if choice == '1':
            # Creating a new key and saving it to the user-specified path
            path = input("Enter key file path: ").strip()
            pm.create_key(path)
        elif choice == '2':
            # Loading an existing key from the user-specified path
            path = input("Enter key file path: ").strip()
            pm.load_key(path)
        elif choice == '3':
            # Creating a new password file with initial passwords
            path = input("Enter password file path: ").strip()
            pm.create_password_file(path, password)
        elif choice == '4':
            # Loading an existing password file
            path = input("Enter password file path: ").strip()
            pm.load_password_file(path)
        elif choice == '5':
            # Adding a new password for a site
            site = input("Enter site: ").strip()
            password = input("Enter password: ").strip()
            pm.add_password(site, password)
        elif choice == '6':
            # Retrieving a stored password for a site
            site = input("Enter site: ").strip()
            print(f"Password for {site}: {pm.get_password(site)}")
        elif choice == 'q':
            # Exiting the program
            done = True
            print("Goodbye!")
        else:
            # Handling invalid choices from the menu
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()  # Running the main function when the script is executed
