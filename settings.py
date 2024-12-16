import json
import requests


class SettingsManager:
    def __init__(self, settings_file = "config.json"):
        self.settings_file = settings_file
        self.settings = {}
        self.load_settings()
    
    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            print("Settings file not found. Using default settings.")
    

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get_user_settings(self):
        return self.settings["user-defined"]    
    
    def get_settings_entry(self, key):
        return self.settings.get(key)
    
    def set_settings_entry(self, key, value):
        self.settings["user-defined"][key] = value
        self.save_settings()
        return value

    def load_settings_from_url(self,url):
        if(url.startswith("http")):
            try:
                r = requests.get(url)
                self.settings = r.json()
            except requests.exceptions.RequestException as e:
                print("Error loading settings file:", e)
        else:
            try:
                with open(url, 'r') as f:
                    self.settings = json.load(f)
                self.save_settings()
            except FileNotFoundError:
                print("Settings file not found. Using default settings.")





def RunSettingsPrompt(sm:SettingsManager):
    backup = sm.settings.copy()
    while True:
        print()
        print("Settings Manager:")
        print("1. View Settings")
        print("2. Edit Settings Entry")
        print("3. Add Settings Entry")
        print("4. Delete Settings Entry")
        print("5. Load Settings from URL")
        print("6. Save and Go Back")
        print("7. Go Back without Saving")
        choice = input("Enter choice: ").strip().lower()
        if(choice == "1"):
            print("\nUser Settings:")
            for i in sm.settings["user-defined"]:
                print(f"{i}: {sm.settings["user-defined"][i]}")
        elif(choice == "2"):
            key = input("Enter key to edit: ")
            value = input("Enter new value: ")
            sm.settings["user-defined"][key] = value
        elif(choice == "3"):
            key = input("Enter key to edit: ")
            value = input("Enter new value: ")
            sm.settings["user-defined"][key] = value
        elif(choice == "4"):
            key = input("Enter key to delete: ")
            a = input(f"Are you sure you want to delete {key}? (y/n) ")
            if(a == "y"):
                del sm.settings["user-defined"][key]
            else:
                print("Deletion cancelled.")
        elif(choice == "5"):
            url = input("Enter URL to load settings from: ")
            sm.load_settings_from_url(url)
        elif(choice == "6"):
            sm.save_settings()
            print()
            break
            
        elif(choice == "7"):
            sm.settings = backup
            print()
            break
            
        else:
            print("Invalid choice. Please try again.")

