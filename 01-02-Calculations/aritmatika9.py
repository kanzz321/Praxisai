import os
import getpass

os.system('cls')
os.system('color b')

Correct_username = "ilmi"
Correct_password = "level 10"

# Memasukkan nama pengguna
while True:
    username = input("Masukkan nama pengguna: ")
    
    if username == Correct_username:
        print("Username yang dimasukkan benar!")
        break
    else:
        print("Username salah. Silahkan coba lagi")

while True:
    password = getpass.getpass("Masukkan password: ")

    if password == Correct_password:
        print("Password yang dimasukkan benar!")
        break
    else:
        print("Kata sandi salah. Silahkan coba lagi")

while True:
    try:
        operator = input('Pilih operator "penambahan", "pengurangan", "perkalian", atau "pembagian": ').lower()
        number1 = int(input("Masukkan angka pertama: "))
        number2 = int(input("Masukkan angka kedua: "))

        if operator == 'penambahan':
            res = number1 + number2
        elif operator == 'pengurangan':
            res = number1 - number2
        elif operator == 'perkalian':
            res = number1 * number2
        elif operator == 'pembagian':
            if number2 != 0:
                res = number1 / number2
            else:
                res = "Pembagian dengan nol tidak valid." 
        else:
            res = "Operasi yang dimasukkan tidak valid." 
    except ValueError:
        res = "Input angka yang dimasukkan tidak valid." 

    # Menampilkan hasil
    if isinstance(res, str):
        print(res)
    else:
        if res.is_integer():
            res = int(res)
        print(f'{operator} dari {number1} dan {number2} adalah {res}')

    while True:
        ulang = input("Apakah kamu mau berhitung lagi? (ya/tidak): ")

        if ulang == "tidak":
            quit()
        elif ulang == "ya":
            break
        else:
            print("Input tidak valid, silahkan coba lagi.")
            continue

