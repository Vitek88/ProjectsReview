import stderr_patch
from opcua import Client
import customtkinter as ctk

url = "opc.tcp://<IP ADDRESS>:<PORT>" # OPC connection specify

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")



try:
    client = Client(url)

    client.connect()

except Exception as err:
    print("Error:", err)
    
#window
root = ctk.CTk()
root.title('Pirometers')
root.geometry("320x300")

def refresh():
    try:
        client = Client(url)
        client.connect()

    except Exception as err:
        print("Error:", err)

    pirouv1_node = client.get_node("ns=2;s=aaaaaaaaaaaa")
    pirouv1_value = pirouv1_node.get_value()
    pirouv1_value = round(pirouv1_value, 2)
    labeluv1_a.delete(0,20)
    labeluv1_a.insert(0, pirouv1_value)

    pirouv2_node = client.get_node("ns=2;s=bbbbbbbbbbbbbb")
    pirouv2_value = pirouv2_node.get_value()
    pirouv2_value = round(pirouv2_value, 2)
    labeluv2_a.delete(0,20)
    labeluv2_a.insert(0, pirouv2_value)

    pirouv3_node = client.get_node("ns=2;s=cccccccccccccccccc")
    pirouv3_value = pirouv3_node.get_value()
    pirouv3_value = round(pirouv3_value, 2)
    labeluv3_a.delete(0,20)
    labeluv3_a.insert(0, pirouv3_value)
    
    pirouv4_node = client.get_node("ns=2;s=dddddddddddddddddd")
    pirouv4_value = pirouv4_node.get_value()
    pirouv4_value = round(pirouv4_value, 2)
    labeluv4_a.delete(0,20)
    labeluv4_a.insert(0, pirouv4_value)
    
    pirowsl_node = client.get_node("ns=2;s=eeeeeeeeeeeeee")
    pirowsl_value = pirowsl_node.get_value()
    pirowsl_value = round(pirowsl_value, 2)
    labelwsl_a.delete(0,20)
    labelwsl_a.insert(0, pirowsl_value)

    client.disconnect()

    

frame = ctk.CTkFrame(master=root)    
frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

label = ctk.CTkLabel(master=frame, text="PIROMETRY", compound="center", anchor="center")
label.grid(row=0, column=0, columnspan=3 )

#UV1
labeluv1 = ctk.CTkLabel(master=frame, text="Pirometr na UV1:      ", compound="center", anchor="center")
labeluv1.grid(row=1, column=0)
labeluv1_a = ctk.CTkEntry(master=frame)
labeluv1_a.grid(row=1, column=1)

#UV2
labeluv2 = ctk.CTkLabel(master=frame, text="Pirometr na UV2:      ", compound="center", anchor="center")
labeluv2.grid(row=2, column=0)
labeluv2_a = ctk.CTkEntry(master=frame)
labeluv2_a.grid(row=2, column=1)

#UV3
labeluv3 = ctk.CTkLabel(master=frame, text="Pirometr na UV3:      ", compound="center", anchor="center")
labeluv3.grid(row=3, column=0)
labeluv3_a = ctk.CTkEntry(master=frame)
labeluv3_a.grid(row=3, column=1)

#UV4
labeluv4= ctk.CTkLabel(master=frame, text="Pirometr na UV4:      ", compound="center", anchor="center")
labeluv4.grid(row=4, column=0)
labeluv4_a = ctk.CTkEntry(master=frame)
labeluv4_a.grid(row=4, column=1)

#WSL
labelwsl = ctk.CTkLabel(master=frame, text="Pirometr na WSL:      ", compound="center", anchor="center")
labelwsl.grid(row=5, column=0)
labelwsl_a = ctk.CTkEntry(master=frame)
labelwsl_a.grid(row=5, column=1)

button= ctk.CTkButton(master=frame, text="Refresh", command=refresh)
button.grid(row=6, column=0, columnspan=2)

#run
root.mainloop()