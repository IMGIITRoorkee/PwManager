from flask import Flask, request, jsonify

from manager import PasswordManager

app = Flask(__name__)
pm = PasswordManager()

@app.route('/create_key', methods=['POST'])
def create_key():
    path = request.json.get('path')
    if not path:
        return jsonify({"error": "Path is required!"}), 400
    pm.create_key(path)
    return jsonify({"message": "Key file created successfully!"}), 200

@app.route('/load_key', methods=['POST'])
def load_key():
    path = request.json.get('path')
    if not path:
        return jsonify({"error": "Path is required!"}), 400
    try:
        pm.load_key(path)
        return jsonify({"message": "Key loaded successfully!"}), 200
    except FileNotFoundError:
        return jsonify({"error": "Key file not found!"}), 404

@app.route('/create_password_file', methods=['POST'])
def create_password_file():
    path = request.json.get('path')
    initial_values = {
        "gmail": "password1",
        "facebook": "password2",
        "twitter": "password3"
    }
    pm.create_password_file(path, initial_values)
    return jsonify({"message": "Password file created successfully"}), 200

@app.route('/load_password_file', methods=['POST'])
def load_password_file():
    path = request.json.get('path')
    try:
        pm.load_password_file(path)
        return jsonify({"message": "Password file loaded successfully"}), 200
    except FileNotFoundError:
        return jsonify({"error": "Password file not found"}), 404

@app.route('/add_password', methods=['POST'])
def add_password():
    site = request.json.get('site')
    password = request.json.get('password')
    if not site or not password:
        return jsonify({"error": "Site and password are required"}), 400
    pm.add_password(site, password)
    return jsonify({"message": f"Password for {site} added successfully"}), 200

@app.route('/get_password/<site>', methods=['GET'])
def get_password(site):
    password = pm.get_password(site)
    if password == "Password not found.":
        return jsonify({"error": password}), 404
    return jsonify({"site": site, "password": password}), 200

app.run(debug=True)