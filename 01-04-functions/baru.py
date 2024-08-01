
# Teks yang akan dihitung jumlah hurufnya
teks = "saya ingin belajar coding"

# Menghapus spasi dari teks dan menghitung jumlah setiap huruf
jumlah_huruf = {}
for huruf in teks.replace(" ", ""):
    jumlah_huruf[huruf] = jumlah_huruf.get(huruf, 0) + 1

# Membuat string hasil yang sesuai format
hasil = ", ".join([f"{huruf}:{jumlah}" for huruf, jumlah in jumlah_huruf.items()])

# Menampilkan hasil
print(hasil)