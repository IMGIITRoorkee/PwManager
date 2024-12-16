from manager import PasswordManager

def check_site():
    while(True):
        site = input("Enter site: ").strip()
        if(site == ""):
            print("Please enter a valid site.")
            continue
        break
    return site

def check_password():
    while(True):
        password = input("Enter password: ").strip()
        if(password == ""):
            print("Please enter a valid password.")
            continue
        break
    return password


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
            site = check_site()
            password = check_password()
            pm.add_password(site, password)
        elif choice == '6':
            site = check_site()
            print(f"Password for {site}: {pm.get_password(site)}")
        elif choice == 'q':
            done = True
            print("Goodbye!")
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
