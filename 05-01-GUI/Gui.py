import os
import tkinter as tk
import json
from tkinter import messagebox

filename = 'data.json'

if os.path.exists(filename):
    with open(filename, 'r') as f:  
        data = json.load(f)
else:
    data = {
        'name': '',
        'level': ''
    }

# Membuat jendela utama
window = tk.Tk()
window.title("Input Data")

# Label dan Entry untuk nama
tk.Label(window, text='Masukkan nama Anda:').pack()
name_entry = tk.Entry(window)
name_entry.insert(tk.INSERT, data['name'])
name_entry.pack()

# Label dan Entry untuk level
tk.Label(window, text='Masukkan level berapa:').pack()
level_entry = tk.Entry(window)
level_entry.insert(tk.INSERT, data['level'])
level_entry.pack()

# Fungsi untuk menyimpan data
def save_command():
    name = name_entry.get()
    level = level_entry.get()
    data = {
        'name': name,
        'level': level
    }
    with open(filename, 'w') as f:
        json.dump(data, f)
    messagebox.showinfo('info', f'Hello {name}! Level Anda: {level}')

# Tombol untuk menyimpan
tk.Button(window, text='Simpan', command=save_command).pack()

# Menjalankan jendela
window.mainloop()
