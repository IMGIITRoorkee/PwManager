from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog, QMessageBox
from manager import PasswordManager


class PasswordManagerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.pm = PasswordManager()
        self.key_loaded = False
        self.file_loaded = False
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Password Manager")
        self.setGeometry(100, 100, 500, 500)
        self.setStyleSheet("font-family: Arial; font-size: 12pt;")
        
        self.layout = QVBoxLayout(self)

        self.step1_layout = QVBoxLayout()
        self.step1_title = QLabel("Step 1: Key Management")
        self.step1_layout.addWidget(self.step1_title)

        self.create_key_button = QPushButton("Create New Key")
        self.create_key_button.clicked.connect(self.create_key)
        self.step1_layout.addWidget(self.create_key_button)

        self.load_key_button = QPushButton("Load Existing Key")
        self.load_key_button.clicked.connect(self.load_key)
        self.step1_layout.addWidget(self.load_key_button)

        self.key_file_label = QLabel("No key file loaded.")
        self.step1_layout.addWidget(self.key_file_label)

        self.step2_layout = QVBoxLayout()
        self.step2_title = QLabel("Step 2: Password File Management")
        self.step2_layout.addWidget(self.step2_title)

        self.create_file_button = QPushButton("Create New Password File")
        self.create_file_button.clicked.connect(self.create_password_file)
        self.step2_layout.addWidget(self.create_file_button)

        self.load_file_button = QPushButton("Load Existing Password File")
        self.load_file_button.clicked.connect(self.load_password_file)
        self.step2_layout.addWidget(self.load_file_button)

        self.password_file_label = QLabel("No password file loaded.")
        self.step2_layout.addWidget(self.password_file_label)


        self.step3_layout = QVBoxLayout()
        self.step3_title = QLabel("Step 3: Manage Passwords")
        self.step3_layout.addWidget(self.step3_title)

        self.site_layout = QHBoxLayout()
        self.site_label = QLabel("Site:")
        self.site_layout.addWidget(self.site_label)

        self.site_entry = QLineEdit(self)
        self.site_layout.addWidget(self.site_entry)
        self.step3_layout.addLayout(self.site_layout)

        self.password_layout = QHBoxLayout()
        self.password_label = QLabel("Password:")
        self.password_layout.addWidget(self.password_label)

        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_layout.addWidget(self.password_entry)
        self.step3_layout.addLayout(self.password_layout)

        self.add_button = QPushButton("Add Password")
        self.add_button.clicked.connect(self.add_password)
        self.step3_layout.addWidget(self.add_button)

        self.get_button = QPushButton("Get Password")
        self.get_button.clicked.connect(self.get_password)
        self.step3_layout.addWidget(self.get_button)

        self.layout.addLayout(self.step1_layout)
        self.layout.addLayout(self.step2_layout)
        self.layout.addLayout(self.step3_layout)

        self.step2_layout.setEnabled(False)
        self.step3_layout.setEnabled(False)

    def create_key(self):
        path, _ = QFileDialog.getSaveFileName(self, "Create Key File", "", "Key Files (*.key);;All Files (*)")
        if path:
            if not path.endswith(".key"):
                path += ".key"
            self.pm.create_key(path)
            self.key_loaded = True
            self.key_file_label.setText(f"Key file loaded: {path}")
            QMessageBox.information(self, "Success", f"New key created at {path}")
            self.step2_layout.setEnabled(True)


    def load_key(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Key File", "", "Key Files (*.key);;All Files (*)")
        if path:
            self.pm.load_key(path)
            self.key_loaded = True
            self.key_file_label.setText(f"Key file loaded: {path}")
            QMessageBox.information(self, "Success", f"Key loaded successfully from {path}")
            self.step2_layout.setEnabled(True)
        else:
            self.key_loaded = False

    def create_password_file(self):
        if not self.key_loaded:
            QMessageBox.warning(self, "Error", "Please load or create a key file first!")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Create Password File", "", "Text Files (*.txt);;All Files (*)")
        if path:
            if not path.endswith(".txt"):
                path += ".txt"
            self.pm.create_password_file(path)
            self.file_loaded = True
            self.password_file_label.setText(f"Password file loaded: {path}")
            QMessageBox.information(self, "Success", f"New password file created at {path}")
            self.step3_layout.setEnabled(True)


    def load_password_file(self):
        if not self.key_loaded:
            QMessageBox.warning(self, "Error", "Please load or create a key file first!")
            return

        path, _ = QFileDialog.getOpenFileName(self, "Open Password File", "", "Text Files (*.txt);;All Files (*)")
        if path:
            self.pm.load_password_file(path)
            self.file_loaded = True
            self.password_file_label.setText(f"Password file loaded: {path}")
            QMessageBox.information(self, "Success", f"Password file loaded successfully from {path}")
            self.step3_layout.setEnabled(True)
        else:
            self.file_loaded = False

    def add_password(self):
        if not self.key_loaded or not self.file_loaded:
            QMessageBox.warning(self, "Error", "Please load or create both a key and a password file first!")
            return

        site = self.site_entry.text().strip()
        password = self.password_entry.text().strip()
        if site and password:
            self.pm.add_password(site, password)
            QMessageBox.information(self, "Success", f"Password for {site} added successfully!")
        else:
            QMessageBox.warning(self, "Error", "Both site and password fields must be filled!")

    def get_password(self):
        if not self.key_loaded or not self.file_loaded:
            QMessageBox.warning(self, "Error", "Please load or create both a key and a password file first!")
            return

        site = self.site_entry.text().strip()
        if site:
            password = self.pm.get_password(site)
            QMessageBox.information(self, "Password", f"Password for {site}: {password}")
        else:
            QMessageBox.warning(self, "Error", "Please enter a site!")

