from tkinter import *
from tkinter import ttk,filedialog,messagebox
from manager import PasswordManager

password = {
        "gmail": "password1",
        "facebook": "password2",
        "twitter": "password3"
    }

pm = PasswordManager()
root = Tk()
siteVar = StringVar()
passVar = StringVar()



def save_file(filetypes):
        # File save dialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".key",
            filetypes=[
                filetypes
            ]
        )

        if filename:
            return filename
def selectDirectory(fileName,filetypes):
    filename = filedialog.askopenfilename(
            title=f"Open a {fileName} file",
            initialdir="/",
            filetypes=[
                filetypes
            ]
        )
    if filename:
        return filename

def remove_widget(row, column):
    for widget in root.grid_slaves():  
        if int(widget.grid_info()["row"]) == row and int(widget.grid_info()["column"]) == column:
            widget.destroy()  
            break

def makeKey():
    filename = save_file(("key Files", "*.key"))
    pm.create_key(filename)
    messagebox.showinfo("Key saved", f"Key saved to {filename}")

def loadKey():    
    path = selectDirectory("key",("key Files", "*.key"))
    print(path)
    pm.load_key(path)
    messagebox.showinfo("Key loaded", f"Key loaded from {path}")

def makePassFile():
    fileName = save_file(("password file", "*.txt"))
    pm.create_password_file(fileName,password)
    messagebox.showinfo("Password file created", f"Password file created at {fileName}")

def loadPassFile():
    path = selectDirectory("password file",("password file", "*.txt"))
    pm.load_password_file(path=path)
    messagebox.showinfo("Password file loaded", f"Password file loaded from {path}")

def createPass():
    pm.add_password(siteVar.get(),passVar.get())
    messagebox.showinfo("Password created", f"Password created for {siteVar.get()}")

def getPass():
    messagebox.showinfo("Password retrieved", f"Password retrieved for {siteVar.get()} and the password is {pm.get_password(siteVar.get())}")


def pmManager():

    for col in range(4):
        remove_widget(3,col)
        remove_widget(4,col)
    choice = choiceVar.get()
    if choice == '1':
        pathLabel = ttk.Label(root,text="save your key file: ")
        pathButton = ttk.Button(root,text="save",command=makeKey)
        pathLabel.grid(column=0,row=3)
        pathButton.grid(column=1,row=3)
    elif choice == '2':
        pathLabel = ttk.Label(root,text="select key file : ")
        pathButton = ttk.Button(root,text="select",command=loadKey)
        pathLabel.grid(column=0,row=3)
        pathButton.grid(column=1,row=3)
    elif choice == '3':
        pathLabel = ttk.Label(root,text="make a password file: ")
        pathButton = ttk.Button(root,text="make",command=makePassFile)
        pathLabel.grid(column=0,row=3)
        pathButton.grid(column=1,row=3)
    elif choice == '4':
        pathLabel = ttk.Label(root,text="select password file: ")
        pathButton = ttk.Button(root,text="select",command=loadPassFile)
        pathLabel.grid(column=0,row=3)
        pathButton.grid(column=1,row=3)
    elif choice == '5':
        siteLabel = ttk.Label(root,text="Enter site: ")
        siteEntry = ttk.Entry(root,textvariable=siteVar)
        siteLabel.grid(column=0,row=3)
        siteEntry.grid(column=1,row=3)
        passwordLabel = ttk.Label(root,text="Enter password: ")
        passwordEntry = ttk.Entry(root,textvariable=passVar)
        passButton = ttk.Button(root,text="submit",command=createPass)
        passwordLabel.grid(column=0,row=4)
        passwordEntry.grid(column=1,row=4)
        passButton.grid(column=2,row=4)   
    elif choice == '6':
        siteLabel = ttk.Label(root,text="Enter site: ")
        siteEntry = ttk.Entry(root,textvariable=siteVar)
        siteButton = ttk.Button(root,text="submit",command=getPass)
        siteLabel.grid(column=0,row=3)
        siteEntry.grid(column=1,row=3)
        siteButton.grid(column=2,row=3)
    else:
        pass




frm = ttk.Frame(root,padding=10)
frm.grid()
root.title("Password Manager")

choiceVar = StringVar()

ttk.Label(frm,text="Welcome to the Password Manager").grid(column=0,row=0)
ttk.Button(frm,text="Exit",command=root.destroy).grid(column=0,row=2)
ttk.Button(frm,text="Choice",command=pmManager).grid(column=0,row=1)
choiceLabel = ttk.Entry(root,textvariable=choiceVar)
choiceLabel.grid(column=0,row=2)

print(TkVersion,TclVersion)
root.mainloop()
