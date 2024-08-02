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
       # int(input()): Untuk mengonversi input dari string menjadi bilangan bulat sehingga operasi matematika bisa dilakukan.
        operator = input('Pilih operator "penambahan", "pengurangan", "perkalian", atau "pembagian": ').lower()
        number1 = int(input("Masukkan angka pertama: "))
        number2 = int(input("Masukkan angka kedua: "))
 
    # if-elif-else: Untuk menentukan operasi matematika yang akan dilakukan berdasarkan input operator.
       
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

    #try-except: Untuk menangani kesalahan input yang mungkin terjadi ketika mengonversi input menjadi bilangan bulat.

    # Menampilkan hasil
   
    #isinstance(res, str): Untuk memeriksa apakah res adalah instance dari tipe str, 
    # sehingga jika terjadi kesalahan (seperti pembagian dengan nol atau input yang tidak valid), pesan kesalahan bisa dicetak dengan benar.

    if isinstance(res, str):
        print(res)
    
    #res.is_integer(): Untuk memeriksa apakah hasil operasi matematika adalah bilangan bulat, 
    # sehingga bisa ditampilkan tanpa desimal jika hasilnya bilangan bulat.
    else:
 
        if res.is_integer():
            res = int(res)
        print(f'{operator} dari {number1} dan {number2} adalah {res}')

    while True:
        ulang = input("Apakah kamu mau berhitung lagi? (ya/tidak): ")

        if ulang == "tidak":
            quit("Terimakasih telah menggunakan aplikasi ini")
        elif ulang == "ya":
            break

    #break: Untuk kembali ke loop utama dan memulai perhitungan baru jika pengguna memilih "ya".
    # quit(): Untuk keluar dari program jika pengguna memilih "tidak", dengan pesan terima kasih.
        else:
            print("Input tidak valid, silahkan coba lagi.")
            continue

    #terimakasih
