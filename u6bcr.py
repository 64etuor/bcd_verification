import tkinter as tk
from tkinter import ttk, messagebox
import time
import datetime
import pyperclip
import os

div_map = {"Hard-pack(Chinese)":"KRRPMI4301010ADB67","Hard-pack(India)":"KRRPMI4301014ADB67"} # 제품구분별 고정 BCD MAPPING

year_map = {2023: "W", 2024: "X", 2025: "Y", 2026: "L", 2027: "P", 2028: "Q", 2029: "S", 2030: "Z"} # 연도 일련번호 MAPPING

month_map = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "A", 11: "B", 12: "C"}

day_map = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "A", 11: "B", 12: "C",
           13: "D", 14: "E", 15: "F", 16: "G", 17: "H", 18: "I", 19: "J", 20: "K", 21: "L", 22: "M", 23: "N",
           24: "O", 25: "P", 26: "Q", 27: "R", 28: "S", 29: "T", 30: "U", 31: "V"} # 날짜 일련번호 MAPPING

def generate_barcode():
    div = div_map[div_Combobox.get()]
    now = time.localtime()
    year = year_map[now.tm_year]
    month = month_map[now.tm_mon]
    day = day_map[now.tm_mday]
    return f"{div}{year}{month}{day}0000" # 바코드 형식 (A라인 생산 고정)

def verify_barcode(event=None):
    barcode = barcode_entry.get()
    barcode = barcode.upper() # 바코드 Entry 강제 대문자 인식
    generated_barcode = generate_barcode()
    if barcode[:21] == generated_barcode[:21] and len(barcode) == 25 and barcode[-4:].isdigit(): # BCD 검증 제품구분, 연, 월, 일, 생산라인, 일련번호 총 12자리(마지막 4자리 숫자 검증)
        result_status = "PASS"
        messagebox.showinfo("Verification", "PASS")
    else:
        result_status = "NG"
        messagebox.showerror("Verification", "NG (Barcode is invalid)")
    log_barcode(barcode, generated_barcode, result_status)

def log_barcode(barcode, generated_barcode, result_status):
    div = div_Combobox.get()
    if result_status == "PASS":
        log_folder_path = "C:/Logs/U6"
        if not os.path.exists(log_folder_path):
            os.makedirs(log_folder_path) # Log 폴더 강제 생성
        log_file_path = f"{log_folder_path}/{time.strftime('%Y-%m-%d')}_{barcode_entry.get()}.csv" # Log 파일명, 파일형식(csv)
        with open(log_file_path, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}, {div}, {barcode}, {generated_barcode}, {result_status}\n") # Log 저장 정보(제품구분, 바코드, 기준바코드, 결과값)

def open_log_files_folder():
    log_folder_path = "C:/Logs/U6" # Open folder Button Linked Address
    os.startfile(log_folder_path)

root = tk.Tk() # ↓↓ GUI Setting ↓↓
root.title("U6 BCD Verification_ver.00")
root.geometry("450x190")

div_label = tk.Label(root, text="Div.Class", bg='#2F5597', fg='white',
                         width=8, height=1,
                         font=('맑은고딕',12,'bold'))
div_label.grid(row=0, column=0, padx=5, pady=10)

div_var = tk.StringVar(value=list(div_map.keys())[0])
div_Combobox = ttk.Combobox(root, font=('맑은고딕',11), textvariable=div_var, values=list(div_map.keys()), justify='center')
div_Combobox.grid(row=0, column=1, padx=5, pady=10)

barcode_label = tk.Label(root, text="BCD Scan", bg='#2F5597', fg='white', width=8, height=1, font=('맑은고딕',12, 'bold'))
barcode_label.grid(row=1, column=0, padx=5, pady=5)

barcode_entry = tk.Entry(root, bg='white', width=30, font=('맑은고딕', 11, 'bold'), justify='center')
barcode_entry.grid(row=1, column=1, padx=5, pady=5)

verify_button = ttk.Button(root, text="Verify BCD", command=verify_barcode)
verify_button.grid(row=2, column=0, padx=38, pady=10, sticky="W")

barcode_entry.bind("<Return>", verify_barcode) # Return Key 입력에 Verify 버튼 Binding

openfolder_button = ttk.Button(root, text="Open Logs", command=open_log_files_folder)
openfolder_button.grid(row=2, column=1, padx=0, pady=0, sticky="E")

def show_barcode():
    barcode2 = generate_barcode()
    barcode2_label.configure(text=barcode2)
    pyperclip.copy(barcode2) # Copy to Clipboard
    messagebox.showinfo("Success", "Copied to Clipboard") 

generate_button = ttk.Button(root, text="Generate BCD", command=show_barcode)
generate_button.grid(row=3, column=0, padx=5, pady=5)

barcode2_label = tk.Label(root, text="", font=('맑은고딕', 11, 'bold'))
barcode2_label.grid(row=3, column=1, padx=5, pady=5)

def update_label():
    current_time = datetime.datetime.now().strftime("Sys. Date : "+"%Y-%m-%d") # 시스템 날짜 표시
    date_label.config(text=current_time)
    date_label.after(1000, update_label)

date_label = tk.Label(root, font=('맑은고딕', 9, 'bold'))
date_label.grid(row=4, column=0, padx=16, pady=5, sticky="W")

update_label()

dept_label = tk.Label(root, text="_Elentec Corp.", font=('맑은고딕',8))
dept_label.grid(row=4, column=1, padx=0, pady=5, sticky="E")

root.mainloop()
