from manager import PasswordManager
from settings import SettingsManager


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
          7. Manage Settings
          q. Quit
          """)

    done = False
    while not done:
        choice = input("Enter choice: ").strip().lower()
        if choice == '1':
            path = input("Enter key file path: ").strip()
            if path == '':
                print("File name cannot be empty")
                continue
            pm.create_key(path)
        elif choice == '2':
            path = input("Enter key file path: ").strip()
            if path == '':
                print("File name cannot be empty")
                continue
            pm.load_key(path)
        elif choice == '3':
            path = input("Enter password file path: ").strip()
            if path == '':
                print("File name cannot be empty")
                continue
            pm.create_password_file(path, password)
        elif choice == '4':
            path = input("Enter password file path: ").strip()
            if path == '':
                print("File name cannot be empty")
                continue
            pm.load_password_file(path)
        elif choice == '5':
            site = input("Enter site: ").strip()
            password = input("Enter password: ").strip()
            pm.add_password(site, password)
        elif choice == '6':
            site = input("Enter site: ").strip()
            print(f"Password for {site}: {pm.get_password(site)}")
        elif choice == '7':
            print("Settings Menu:")
            print("1. View Settings")
            print("2. Update Setting")
            print("3. Delete Setting")
            setting_choice = input("Enter choice: ").strip()

            if setting_choice == '1':
                settings = SettingsManager.list_all()
                print("Current Settings:", settings)
            elif setting_choice == '2':
                key = input("Enter setting name: ").strip()
                value = input("Enter setting value: ").strip()
                SettingsManager.set(key, value)
                print(f"Setting '{key}' updated.")
            elif setting_choice == '3':
                key = input("Enter setting name to delete: ").strip()
                SettingsManager.delete(key)
                print(f"Setting '{key}' deleted.")
            else:
                print("Invalid choice.")
        elif choice == 'q':
            done = True
            print("Goodbye!")
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
