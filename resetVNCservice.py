import tkinter as tk
from tkinter import messagebox
import paramiko
import os

# dane logowania do SSH
SSH_USER = os.environ["ssh_user"]       
SSH_PASS = os.environ["ssh_pass"]      
SSH_PORT = 22

# komendy do restartu VNC
PID_COMMAND = "ps aux | grep x11vnc | grep 5900 | awk '{print $2}'"
KILL_COMMAND = "kill -9 {pid}"
START_COMMAND = "killall x11vnc && x11vnc --forever --shared"

def restart_vnc(ip_address):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip_address, port=SSH_PORT, username=SSH_USER, password=SSH_PASS, timeout=10)

        # znajdź PID procesu x11vnc
        stdin, stdout, stderr = ssh.exec_command(PID_COMMAND)
        pid = stdout.read().decode().strip()

        if pid:
            # zabij proces jeśli istnieje
            ssh.exec_command(KILL_COMMAND.format(pid=pid))

        # uruchom ponownie usługę
        ssh.exec_command(START_COMMAND)

        ssh.close()

        messagebox.showinfo("Success", "VNC service has been restarted.")

    except Exception:
        # pokaż błąd tylko w przypadku problemów z połączeniem
        messagebox.showerror("Error", "Failed to connect to the device.")

def on_restart_click():
    ip = ip_entry.get().strip()
    if not ip:
        messagebox.showwarning("No IP provided", "Please provide the device IP address!")
        return
    restart_vnc(ip)

# GUI
root = tk.Tk()
root.title("Restart VNC Service")
root.geometry("350x150")

label = tk.Label(root, text="Input device IP address:")
label.pack(pady=5)

ip_entry = tk.Entry(root, width=30)
ip_entry.pack(pady=5)

restart_button = tk.Button(root, text="Restart VNC service", command=on_restart_click, bg="lightblue")
restart_button.pack(pady=20)

root.mainloop()
