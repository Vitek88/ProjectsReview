import csv
import struct
from pymodbus.client import ModbusTcpClient
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import pandas as pd

def sanitize_value(value):
    if isinstance(value, str):
        return ''.join(c for c in value if c.isprintable())
    return value

def scan_modbus_registers(ip, start_register=0, end_register=100, progress_callback=None):
    client = ModbusTcpClient(ip)
    results = []
    errors = []

    try:
        connection = client.connect()
        if connection:
            total_registers = end_register - start_register + 1
            for i, register in enumerate(range(start_register, end_register + 1)):
                try:
                    result = client.read_holding_registers(register, count=2)
                    if not result.isError():
                        try:
                            # Zakładamy, że wartość jest typu float (32-bitowy)
                            value_float = struct.unpack('>f', struct.pack('>HH', result.registers[0], result.registers[1]))[0]
                        except:
                            value_float = None

                        try:
                            # Zakładamy, że wartość jest typu int (16-bitowy)
                            value_int16 = result.registers[0]
                        except:
                            value_int16 = None

                        try:
                            # Zakładamy, że wartość jest typu int (32-bitowy)
                            value_int32 = struct.unpack('>i', struct.pack('>HH', result.registers[0], result.registers[1]))[0]
                        except:
                            value_int32 = None

                        try:
                            # Zakładamy, że wartość jest typu unsigned int (32-bitowy)
                            value_uint32 = struct.unpack('>I', struct.pack('>HH', result.registers[0], result.registers[1]))[0]
                        except:
                            value_uint32 = None

                        try:
                            # Zakładamy, że wartość jest typu word (16-bitowy unsigned int)
                            value_word1 = result.registers[0]
                            value_word2 = result.registers[1]
                        except:
                            value_word1 = None
                            value_word2 = None

                        try:
                            # Zakładamy, że wartość jest typu bool (16-bitowy unsigned int)
                            value_bool = bool(result.registers[0])
                        except:
                            value_bool = None

                        try:
                            # Zakładamy, że wartość jest typu string (32-bitowy)
                            value_string = struct.pack('>HH', result.registers[0], result.registers[1]).decode('utf-8')
                        except:
                            value_string = None

                        try:
                            # Zakładamy, że wartość jest typu char (8-bitowy)
                            value_char1 = chr(result.registers[0] & 0xFF)
                            value_char2 = chr((result.registers[0] >> 8) & 0xFF)
                        except:
                            value_char1 = None
                            value_char2 = None

                        try:
                            # Zakładamy, że wartość jest typu long (64-bitowy)
                            if len(result.registers) >= 4:
                                value_long = struct.unpack('>q', struct.pack('>HHHH', result.registers[0], result.registers[1], result.registers[2], result.registers[3]))[0]
                            else:
                                value_long = None
                        except:
                            value_long = None

                        results.append({
                            'register': register,
                            'value_float': sanitize_value(value_float),
                            'value_int16': sanitize_value(value_int16),
                            'value_int32': sanitize_value(value_int32),
                            'value_uint32': sanitize_value(value_uint32),
                            'value_word1': sanitize_value(value_word1),
                            'value_word2': sanitize_value(value_word2),
                            'value_bool': sanitize_value(value_bool),
                            'value_string': sanitize_value(value_string),
                            'value_char1': sanitize_value(value_char1),
                            'value_char2': sanitize_value(value_char2),
                            'value_long': sanitize_value(value_long)
                        })
                    else:
                        errors.append({'register': register, 'error': 'Read error'})
                except Exception as e:
                    errors.append({'register': register, 'error': str(e)})
                
                if progress_callback:
                    progress_callback((i + 1) / total_registers * 100)

            client.close()
        else:
            errors.append({'error': f'Cannot connect to {ip}'})
    except Exception as e:
        errors.append({'error': str(e)})

    return results, errors

def export_to_excel(results, errors, directory):
    results_file = f"{directory}/modbus_scan_results.xlsx"
    errors_file = f"{directory}/modbus_scan_errors.xlsx"

    # Export results to Excel
    df_results = pd.DataFrame(results)
    df_results.to_excel(results_file, index=False)

    # Export errors to Excel
    df_errors = pd.DataFrame(errors)
    df_errors.to_excel(errors_file, index=False)

def start_scan():
    ip_address = ip_entry.get()
    start_register = int(start_entry.get())
    end_register = int(end_entry.get())

    directory = filedialog.askdirectory(title="Wybierz lokalizację dla plików Excel")
    if not directory:
        messagebox.showwarning("Brak lokalizacji", "Nie wybrano lokalizacji dla plików Excel.")
        return

    progress_bar["value"] = 0
    root.update_idletasks()

    def update_progress(value):
        progress_bar["value"] = value
        root.update_idletasks()

    results, errors = scan_modbus_registers(ip_address, start_register, end_register, progress_callback=update_progress)
    export_to_excel(results, errors, directory)

    messagebox.showinfo("Skanowanie zakończone", "Wyniki zapisane do plików modbus_scan_results.xlsx i modbus_scan_errors.xlsx.")

# Tworzenie interfejsu użytkownika
root = tk.Tk()
root.title("Modbus TCP Scanner")

tk.Label(root, text="Adres IP:").grid(row=0)
tk.Label(root, text="Zakres rejestrów od:").grid(row=1)
tk.Label(root, text="Zakres rejestrów do:").grid(row=2)

ip_entry = tk.Entry(root)
start_entry = tk.Entry(root)
end_entry = tk.Entry(root)

ip_entry.grid(row=0, column=1)
start_entry.grid(row=1, column=1)
end_entry.grid(row=2, column=1)

tk.Button(root, text="Rozpocznij skanowanie", command=start_scan).grid(row=3, columnspan=2)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=4, columnspan=2)

root.mainloop()
