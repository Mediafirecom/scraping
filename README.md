# 🌐 Web Scraper HTML/CSS/JS

**Web Scraper HTML/CSS/JS** adalah sebuah tool sederhana yang dibuat untuk melakukan scraping terhadap halaman web menggunakan kombinasi HTML parser dan JavaScript DOM traversal. Tool ini mampu mengekstrak data seperti teks, elemen HTML, dan atribut tertentu dari halaman web.

---

## 📌 Fitur

- Scraping data teks dari elemen HTML (seperti `<div>`, `<p>`, `<span>`, dll)
- Mendapatkan atribut elemen (contoh: `href`, `src`, `alt`)
- Dukungan untuk parsing HTML dan manipulasi menggunakan JS
- Output hasil scraping dalam bentuk `.json` atau `.txt`
- Cross-platform (Linux, Windows, Termux)

---

## 🛠 Teknologi yang Digunakan

- Python (untuk backend scraping)
- BeautifulSoup (HTML parser)
- requests (pengambil halaman web)
- js2py (eksekusi fungsi JavaScript dari Python)
- bash (untuk script instalasi di Termux)
- Node.js (opsional untuk scraping berbasis JS asli via Puppeteer)

---

## 🚀 Cara Instalasi

### 1. Instalasi di Termux / Linux

```bash
pkg update && pkg upgrade
pkg install python git -y
pip install requests beautifulsoup4 rich
git clone https://github.com/mediafirecom/scraping
cd scraping
python py.py
