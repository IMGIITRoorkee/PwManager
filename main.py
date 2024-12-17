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
            generatePassword = input("Do you want to generate a password? (y/n): ").strip().lower()
            if generatePassword == 'y':
                site = input("Enter site: ").strip()
                length = 0
                while length <= 8:
                    length = int(input("Enter password length: ").strip().lower())
                

                strength = input("Enter password strength (good, strong, verystrong): ").strip().lower()
                password = pm.generatePassword(length,strength)
                print(f"Generated password: {password}")
                pm.add_password(site, password)
            elif generatePassword == 'n':
                site = input("Enter site: ").strip()
                password = input("Enter password: ").strip()
                if pm.validate_strength(password) in ['very strong', 'strong', 'good']:
                    print("added successfully")
                else:
                    print("WARNING: This password is weak, It is recommended to set a stronger password")
                    print("- Password should be more than 8 characters long")
                    print("- Password may have alphanumeric characters, capital letters and special characters")
                    print("if trouble choosing a password, you can generate a random password")
            pm.add_password(site, password)
                
        elif choice == '6':
            site = input("Enter site: ").strip()
            print(f"Password for {site}: {pm.get_password(site)}")
        elif choice == 'q':
            done = True
            print("Goodbye!")
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
