# Password Manager for MergeFest Event

A **CLI-based password manager** built in Python for secure password storage and management.

---

## Project Structure

```
/
├── main.py      # Entry point for executing the program
├── manager.py   # Core logic and functionality
```

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
Visit the **htmlcss** channel and ping `2Y` for assistance.  

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
    pip install cryptography
    ```  

5. **Run the Application**:  
    ```bash
    python3 main.py
    ```  

---

## Features  

- **Encrypt and Store Passwords**: Securely save your credentials.  
- **Key Management**: Generate and load encryption keys.  
- **File-Based Storage**: Organize passwords in a file.  

---

## Requirements  

- **Python**: Version 3.x or higher.  
- **Library**: `cryptography`  

---

## How to Use  

1. **Start the Program**:  
    ```bash
    python3 main.py
    ```  

2. **Menu Options**:  
    - `1`: Create a new encryption key.  
    - `2`: Load an existing encryption key.  
    - `3`: Create a new password file.  
    - `4`: Load an existing password file.  
    - `5`: Add a new password to the file.  
    - `6`: Retrieve a password from the file.  
    - `q`: Quit the application.  

---

## Example Usage  

### Create a New Key  

```bash
Enter choice: 1
Enter key file path: keyfile.key
```  

### Add a New Password  

```bash
Enter choice: 5
Enter site: github
Enter password: securepassword123
```  

### Retrieve a Password  

```bash
Enter choice: 6
Enter site: github
Password for github is securepassword123
```  

---

## Security Note  

- **Keep Your Encryption Key Safe**:  
  The encryption key is crucial for accessing your passwords. Losing it means your passwords cannot be decrypted.  
