from flask import Flask,request
from flask_cors import CORS
from manager import PasswordManager


app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False
password = {
        "gmail": "password1",
        "facebook": "password2",
        "twitter": "password3"
    }
    
pm = PasswordManager()


@app.route("/pasword",methods=['GET','POST'])
def password():
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice == '1':
            path = request.form.get('path')
            pm.create_key(path)
            return {
                "msg" : "key created successfully",
                "path" : path,
                "status":"success"
            }
        elif choice == '2':
            path = request.form.get('path')
            pm.load_key(path)
            return {
                "msg" : "loaded from path :" + path,
                "status" : "success",
            }
        elif choice == '3':
            path = request.form.get('path')
            pm.create_password_file(path, password)
            return {
                "status" :"success",
                "msg" : "password file created successfully",
                "path" : path
            }
        elif choice == '4':
            path = request.form.get('path')
            pm.load_password_file(path)
            return  {
                "status" : "success",
                "msg" : "password file loaded successfully",
                "path" : path
            }
        elif choice == '5':
            site = request.form.get('site')
            password = request.form.get('password')
            pm.add_password(site, password)
            return {
                "status" : "success",
                "msg" : f"password for {site} added successfully"
            }
        elif choice == '6':
            site = request.form.get('site')
            password = pm.get_password(site)
            return {
                "status" : "success",
                "msg" : f"password for {site} is {password}"
            }
            
            
            
        else:
            return {
                "status" : "the given choice is invalid",
                
            }
if __name__ == "__main__" :
    app.run()