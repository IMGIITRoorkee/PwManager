import json
import os


class SettingsManager:
    SETTINGS_FILE = "settings.json"
    
    @staticmethod
    def _load_settings():
        """Load settings from the file."""
        if os.path.exists(SettingsManager.SETTINGS_FILE):
            with open(SettingsManager.SETTINGS_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    @staticmethod
    def _save_settings(settings):
        """Save settings to the file."""
        with open(SettingsManager.SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
    
    @classmethod
    def get(cls, key, default=None):
        """Fetch a setting by key."""
        settings = cls._load_settings()
        return settings.get(key, default)
    
    @classmethod
    def set(cls, key, value):
        """Set or update a setting."""
        settings = cls._load_settings()
        settings[key] = value
        cls._save_settings(settings)
    
    @classmethod
    def delete(cls, key):
        """Delete a setting by key."""
        settings = cls._load_settings()
        if key in settings:
            del settings[key]
            cls._save_settings(settings)
    
    @classmethod
    def list_all(cls):
        """List all settings."""
        return cls._load_settings()
