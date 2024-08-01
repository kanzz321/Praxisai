prime = [2, 3, 9, 5, 7,]

# Menentukan nilai maksimum
max_value = max(prime)

# Menentukan nilai minimum
min_value = min(prime)

print(f"Nilai maksimum dari list prime adalah: {max_value}")
print(f"Nilai minimun dari list prime adalah: {min_value}")

# print(f"..."): Fungsi print dengan f-string digunakan untuk menampilkan hasilnya ke layar dengan format yang mudah dibaca.

teks = "saya ingin belajar coding"

jumlah_huruf = {}
for huruf in teks.replace(" ", ""):
    jumlah_huruf[huruf] = jumlah_huruf.get(huruf, 0) + 1

hasil = ", ".join([f"{huruf}:{jumlah}" for huruf, jumlah in jumlah_huruf.items()])

print(hasil)


data = {0: "Ilmi", 1: "Nabil"}

data[2] = "ardan"

print(data)
