import stderr_patch

import customtkinter
import tkinter
import mysql.connector
import datetime
from tkinter import ttk
import os

mydb = mysql.connector.connect(
    host=os.environ["HOST_ADDRESS"],           #
    user=os.environ["DB_USERNAME"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DB_INSTANCE"]
)



class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def radiobutton_event():
            self.radio_var_value = self.radio_var.get()

        def add_record():
            self.values = []
            
            if self.entryNazwa.get() == self.entryNazwa0.get():
                self.entryNazwaValue = self.entryNazwa.get()
                
                self.values.append (self.entryNazwaValue)
                self.values.append (self.radio_var_value)

                self.now = datetime.datetime.now() # time without microseconds
                self.currentTime = self.now - datetime.timedelta(microseconds=self.now.microsecond)
                
                
                try:
                    mycursor = mydb.cursor()
                    self.sql = "INSERT INTO slownik (Nazwa, Hierarchia, WlasciwoscID, Aktualny, DataModyfikacji, DataUtworzenia) VALUES(%s,%s,%s,%s,%s,%s)"
                    self.val = (self.values[0],"58", self.values[1], 1, self.currentTime, self.currentTime )
                    mycursor.execute(self.sql, self.val)
                    self.labelStatus.configure(text="Added record", text_color="green")
                    mydb.commit()

                    self.entryNazwa.delete(0,'end')
                    self.entryNazwa0.delete(0,'end')
                    self.radio_var.set("0")



                except Exception as error:
                    self.labelStatus.configure(text="An error occurred!!", text_color="red")
                    tkinter.messagebox.showerror(title="Error", message=error) #stary tkinterowy błąd
                        

                
                print(mycursor.rowcount, "record inserted")
            else:
                tkinter.messagebox.showerror(title="Error", message=f"Provided names are not identical!")
        
        self.geometry("400x500")
        self.title("Add item/pigment/color")
        self.label = customtkinter.CTkLabel(self, text="Add item/pigment/color",text_color="Orange")
        self.label.pack(padx=(20,0))

        self.labelNazwa = customtkinter.CTkLabel(self, text="Enter item/pigment/color name:")
        self.labelNazwa.pack(padx=20, pady=10)

        self.entryNazwa = customtkinter.CTkEntry(self, width=300)
        self.entryNazwa.pack(padx=20, pady=10)

        self.labelNazwa0 = customtkinter.CTkLabel(self, text="Repeat the item/pigment/color name:")
        self.labelNazwa0.pack(padx=20, pady=10)

        self.entryNazwa0 = customtkinter.CTkEntry(self, width=300)
        self.entryNazwa0.pack(padx=20, pady=10)
        #self.entryNazwaValue = self.entryNazwa.get()
     
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self, text="Color or pigment:")
        self.label_radio_group.pack(padx=10, pady=10)
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self, text="Add color", variable=self.radio_var, value=13, command=radiobutton_event)
        self.radio_button_1.pack(pady=10, padx=20)
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self, text="Add pigment", variable=self.radio_var, value=14, command=radiobutton_event)
        self.radio_button_2.pack(pady=10, padx=20)
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self, text="Add item", variable=self.radio_var, value=30, command=radiobutton_event)
        self.radio_button_3.pack(pady=10, padx=20)
        
        self.buttonConfirm = customtkinter.CTkButton(self, text = "Add...", command=add_record)
        self.buttonConfirm.pack(padx=20, pady=20)

        self.labelStatus= customtkinter.CTkLabel(self, text_color="green", text="" )
        self.labelStatus.pack()

class ToplevelWindow2(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x800")
        self.title("Add color")

        self.now = datetime.datetime.now() # time without microseconds
        self.currentTime = self.now - datetime.timedelta(microseconds=self.now.microsecond)
        dict = {}
        

        def dodajKolor():
            def is_hex(s): # check if string is in hex format
                hex_digits = set("0123456789abcdef")
                s = s.lower()
                if len(s)>6 or len(s)<6:
                    return False
                for char in s:
                 if not (char in hex_digits):
                    return False
                return True
            
            self.labelStatus.configure(text="")
            self.labelStatus2.configure(text="")

            self.entryNowaNazwaValue = self.entryNowaNazwa.get()
            self.entryKolorHexValue = self.entryKolorHex.get()
            self.hexCheck = is_hex(self.entryKolorHexValue)

            
            if is_hex(self.entryKolorHexValue):  
                
                try:
                    defaultColor = "Choose color"
                    vals = dict.values()
                    chosenVals = []
                    for element in vals:
                        chosenVals.append(element.get())
                    if defaultColor in chosenVals:
                        tkinter.messagebox.showwarning(title="WARNING!", message="Please fill in all fields!")
                    else:
                        recordcount =0
                        try:
                            mycursor0 = mydb.cursor()
                            self.sql0 = "INSERT INTO kolor (Nazwa, Hex, Aktualny, DataModyfikacji, DataUtworzenia) VALUES(%s,%s,%s,%s,%s)"
                            self.val0 = (self.entryNowaNazwaValue, self.entryKolorHexValue, 1, self.currentTime, self.currentTime)
                            mycursor0.execute(self.sql0, self.val0)
                            mydb.commit()
                            self.labelStatus.configure(text=f"Added new color '{self.entryNowaNazwaValue}' to the database", text_color="green")
                            #print("dodano kolor do bd")
                        except Exception as error:
                            self.labelStatus.configure(text=f"An error occurred!!\n {error}" , text_color="red")
                        try:
                            mycursor1 = mydb.cursor()
                            self.sql1 = f"SELECT ID FROM kolor WHERE Nazwa like '{self.entryNowaNazwaValue}'"
                            mycursor1.execute(self.sql1)
                            self.newColorIDTouple = mycursor1.fetchone()
                            self.newColorID = self.newColorIDTouple[0] ## ID nowego koloru
                            #print(self.newColorID)     
                        except Exception as error:
                            self.labelStatus.configure(text=f"An error occurred!!\n {error}" , text_color="red")        

                        for lineId in dict:

                            try:
                                self.oldColorID = 0
                                mycursor5 = mydb.cursor()
                                self.sql5 = f"SELECT ID FROM kolor WHERE Nazwa like '{dict[lineId].get()}'"
                                mycursor5.execute(self.sql5)
                                self.oldColorIDTouple = mycursor5.fetchone()
                                self.oldColorID = self.oldColorIDTouple[0] ## ID starego koloru

                            except Exception as error:
                                self.labelStatus.configure(text=f"An error occurred!!\n {error}", text_color="red")

                            mycursor = mydb.cursor()
                            self.sql = f"SELECT * FROM wartoscgraniczna WHERE KolorID like '{self.oldColorID}'AND LiniaID like '{lineId}'"
                            mycursor.execute(self.sql)
                            self.wartoscgranicznaGet = mycursor.fetchall() #fetchall / fetchone
                            recordcount = recordcount + mycursor.rowcount

                            for wartosc in self.wartoscgranicznaGet:
                                mycursor7 = mydb.cursor()
                                self.sql2 = f"INSERT INTO wartoscgraniczna \
                                    (Min, Max, LiniaID, KolorID, WlasciwoscID, LokalizacjaID, Aktualny, CzyKolorGlobalny, CzyLiniaGlobalna, MinNowy, MaxNowy, TypZmianyID, DataPublikacji) \
                                    VALUES({wartosc[1]},{wartosc[2]},{wartosc[3]},{self.newColorID},{wartosc[5]},{wartosc[6]},{wartosc[7]},{wartosc[8]}, {wartosc[9]},{wartosc[10]},{wartosc[11]},NULL,NULL)"
                                mycursor7.execute(self.sql2)
                                mydb.commit()
                                
                                self.entryNowaNazwa.delete(0,'end')
                                self.entryKolorHex.delete(0,'end')
                                
                                

                    self.labelStatus2.configure(text=f"Added {recordcount} entries to the limit values" , text_color="green")

                except Exception as error:
                    self.labelStatus.configure(text=f"Wystąpił błąd!!\n {error}", text_color="red")
            else:self.labelStatus.configure(text="Kolor nie jest w kodzie HEX", text_color="red")  


        mycursor6 = mydb.cursor()
        self.sql6 = "SELECT ID, Nazwa FROM linia"
        mycursor6.execute(self.sql6)
        self.linesWithId = mycursor6.fetchall()
        self.linesList = []
        
        for line in self.linesWithId:
            self.linesList.append(line[1])       

        mycursor7 = mydb.cursor()
        self.sql7 = "SELECT ID, Nazwa FROM kolor"
        mycursor7.execute(self.sql7)
        self.kolorsWithId = mycursor7.fetchall()
        #print(self.kolorsWithId)
        self.kolorsList = []

        for kolor in self.kolorsWithId:
            self.kolorsList.append(kolor[1])  
           

        self.labelNowaNazwa = customtkinter.CTkLabel(master=self,text= "Please enter the name of the new color:").pack(padx=20)
        self.entryNowaNazwa = customtkinter.CTkEntry(self, width=400, placeholder_text="Color name")
        self.entryNowaNazwa.pack(padx=20, pady=(0,20))

        self.labelKolorHex = customtkinter.CTkLabel(master=self,text= "Please enter the color in 'HEX' format:").pack(padx=20, pady=(20,0))
        self.entryKolorHex = customtkinter.CTkEntry(self,width=400, placeholder_text="For example: 6b92f1")
        self.entryKolorHex.pack(padx=20, pady=(0,20))

        self.labelStaraNazwa = customtkinter.CTkLabel(master=self,text= "Please enter the name of the old color from which to copy the limit values:").pack(padx=20,pady=(20,0))

        
        
        for id, lines in self.linesWithId:
            customtkinter.CTkLabel(self,text=f"From which color to copy for line {lines}?").pack(pady=5)

            dict[id] = customtkinter.StringVar(value="Select color")
            customtkinter.CTkOptionMenu(master=self, values=self.kolorsList, variable=dict[id]).pack(pady=5) 

        self.buttonSubmit = customtkinter.CTkButton(self, text="Add color...", command=dodajKolor).pack(padx=20, pady=20)

        self.labelStatus= customtkinter.CTkLabel(self, text_color="green", text="" )
        self.labelStatus.pack()

        self.labelStatus2= customtkinter.CTkLabel(self, text_color="green", text="" )
        self.labelStatus2.pack()

class ToplevelWindow3(customtkinter.CTkToplevel):
    class WszystkieLakiery(customtkinter.CTkScrollableFrame):
        def __init__(self, master, values):
            super().__init__(master)
            self.columnconfigure((0,1,2), weight=1)
            self.rowconfigure((0,1,2), weight=1)
            self.rowconfigure((3,4,5), weight=3)
            self.values = values
            self.switchboxes = []
            self.tuple_status = []
            for i, value in enumerate(self.values, start=2):

                nazwa = customtkinter.CTkLabel(self, text=value[1])
                nazwa.grid(row=i, column=0, padx=10, pady=(10, 0))

                switch_var = customtkinter.IntVar(value=value[3])
                switch = customtkinter.CTkSwitch(self, text="", variable=switch_var, onvalue=1, offvalue=0)
                switch.grid(row=i, column=1, padx=10, pady=(10, 0))
                #print(value[0], switch.get())

                data = customtkinter.CTkLabel(self, text=value[4])
                data.grid(row=i, column=2, padx=10, pady=(10, 0))

                self.tuple_status.append([value[0], switch])


        def get(self):
               
            for tuple in self.tuple_status:
                try:
                    mycursor = mydb.cursor()
                    sql = f"UPDATE slownik SET Aktualny = {tuple[1].cget('variable').get()} WHERE ID = {tuple[0]}"
                    mycursor.execute(sql)
                    mydb.commit()
                

                except Exception as error:
                    tkinter.messagebox.showerror(title="Błąd", message=error)
                    return  False

            tkinter.messagebox.showinfo(title="Success!", message="Great success!")
            
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("1200x900")
        self.title("Overview of all colors and pigments")

        mycursor0 = mydb.cursor()
        self.sql0 = f"SELECT ID, Nazwa, WlasciwoscID, Aktualny, DataUtworzenia FROM slownik WHERE WlasciwoscID like '13' OR WlasciwoscID like '14' ORDER BY Nazwa ASC"
        mycursor0.execute(self.sql0)
        wszystkieLakiery = mycursor0.fetchall()

        self.labelNazwa = customtkinter.CTkLabel(master=self,text= "Overview of all colors and pigments:")
        self.labelNazwa.pack(side="top")

        self.nameFrame =customtkinter.CTkFrame(master=self)
        self.nameFrame.pack(fill="x")

        self.labelStatus = customtkinter.CTkLabel(self.nameFrame,text= "Status:")
        self.labelStatus.pack(side="top")

        self.scrollable_checkbox_frame = self.WszystkieLakiery(master=self, values=wszystkieLakiery)
        self.scrollable_checkbox_frame.pack(side="top", fill="both", expand=True)

        self.submitButton = customtkinter.CTkButton(self, text="Submit", command=self.button_callback)
        self.submitButton.pack(side="bottom")

    def button_callback(self):
        print(f"Wartości: {self.scrollable_checkbox_frame.get()}")



class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Logbook Updater")
        self.geometry("400x400")
        

        self.label1 = customtkinter.CTkLabel(self, text="What do you want to add?", text_color="Orange")
        self.label1.pack(padx=20)

        self.button_1 = customtkinter.CTkButton(self, text="Add item/color/pigment", command=self.open_toplevel)
        self.button_1.pack(side="top", padx=20, pady=40)

        self.button_2 = customtkinter.CTkButton(self, text="Add color", command=self.open_toplevel2)
        self.button_2.pack(side="top", padx=20, pady=40)

        self.button_3 = customtkinter.CTkButton(self, text="Overview of all colors and pigments", command=self.open_toplevel3)
        self.button_3.pack(side="top", padx=20, pady=40)

        self.toplevel_window = None
        self.toplevel_window2 = None
        self.toplevel_window3 = None
        

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def open_toplevel2(self):
        if self.toplevel_window2 is None or not self.toplevel_window2.winfo_exists():
            self.toplevel_window2 = ToplevelWindow2(self)  # create window if its None or destroyed
        else:
            self.toplevel_window2.focus()  # if window exists focus it
    def open_toplevel3(self):
        if self.toplevel_window3 is None or not self.toplevel_window3.winfo_exists():
            self.toplevel_window3 = ToplevelWindow3(self)  # create window if its None or destroyed
        else:
            self.toplevel_window3.focus()  # if window exists focus it


if __name__ == "__main__":
    app = App()
    app.mainloop()