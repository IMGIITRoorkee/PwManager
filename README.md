# Password Manager for MergeFest Event

A **CLI-based password manager** built in Python for secure password storage and management.

---

## Project Structure

```
/
├── main.py      # Entry point for executing the program
├── manager.py   # Core logic and functionality
├── user_handler.py   # User handling
├── database.py   # Database schema
```
### Install required dependencies:
`pip install -r requirements.txt`

---

## Built With

- **Python**: A versatile programming language.  

---

## Resources to Learn Python

- [Python Tutorial - W3Schools](https://www.w3schools.com/python/)

---

## Contributing  

Before contributing, review the following:  

1. **Rules for MergeFest**: [MergeFest Rules](https://github.com/IMGIITRoorkee/MergeFest-Hacker/blob/main/RULES.md)  
2. **Contribution Guidelines**: [How to Contribute](https://github.com/IMGIITRoorkee/MergeFest-Hacker/blob/main/CONTRIBUTORS.md)  

### Contribution Guidelines  

- **Code Style**: Follow best practices for Python coding.  
- **Readable Commits**: Write clear and descriptive commit messages.  
- **Testing**: Ensure your changes don’t break existing functionality.  
- **Proof of Work**: Attach a video showcasing the feature you implemented.  

### Looking for Guidance?

Join our **Discord server**: [MergeFest Discord](https://discord.gg/aKaEbaVYKf)  
Visit the **python** channel and ping `2Y` for assistance.  

---

## Setup Instructions  

1. **Fork the Repository** and clone it to your local machine:  
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```  

2. **Set up SSH** for GitHub to commit changes.  

3. **Ensure Python 3 is installed**:  
    ```bash
    python3 --version
    ```  

4. **Install required dependencies**:  
    ```bash
    pip install cryptography sqlalchemy
    ```  

5. **Run the Application**:  
    ```bash
    python3 main.py
    ```  

---

## Features  

- **Encrypt and Store Passwords**: Securely save your credentials.  
- **Key Management**: Generate and load encryption keys.  
- **Database-Based Storage**: Organize passwords in a database.

---

## Requirements  

- **Python**: Version 3.x or higher.  
- **Library**: `cryptography` and `sqlalchemy`

---

## How to Use  

1. **Start the Program**:  
    ```bash
    python3 main.py
    ```  

2. **Menu Options**: 

**Login Menu**
    - `1`: Register a user.  
    - `2`: Login using existing user credentials.  
    - `q`: Quit the application.  

**Application Menu**
    - `1`: List all existing keys created by a user.  
    - `2`: Load an existing encryption key.  
    - `3`: Create a new key.  
    - `4`: Add a new password to the file.  
    - `5`: Retrieve a password.  
    - `6`: List all sites for which password are saved.  
    - `q`: Quit the application.  

---

## Security Note  

- **Keep Your Encryption Key Safe**:  
  The encryption key is crucial for accessing your passwords. Losing it means your passwords cannot be decrypted.  
