import tkinter as tk
from tkinter import messagebox
import time
import os

year_map = {2023: "C", 2024: "D", 2025: "E", 2026: "F", 2027: "G", 2028: "H", 2029: "I", 2030: "J", 2031: "K",
            2032: "L", 2033: "M", 2034: "N", 2035: "O"}

month_map = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "A", 11: "B", 12: "C"}

day_map = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "A", 11: "B", 12: "C",
           13: "D", 14: "E", 15: "F", 16: "G", 17: "H", 18: "I", 19: "J", 20: "K", 21: "L", 22: "M", 23: "N",
           24: "O", 25: "P", 26: "Q", 27: "R", 28: "S", 29: "T", 30: "U", 31: "V"}

def generate_barcode():
    now = time.localtime()
    year = year_map[now.tm_year]
    month = month_map[now.tm_mon]
    day = day_map[now.tm_mday]
    return f"ABCDEFGH{year}{month}{day}0000"

def verify_barcode(event=None):
    barcode = barcode_entry.get()
    barcode = barcode.upper()
    generated_barcode = generate_barcode()
    if barcode[:11] == generated_barcode[:11] and len(barcode) == 15 and barcode[-4:].isdigit():
        result_status = "Valid"
        messagebox.showinfo("Verification", "PASS")
    else:
        result_status = "Invalid"
        messagebox.showerror("Verification", "NG (Barcode is invalid)")
    log_barcode(barcode, generated_barcode, result_status)

def log_barcode(barcode, generated_barcode, result_status):
    if result_status == "Valid":
        log_folder_path = "D:/Logs/U6/"
        if not os.path.exists(log_folder_path):
            os.makedirs(log_folder_path)
        log_file_path = f"{log_folder_path}/{time.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        with open(log_file_path, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}, {barcode}, {generated_barcode}, {result_status}\n")

def open_log_files_folder():
    log_folder_path = "D:/Logs/U6/"
    os.startfile(log_folder_path)

root = tk.Tk()
root.title("U6 H/P Barcode Verification")
root.geometry("340x100")

barcode_label = tk.Label(root, text="BCR Scan",
                         bg='#2F5597', fg='white',
                         width=8, height=1,
                         font=('맑은고딕',12,'bold'))
barcode_label.grid(row=0, column=0, padx=20, pady=10)

barcode_entry = tk.Entry(root, bg='white', width=20, font=('맑은고딕', 12, 'bold'))
barcode_entry.grid(row=0, column=1, padx=10, pady=10)

verify_button = tk.Button(root, text="Verify BCR", command=verify_barcode)
verify_button.grid(row=1, column=0, padx=20, pady=10, sticky="W")

openfolder_button = tk.Button(root, text="Open Logs", command=open_log_files_folder)
openfolder_button.grid(row=1, column=1, padx=10, pady=10, sticky="E")

barcode_entry.bind("<Return>", verify_barcode)

root.mainloop()