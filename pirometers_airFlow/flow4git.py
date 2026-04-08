import stderr_patch
from opcua import Client
import customtkinter as ctk

url = "opc.tcp://<IP ADDRESS>:<PORT>"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

#window
root = ctk.CTk()
root.title('Air Flow Meters')
root.geometry("660x570")

def refresh_uv1():
    try:
        client = Client(url)
        client.connect()
        print("Connected to opc")
    except Exception as err:
        print("Error:", err)

    ventuv1a_node = client.get_node("ns=2;s=aaaaaaa")
    ventuv1_value = ventuv1a_node.get_value()
    ventuv1_value = round(ventuv1_value, 2)
    #
    labeluv1_a.delete(0,20)
    labeluv1_a.insert(0, ventuv1_value)
    ##
    ventuv1b_node = client.get_node("ns=2;s=bbbbbbbbbbbbbb")
    ventuv1b_value = ventuv1b_node.get_value()
    ventuv1b_value = round(ventuv1b_value, 2)
    #
    labeluv1_b.delete(0,20)
    labeluv1_b.insert(0, ventuv1b_value)

    client.disconnect()
    print("Disonnected from opc")

def refresh_uv2():
    try:
        client = Client(url)
        client.connect()
        print("Connected to opc")
    except Exception as err:
        print("Error:", err)

    ventuv2a_node = client.get_node("ns=2;s=cccccccccccccccccccc")
    ventuv2a_value = ventuv2a_node.get_value()
    ventuv2a_value = round(ventuv2a_value, 2)
    #
    labeluv2_a.delete(0,20)
    labeluv2_a.insert(0, ventuv2a_value)
    ##
    ventuv2b_node = client.get_node("ns=2;s=dddddddddddddddddddddd")
    ventuv2b_value = ventuv2b_node.get_value()
    ventuv2b_value = round(ventuv2b_value, 2)
    #
    labeluv2_b.delete(0,20)
    labeluv2_b.insert(0, ventuv2b_value)

    client.disconnect()
    print("Disonnected from opc")

def refresh_uv3():
    try:
        client = Client(url)
        client.connect()
        print("Connected to opc")
    except Exception as err:
        print("Error:", err)

    ventuv3a_node = client.get_node("ns=2;s=eeeeeeeeeeeeeeeeeeeeeeeee")
    ventuv3a_value = ventuv3a_node.get_value()
    ventuv3a_value = round(ventuv3a_value, 2)
    #
    labeluv3_a.delete(0,20)
    labeluv3_a.insert(0, ventuv3a_value)

    client.disconnect()
    print("Disonnected from opc")

def refresh_uv4():
    try:
        client = Client(url)
        client.connect()
        print("Connected to opc")
    except Exception as err:
        print("Error:", err)

    ventuv4a_node = client.get_node("ns=2;s=ffffffffffffffffffffff")
    ventuv4a_value = ventuv4a_node.get_value()
    ventuv4a_value = round(ventuv4a_value, 2)
    #
    labeluv4_a.delete(0,20)
    labeluv4_a.insert(0, ventuv4a_value)
    ##
    ventuv4b_node = client.get_node("ns=2;s=gggggggggggggggggggggg")
    ventuv4b_value = ventuv4b_node.get_value()
    ventuv4b_value = round(ventuv4b_value, 2)
    #
    labeluv4_b.delete(0,20)
    labeluv4_b.insert(0, ventuv4b_value)

    client.disconnect()
    print("Disonnected from opc")

def refresh_wsl():
    try:
        client = Client(url)
        client.connect()
        print("Connected to opc")
    except Exception as err:
        print("Error:", err)
    ##
    ventwsla_node = client.get_node("ns=2;s=hhhhhhhhhhhhhhhhhhhhhhhhh")
    ventwsla_value = ventwsla_node.get_value()
    ventwsla_value = round(ventwsla_value, 2)
    #
    labelwsl_a.delete(0,20)
    labelwsl_a.insert(0, ventwsla_value)
    ##
    ventwslb_node = client.get_node("ns=2;s=iiiiiiiiiiiiiiiiiiiiiii")
    ventwslb_value = ventwslb_node.get_value()
    ventwslb_value = round(ventwslb_value, 2)
    #
    labelwsl_b.delete(0,20)
    labelwsl_b.insert(0, ventwslb_value)
    ##
    ventwslc_node = client.get_node("ns=2;s=jjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
    ventwslc_value = ventwslc_node.get_value()
    ventwslc_value = round(ventwslc_value, 2)
    #
    labelwsl_c.delete(0,20)
    labelwsl_c.insert(0, ventwslc_value)
    ##
    ventwsld_node = client.get_node("ns=2;s=kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
    ventwsld_value = ventwsld_node.get_value()
    ventwsld_value = round(ventwsld_value, 2)
    #
    labelwsl_d.delete(0,20)
    labelwsl_d.insert(0, ventwsld_value)
    ##
    ventwsle_node = client.get_node("ns=2;s=lllllllllllllllllllllllllllll")
    ventwsle_value = ventwsle_node.get_value()
    ventwsle_value = round(ventwsle_value, 2)
    #
    labelwsl_e.delete(0,20)
    labelwsl_e.insert(0, ventwsle_value)
    ##
    ventwslf_node = client.get_node("ns=2;s=mmmmmmmmmmmmmmmmmmmmmmmmmmm")
    ventwslf_value = ventwslf_node.get_value()
    ventwslf_value = round(ventwslf_value, 2)
    #
    labelwsl_f.delete(0,20)
    labelwsl_f.insert(0, ventwslf_value)

    client.disconnect()
    print("Disonnected from opc")

def refresh_esl():
    try:
        client = Client(url)
        client.connect()
        print("Connected to opc")
    except Exception as err:
        print("Error:", err)
    ##
    ventesla_node = client.get_node("ns=2;s=nnnnnnnnnnnnnnnnnnnnnnnnnnnn")
    ventesla_value = ventesla_node.get_value()
    ventesla_value = round(ventesla_value, 2)
    #
    labelesl_a.delete(0,20)
    labelesl_a.insert(0, ventesla_value)
    ##
    venteslb_node = client.get_node("ns=2;s=oooooooooooooooooooooooooo")
    venteslb_value = venteslb_node.get_value()
    venteslb_value = round(venteslb_value, 2)
    #
    labelesl_b.delete(0,20)
    labelesl_b.insert(0, venteslb_value)
    ##
    venteslc_node = client.get_node("ns=2;s=ppppppppppppppppppppppppp")
    venteslc_value = venteslc_node.get_value()
    venteslc_value = round(venteslc_value, 2)
    #
    labelesl_c.delete(0,20)
    labelesl_c.insert(0, venteslc_value)
    ##
    ventesld_node = client.get_node("ns=2;s=qqqqqqqqqqqqqqqqqqqqqqqq")
    ventesld_value = ventesld_node.get_value()
    ventesld_value = round(ventesld_value, 2)
    #
    labelesl_d.delete(0,20)
    labelesl_d.insert(0, ventesld_value)
    ##
    ventesle_node = client.get_node("ns=2;s=rrrrrrrrrrrrrrrrrrrrrr")
    ventesle_value = ventesle_node.get_value()
    ventesle_value = round(ventesle_value, 2)
    #
    labelesl_e.delete(0,20)
    labelesl_e.insert(0, ventesle_value)
    ##
    venteslf_node = client.get_node("ns=2;s=ssssssssssssssssssssssssssss")
    venteslf_value = venteslf_node.get_value()
    venteslf_value = round(venteslf_value, 2)
    #
    labelesl_f.delete(0,20)
    labelesl_f.insert(0, venteslf_value)
    ##
    venteslg_node = client.get_node("ns=2;s=tttttttttttttttttttttttttttt")
    venteslg_value = venteslg_node.get_value()
    venteslg_value = round(venteslg_value, 2)
    #
    labelesl_g.delete(0,20)
    labelesl_g.insert(0, venteslg_value)
    ##
    venteslh_node = client.get_node("ns=2;s=uuuuuuuuuuuuuuuuuuuuuuuuuuu")
    venteslh_value = venteslh_node.get_value()
    venteslh_value = round(venteslh_value, 2)
    #
    labelesl_h.delete(0,20)
    labelesl_h.insert(0, venteslh_value)

    client.disconnect()
    print("Disonnected from opc")


frame = ctk.CTkFrame(master=root)    
frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

label = ctk.CTkLabel(master=frame, text="PRZEPŁYWOMIERZE", compound="center", anchor="center")
label.grid(row=0, column=1, columnspan=3)

# #UV1
labeluv1 = ctk.CTkLabel(master=frame, text="UV1", compound="center", anchor="center")
labeluv1.grid(row=1, column=0, columnspan=2)

labeluv1_a = ctk.CTkLabel(master=frame, text="Pezepływomierz 1 na UV1:      ", compound="center", anchor="center")
labeluv1_a.grid(row=2, column=0)
labeluv1_a = ctk.CTkEntry(master=frame)
labeluv1_a.grid(row=2, column=1)

labeluv1_b = ctk.CTkLabel(master=frame, text="Pezepływomierz 2 na UV1:      ", compound="center", anchor="center")
labeluv1_b.grid(row=3, column=0)
labeluv1_b = ctk.CTkEntry(master=frame)
labeluv1_b.grid(row=3, column=1)

button_uv1= ctk.CTkButton(master=frame, text="Refresh", command=refresh_uv1)
button_uv1.grid(row=4, column=0, columnspan=2)

# #UV2
labeluv2 = ctk.CTkLabel(master=frame, text="UV2", compound="center", anchor="center")
labeluv2.grid(row=1, column=3, columnspan=2)

labeluv2_a = ctk.CTkLabel(master=frame, text="  Pezepływomierz 1 na UV2:      ", compound="center", anchor="center")
labeluv2_a.grid(row=2, column=3)
labeluv2_a = ctk.CTkEntry(master=frame)
labeluv2_a.grid(row=2, column=4)

labeluv2_b = ctk.CTkLabel(master=frame, text="  Pezepływomierz 2 na UV2:      ", compound="center", anchor="center")
labeluv2_b.grid(row=3, column=3)
labeluv2_b = ctk.CTkEntry(master=frame)
labeluv2_b.grid(row=3, column=4)

button_uv2= ctk.CTkButton(master=frame, text="Refresh", command=refresh_uv2)
button_uv2.grid(row=4, column=3, columnspan=2)

#UV3
labeluv3 = ctk.CTkLabel(master=frame, text="UV3", compound="center", anchor="center")
labeluv3.grid(row=5, column=0, columnspan=2)

labeluv3_a = ctk.CTkLabel(master=frame, text="Pezepływomierz na UV3:      ", compound="center", anchor="center")
labeluv3_a.grid(row=6, column=0)
labeluv3_a = ctk.CTkEntry(master=frame)
labeluv3_a.grid(row=6, column=1)

button_uv3= ctk.CTkButton(master=frame, text="Refresh", command=refresh_uv3)
button_uv3.grid(row=8, column=0, columnspan=2)

# #UV4
labeluv4 = ctk.CTkLabel(master=frame, text="UV4", compound="center", anchor="center")
labeluv4.grid(row=5, column=3, columnspan=2)

labeluv4_a= ctk.CTkLabel(master=frame, text="  Pezepływomierz 1 na UV4:      ", compound="center", anchor="center")
labeluv4_a.grid(row=6, column=3)
labeluv4_a = ctk.CTkEntry(master=frame)
labeluv4_a.grid(row=6, column=4)

labeluv4_b= ctk.CTkLabel(master=frame, text="  Pezepływomierz 2 na UV4:      ", compound="center", anchor="center")
labeluv4_b.grid(row=7, column=3)
labeluv4_b = ctk.CTkEntry(master=frame)
labeluv4_b.grid(row=7, column=4)

button_uv4= ctk.CTkButton(master=frame, text="Refresh", command=refresh_uv4)
button_uv4.grid(row=8, column=3, columnspan=2)


# #WSL
labelwsl = ctk.CTkLabel(master=frame, text="WSL", compound="center", anchor="center")
labelwsl.grid(row=9, column=0, columnspan=2)

labelwsl_a = ctk.CTkLabel(master=frame, text="Przepływomierz 1 na WSL:      ", compound="center", anchor="center")
labelwsl_a.grid(row=10, column=0)
labelwsl_a = ctk.CTkEntry(master=frame)
labelwsl_a.grid(row=10, column=1)

labelwsl_b = ctk.CTkLabel(master=frame, text="Przepływomierz 2 na WSL:      ", compound="center", anchor="center")
labelwsl_b.grid(row=11, column=0)
labelwsl_b = ctk.CTkEntry(master=frame)
labelwsl_b.grid(row=11, column=1)

labelwsl_c = ctk.CTkLabel(master=frame, text="Przepływomierz 3 na WSL:      ", compound="center", anchor="center")
labelwsl_c.grid(row=12, column=0)
labelwsl_c = ctk.CTkEntry(master=frame)
labelwsl_c.grid(row=12, column=1)

labelwsl_d = ctk.CTkLabel(master=frame, text="Przepływomierz 4 na WSL:      ", compound="center", anchor="center")
labelwsl_d.grid(row=13, column=0)
labelwsl_d = ctk.CTkEntry(master=frame)
labelwsl_d.grid(row=13, column=1)

labelwsl_e = ctk.CTkLabel(master=frame, text="Przepływomierz 5 na WSL:      ", compound="center", anchor="center")
labelwsl_e.grid(row=14, column=0)
labelwsl_e = ctk.CTkEntry(master=frame)
labelwsl_e.grid(row=14, column=1)

labelwsl_f = ctk.CTkLabel(master=frame, text="Przepływomierz 6 na WSL:      ", compound="center", anchor="center")
labelwsl_f.grid(row=15, column=0)
labelwsl_f = ctk.CTkEntry(master=frame)
labelwsl_f.grid(row=15, column=1)

button_wsl= ctk.CTkButton(master=frame, text="Refresh", command=refresh_wsl)
button_wsl.grid(row=18, column=0, columnspan=2)

#ESL
labelesl = ctk.CTkLabel(master=frame, text="ESL", compound="center", anchor="center")
labelesl.grid(row=9, column=3, columnspan=2)

labelesl_a = ctk.CTkLabel(master=frame, text="  Przepływomierz 1 na ESL:      ", compound="center", anchor="center")
labelesl_a.grid(row=10, column=3)
labelesl_a = ctk.CTkEntry(master=frame)
labelesl_a.grid(row=10, column=4)

labelesl_b = ctk.CTkLabel(master=frame, text="  Przepływomierz 2 na ESL:      ", compound="center", anchor="center")
labelesl_b.grid(row=11, column=3)
labelesl_b = ctk.CTkEntry(master=frame)
labelesl_b.grid(row=11, column=4)

labelesl_c = ctk.CTkLabel(master=frame, text="  Przepływomierz 3 na ESL:      ", compound="center", anchor="center")
labelesl_c.grid(row=12, column=3)
labelesl_c = ctk.CTkEntry(master=frame)
labelesl_c.grid(row=12, column=4)

labelesl_d = ctk.CTkLabel(master=frame, text="  Przepływomierz 4 na ESL:      ", compound="center", anchor="center")
labelesl_d.grid(row=13, column=3)
labelesl_d = ctk.CTkEntry(master=frame)
labelesl_d.grid(row=13, column=4)

labelesl_e = ctk.CTkLabel(master=frame, text="  Przepływomierz 5 na ESL:      ", compound="center", anchor="center")
labelesl_e.grid(row=14, column=3)
labelesl_e = ctk.CTkEntry(master=frame)
labelesl_e.grid(row=14, column=4)

labelesl_f = ctk.CTkLabel(master=frame, text="  Przepływomierz 6 na ESL:      ", compound="center", anchor="center")
labelesl_f.grid(row=15, column=3)
labelesl_f = ctk.CTkEntry(master=frame)
labelesl_f.grid(row=15, column=4)

labelesl_g = ctk.CTkLabel(master=frame, text="  Przepływomierz 7 na ESL:      ", compound="center", anchor="center")
labelesl_g.grid(row=16, column=3)
labelesl_g = ctk.CTkEntry(master=frame)
labelesl_g.grid(row=16, column=4)

labelesl_h = ctk.CTkLabel(master=frame, text="  Przepływomierz 8 na ESL:      ", compound="center", anchor="center")
labelesl_h.grid(row=17, column=3)
labelesl_h = ctk.CTkEntry(master=frame)
labelesl_h.grid(row=17, column=4)

button_wsl= ctk.CTkButton(master=frame, text="Refresh", command=refresh_esl)
button_wsl.grid(row=18, column=3, columnspan=2)

#run
root.mainloop()