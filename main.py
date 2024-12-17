from tkinter import *
from tkinter import ttk
from manager import PasswordManager

password = {
        "gmail": "password1",
        "facebook": "password2",
        "twitter": "password3"
    }


pm = PasswordManager()
root = Tk()

pathVar = StringVar()
siteVar = StringVar()
passVar = StringVar()

def remove_widget(row, column):
    for widget in root.grid_slaves():  
        if int(widget.grid_info()["row"]) == row and int(widget.grid_info()["column"]) == column:
            widget.destroy()  
            break

def makeKey():
    pm.create_key(pathVar.get())

def loadKey():    
    pm.load_key(pathVar.get())

def makePassFile():
    pm.create_password_file(pathVar.get(),password)

def loadPassFile():
    pm.load_password_file(pathVar.get())

def createPass():
    pm.add_password(siteVar.get(),passVar.get())

def getPass():
    siteLabel = ttk.Label(root,text=f"password for {str(siteVar.get())}: {pm.get_password(siteVar.get())}")
    siteLabel.grid(column=0,row=3)

def pmManager():

    for col in range(3):
        print(col)
        remove_widget(2,col)
        remove_widget(3,col)
    choice = choiceVar.get()
    if choice == '1':
        pathLabel = ttk.Label(root,text="Enter key file path: ")
        pathEntry = ttk.Entry(root,textvariable=pathVar)
        pathButton = ttk.Button(root,text="submit",command=makeKey)
        pathLabel.grid(column=0,row=2)
        pathEntry.grid(column=1,row=2)
        pathButton.grid(column=2,row=2)
    elif choice == '2':
        pathLabel = ttk.Label(root,text="Enter key file path: ")
        pathEntry = ttk.Entry(root,textvariable=pathVar)
        pathButton = ttk.Button(root,text="submit",command=loadKey)
        pathLabel.grid(column=0,row=2)
        pathEntry.grid(column=1,row=2)
        pathButton.grid(column=2,row=2)
    elif choice == '3':
        pathLabel = ttk.Label(root,text="Enter password file path: ")
        pathEntry = ttk.Entry(root,textvariable=pathVar)
        pathButton = ttk.Button(root,text="submit",command=makePassFile)
        pathLabel.grid(column=0,row=2)
        pathEntry.grid(column=1,row=2)
        pathButton.grid(column=2,row=2)
    elif choice == '4':
        pathLabel = ttk.Label(root,text="Enter password file path: ")
        pathEntry = ttk.Entry(root,textvariable=pathVar)
        pathButton = ttk.Button(root,text="submit",command=loadPassFile)
        pathLabel.grid(column=0,row=2)
        pathEntry.grid(column=1,row=2)
        pathButton.grid(column=2,row=2)
    elif choice == '5':
        siteLabel = ttk.Label(root,text="Enter site: ")
        siteEntry = ttk.Entry(root,textvariable=siteVar)
        siteLabel.grid(column=0,row=2)
        siteEntry.grid(column=1,row=2)
        passwordLabel = ttk.Label(root,text="Enter password: ")
        passwordEntry = ttk.Entry(root,textvariable=passVar)
        passButton = ttk.Button(root,text="submit",command=createPass)
        passwordLabel.grid(column=0,row=3)
        passwordEntry.grid(column=1,row=3)
        passButton.grid(column=2,row=3)   
    elif choice == '6':
        siteLabel = ttk.Label(root,text="Enter site: ")
        siteEntry = ttk.Entry(root,textvariable=siteVar)
        siteButton = ttk.Button(root,text="submit",command=getPass)
        siteLabel.grid(column=0,row=2)
        siteEntry.grid(column=1,row=2)
        siteButton.grid(column=2,row=2)
    else:
        pass




frm = ttk.Frame(root,padding=10)
frm.grid()

choiceVar = StringVar()

# ttk.Label(frm,text="Hello World!").grid(column=0,row=0)
ttk.Button(frm,text="Exit",command=root.destroy).grid(column=1,row=0)
ttk.Button(frm,text="Choice",command=pmManager).grid(column=0,row=0)
choiceLabel = ttk.Entry(root,textvariable=choiceVar)
choiceLabel.grid(column=0,row=1)

root.mainloop()
