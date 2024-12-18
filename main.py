from manager import PasswordManager
from cloud_manager import CloudManager


def main():
    password = {
        "gmail": "password1",
        "facebook": "password2",
        "twitter": "password3"
    }

    credentials_path = 'credentials.json'
    cloud_manager = CloudManager(credentials_path)
    pm = PasswordManager(cloud_manager)

    print("""What would you like to do?
          1. Create a new key
          2. Load an existing key
          3. Create a new password file
          4. Load an existing password file
          5. Add a password
          6. Get a password
          7. Upload password file to cloud
          8. Download password file from cloud
          q. Quit
          """)

    while True:
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
            pm.upload_password_file()
        elif choice == '8':
            file_name = input("Enter the file name to download: ").strip()
            pm.download_password_file(file_name)
        elif choice == 'q':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()