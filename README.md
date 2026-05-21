# 🔐 Kalkulator Kriptografi Klasik (Web-Based)

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Framework-lightgrey.svg?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](https://opensource.org/licenses/MIT)

Sebuah aplikasi berbasis web (*Web-Based Application*) yang dirancang khusus sebagai kalkulator interaktif untuk mensimulasikan, mempelajari, dan menghitung berbagai metode **Kriptografi Klasik**. 

Proyek ini dibangun menggunakan **Python Flask** sebagai backend untuk menangani logika matematis cipher, serta antarmuka web yang responsif untuk mempermudah pengguna dalam memahami bagaimana teks disamarkan (*encryption*) dan dikembalikan ke bentuk semula (*decryption*). Aplikasi ini sangat cocok digunakan sebagai media pembelajaran interaktif bagi mahasiswa teknik informatika, praktisi keamanan siber, atau siapa saja yang tertarik dengan sejarah kriptografi.

---

## 🚀 Fitur Utama & Algoritma Supported

Kalkulator ini mengintegrasikan 5 algoritma kriptografi klasik yang paling populer dan fundamental, di antaranya:

### 1. 🔑 Caesar Cipher
Algoritma substitusi paling klasik yang bekerja dengan menggeser setiap karakter pada *plaintext* berdasarkan nilai kunci (*shift*) tertentu (0–25). 
* **Kelebihan di App:** Mendukung pergeseran dinamis serta mempertahankan format spasi/karakter non-alfabet jika diperlukan.

### 2. 🗺️ Vigenere Cipher
Pengembangan dari Caesar Cipher yang menggunakan metode substitusi polialfabetik. Algoritma ini menggunakan sebuah kata kunci (*keyword*) yang diulang sepanjang teks asli untuk menentukan nilai pergeseran tiap karakter.
* **Kelebihan di App:** Validasi kata kunci otomatis agar proses enkripsi tetap presisi tanpa memedulikan perbedaan *case* huruf.

### 3. 📐 Affine Cipher
Cipher substitusi monoalfabetik yang memanfaatkan fungsi matematis linear $E(x) = (ax + b) \pmod{26}$.
* **Kelebihan di App:** Dilengkapi dengan validasi otomatis untuk memastikan nilai $a$ yang dimasukkan saling prima (*coprime*) dengan 26 ($	ext{gcd}(a, 26) = 1$), sehingga proses dekripsi selalu valid dan memiliki invers matriks modular.

### 4. 📊 Hill Cipher
Algoritma kriptografi polialfabetik yang memanfaatkan teori aljabar linear, khususnya perkalian matriks. Teks dikelompokkan ke dalam blok-blok berukuran tertentu kemudian dikalikan dengan matriks kunci.
* **Kelebihan di App:** Mendukung konfigurasi matriks kunci (seperti $2 	imes 2$ atau $3 	imes 3$) secara dinamis langsung dari antarmuka web dengan perhitungan determinan otomatis untuk proses dekripsi.

### 5. 👥 Playfair Cipher
Metode enkripsi simetris berbasis teknik substitusi digram (pasangan huruf) yang menggunakan matriks kunci berukuran $5 	imes 5$ yang berisi kombinasi alfabet (biasanya menggabungkan huruf I dan J).
* **Kelebihan di App:** Logika otomatis untuk menangani pemisahan huruf kembar (*filler character* seperti 'X') dan pembentukan pasangan digram secara *real-time*.

---

## 🛠️ Tech Stack & Arsitektur

Proyek ini dirancang secara modular untuk memastikan kode mudah dipahami, dirawat, dan dikembangkan di masa mendatang:

* **Backend Core:** `Python 3` – Menangani seluruh komputasi matematis, manipulasi string, dan operasi matriks.
* **Web Framework:** `Flask` – Sebagai *micro-framework* yang ringan untuk menjembatani logika backend dengan antarmuka pengguna secara efisien melalui perutean (*routing*) yang rapi.
* **Frontend Interface:** `HTML5 & CSS3` – Desain antarmuka yang bersih, intuitif, dan *user-friendly*, memisahkan input parameter kunci untuk setiap jenis cipher agar tidak membingungkan pengguna.
* **Deployment Ready:** Dilengkapi konfigurasi `passenger_wsgi.py` yang siap digunakan untuk kebutuhan *hosting* pada *cPanel* atau layanan cloud modern.

---

## 💡 Tujuan Proyek

Proyek ini dibuat bukan hanya sekadar untuk menghasilkan teks tersandi, melainkan sebagai **perangkat edukasi** (*Educational Tool*). Melalui aplikasi ini, pengguna dapat:
1. Memahami perbedaan mendasar antara cipher substitusi monoalfabetik dan polialfabetik.
2. Mempelajari implementasi nyata matematika diskrit (operasi modulo, fpb/gcd, dan matriks inverse) di dalam baris kode pemrograman.
3. Melakukan validasi hasil perhitungan manual (misalnya untuk tugas kuliah atau praktikum) dengan cepat dan akurat.

---
*Dibuat dengan 💻 dan ☕ untuk pengembangan ilmu keamanan informasi.*
