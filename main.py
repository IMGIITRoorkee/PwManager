from database import Database
from user_handler import UserHandler
from manager import PasswordManager
import pyperclip
import platform
import sys

# Windows:
# Install the winbio library, which is a Python wrapper for the Windows Biometric Framework.
# Ensure your fingerprint device is configured in Windows Hello.

# macOS:
# Install pyobjc (pip install pyobjc).
# This script uses the LocalAuthentication framework via PyObjC.

def authenticate_windowsHello():
    try:
        import winbio  # Windows Biometric Framework library
        bio = winbio.WinBio()
        print("Place your finger on the fingerprint reader...")
        result = bio.verify()
        if result:
            print("Authentication successful!")
            return True
        else:
            print("Authentication failed.")
            return False
    except ImportError:
        print("Windows Biometric Framework (winbio) is not installed.")
        return False

def authenticate_touchId():
    try:
        import objc
        from Foundation import NSBundle
        from LocalAuthentication import LAContext, LAPolicyDeviceOwnerAuthenticationWithBiometrics
        
        context = LAContext.alloc().init()
        if context.canEvaluatePolicy_error_(LAPolicyDeviceOwnerAuthenticationWithBiometrics, None)[0]:
            success, error = context.evaluatePolicy_localizedReason_reply_(
                LAPolicyDeviceOwnerAuthenticationWithBiometrics,
                "Authenticate to proceed.",
                None
            )
            if success:
                print("Authentication successful!")
                return True
            else:
                print("Authentication failed.")
                return False
        else:
            print("Touch ID is not available on this device.")
            return False
    except ImportError:
        print("PyObjC is not installed.")
        return False

def main():
    system = platform.system()
    if system == "Windows":
        authenticated = authenticate_windowsHello()
    elif system == "Darwin":  # macOS
        authenticated = authenticate_touchId()
    else:
        print(f"Unsupported operating system: {system}")
        sys.exit(1)

    if authenticated:
        print("Running the main code...")
        db = Database()
        session = db.get_session()
        user_handler = UserHandler(session)

        print("Welcome to the Multi-User Password Manager!")
        current_user = None

        while not current_user:
            print("\n1. Register\n2. Login\nq. Quit")
            choice = input("Enter choice: ").strip().lower()

            if choice == '1':
                username = input("Enter username: ").strip()
                password = input("Enter password: ").strip()
                try:
                    user_handler.register_user(username, password)
                    print("Registration successful!")
                except:
                    print("Username already exists. Try a different one.")

            elif choice == '2':
                username = input("Enter username: ").strip()
                password = input("Enter password: ").strip()
                user = user_handler.authenticate_user(username, password)
                if user:
                    print(f"Welcome, {username}!")
                    current_user = user
                else:
                    print("Invalid credentials. Please try again.")

            elif choice == 'q':
                print("Goodbye!")
                return

            else:
                print("Invalid choice. Try again.")

        pm = PasswordManager(session, current_user)

        while True:
            print("""
            1. List Available Keys
            2. Select a Key
            3. Add a New Key
            4. Add Password (Using Selected Key)
            5. Retrieve Password
            6. List Sites
            q. Quit
            """)
            choice = input("Enter choice: ").strip().lower()

            if choice == '1':
                pm.list_keys()

            elif choice == '2':
                keys = pm.list_keys()
                if keys:
                    key_id = input("Enter the Key ID to select: ").strip()
                    pm.load_key(key_id)

            elif choice == '3':
                pm.add_new_key()

            elif choice == '4':
                path = input("Enter password file path: ").strip()
                pm.load_password_file(path)
                size = pm.get_file_size(path)
                print(f"Password file loaded successfully. The size of is {size} bytes.")
                if not pm.key:
                    print("Please select a key first.")
                    continue
                site = input("Enter site name: ").strip()
                password_value = input("Enter password: ").strip()
                pm.add_password(site, password_value)

            elif choice == '5':
                site = input("Enter site name to retrieve password: ").strip()
                password = pm.get_password(site)
                print(f"Password for {site}: {password}")

            elif choice == '6':
                pm.list_sites()
                
            elif choice == 'q':
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Try again.")
    else:
        print("Exiting due to failed authentication.")
    
if __name__ == "__main__":
    main()
