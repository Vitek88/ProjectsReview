import sys, os
from customtkinter import *
from customtkinter import filedialog
import paramiko
from tkinter import messagebox

def resource(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def popup():
    response = messagebox.askquestion(title="Warning!!!",message="Are you sure that you wanted to reboot all machines on the list?")
    #print(response)
    if response == "yes":
        try :
            reboot()
        except Exception as err:
            messagebox.showerror(title="Error!",message=err)

    

def reboot():
    global terminal
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(servers)
    file = open(servers, "r")
    for line in file:
        try:
            z = line.split(" ")
            var = z[0]
            terminal = var
            client.connect(var, username='<USERNAME>',password="<PASSWORD>") # type name and password
            stdin, stdout, stderr = client.exec_command('sudo reboot') #command to execute
            for line in stdout:
                print (line.strip('\n'))
            client.close()
        except TimeoutError as err:
            messagebox.showerror(title="Lack of connection", message=terminal + " not responding...")
        except Exception as err:
            messagebox.showerror(title="Error", message=err)
    client.close()

def openFile():
    global servers
    root.filename = filedialog.askopenfilename(initialdir=" ", title="Choose a file with a servers list...", filetypes=(("Servers","*.txt"),("All files", "*.*")))
    servers = root.filename
    label1 = CTkLabel(root, text=root.filename)
    label1.pack()
image = resource("<ICON DIR>") # put an icon dir path
print(image)
root = CTk()
root.title("OpenThinClient Restarter")
root.geometry("350x100")
root.iconbitmap(image)


importButton = CTkButton(root, text="Import...", command=openFile).pack()
linia = CTkLabel(root, text=" ").pack()
button = CTkButton(root, text="Reboot!",command=popup).pack()

root.mainloop()