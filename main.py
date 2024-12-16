from manager import PasswordManager
import asyncio
import sys


async def setTimeOut(prompt,timeout):
    try:
        print(prompt, end="")
        userInp = await asyncio.wait_for(asyncio.to_thread(input), timeout)
        return userInp
    except asyncio.TimeoutError:
        print("Timeout. Goodbye!")
        sys.exit()
        return None
    
async def main():
    password = {
        "gmail": "password1",
        "facebook": "password2",
        "twitter": "password3"
    }
    
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
    pm = PasswordManager()
    while not done:
        choice = await setTimeOut("Enter your choice: ", 10)
        if choice == '1':
            path = await setTimeOut("Enter key file path: ", 10)
            pm.create_key(path)
        elif choice == '2':
            path = await setTimeOut("Enter key file path: ", 10)
            pm.load_key(path)
        elif choice == '3':
            path = await setTimeOut("Enter password file path: ", 10)
            pm.create_password_file(path, password)
        elif choice == '4':
            path = await setTimeOut("Enter password file path: ", 10)
            pm.load_password_file(path)
        elif choice == '5':
            site = await setTimeOut("Enter site: ", 10)
            password = await setTimeOut("Enter password: ", 10)
            pm.add_password(site, password)
        elif choice == '6':
            site = await setTimeOut("Enter site: ", 10)
            print(f"Password for {site}: {pm.get_password(site)}")
        elif choice == 'q':
            done = True
            print("Goodbye!")
        else:
            print("Invalid choice. Please try again.")
if __name__ == '__main__':
    main()
    asyncio.run(main())
