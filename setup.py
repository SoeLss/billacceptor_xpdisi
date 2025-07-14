import os
import re
import subprocess
import logging
import threading
import time

polinema = ("""                              .:x;.                              
                         :;XX; .::..+$x:.                        
                     :xX; :+Xx:   .;XX+.:+X+                     
                  ;$;.:XX:             .;Xx.:XX                  
               ;$: +$:                     .+$:.$x               
            .$; ;$:      X  &;+;;:+ x.$&:.     +X.:&:            
          ;$::$;   ::X+;&X; +.x:XX:X$++:;Xx:X    :$;.$;          
        ;X.;X.  ..+.$++:.                 ;$ :$:+   x+.X;        
      :X.;X.  +;;+;;         :  x  :.        :Xx::x  .x+.X:      
    .&::$.  :;.XX:           : .:;  ;           :++ +   $::$.    
   ;X X;   x: X    + +;   .;X:+: ;: x+.   :X +.   X.     :$ X+   
  X;:&.   : .+   +:    :;     +: +:     :;     +.  .XXX    $;:$  
.$.;x   .++;;   x        .;;:;+: X;;:;;.        ;:   ++$;   ;X.$:
:x X    ;;:+     +.    ;:;;x$;:. X+;X+;+:+     x.     XX;    +.+;
:x X   ++:       ::  :;;. +.  +: X+:  + .+:;   x      .X:+   +:+;
:x X    ;X:     :.  ;.;  X+xx$;: X;XXx+$  ;.+   ;      +x    +:+;
:X X          ..X  ; X::::  :.;+ +:.;  .:.:;:;  .;.          +.x;
.& X       .+      +:.  +   &.+X ;.:$.  X   ++      ::       X $:
 $.x:      .+     .;x:;+&+;;x:+X ; +;;;;$+;;X::     .:       X.& 
 +::X      .;     .+;   $   ; ;X : x.:  X.  X::     .:      ;x.x 
 .X X      .x;..   ;:: :+XXx&+:X..:$$+xx$;..:;   ..:x:      X:x: 
  $:;;          +  .;+.  ; :++:.  :$+: :.  X::  +.         .x.$  
  .x &.          +  .;:+;;;::+;+;;;$::;:;+;;:  ::          $:+:  
   x;.x           +   ;:;;+xX;+x;+++;X+;;:+   :.          ;;:X   
    $ +;        .;      :+: &        : $:       ;        :$ $.   
    :$ X.      .X      ;:;$$+$X;;;x$x+$$;::     ;:       X X:    
     :+ $        .+;+++++++++++++++++++++++X+;:;        $.+;     
      ++.$:   ;+xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx+;.  .$.++      
       ++ X:            ;;;::;;;.:;+;:;;;            :$ x;       
        ;X +;       ;;. :++++++:X ;+++++: .:+       ;x X;        
         .$ :X     ::+.:+      :X;      ;: +;;     x; $.         
           X: Xx:. +;                       ;;..:x$ :X           
            ;X+:  :+XXx+;:             .:;+XX+;  :+X;            
               .:+X$X;.   .:::;;;;;;:::.  .;x$X+:.               
                       ..:;+xXXXXXXXX+;:..                       """)

ugm = ("""                                +.                               
                             .:$+$x:                             
                     :xXXx+;:. :$x  :;;++X$x:                    
                   Xx.   :;+XXx:  ;xXX+;:   :$+                  
             $$: .&. x&+:       ++       :$$. ;$.x$+X            
             X   &; +$         ;;::        +&  &;  .$            
            .+:  $: X:         x  X        .&..&:.;XX+;.         
        .X$+:.:+$$$ :$       :+X .$x       +x ;&$;     ;$+       
       Xx  +XXX:  x$ ;x    .+X $ .;++:    ;X +$. ;$&$&$; :X      
      $. xX.   .+$.:&:;$  :$+++X.::+:.$  x+ $+ xX.     ;$ :$     
     $: X;        ;+ $X $XX+;+&$&&XXxX+x&:;&:;$         .X :x    
    X; +:           $:XXX$$;::$.+x.X;;;$xxx;X:           .X .X.  
.:+X .X.         .;XX+XX:+;;+;+xXXx+;.+;;+$X+$;;:          xx::&+
 X+;&;  ...  ++X+++;XX:+:;X&;+;;+++;.x&+;:;;$;++;++xX+;;+x  $:;: 
  $ +;  +;   :+X::X$+ .;&+:&:+ .++::X++;&;:  $:.Xx:    ;X  .X +. 
  X ;;    .&;     ++  ;$ ++ X+:&&&$:&.;$xXx  .$.  :$&;     .X :: 
 +; x:      ;+:.:X&   &&;::XX;&;  xx+:+:x&&:  ;+::+$+       &..$ 
 &: &:       :X+;++  +X.;:+x;x +XX:.XXx;$x;$  :&XXX;        $: &:
:&:.&.         X$X+  ++;;++X+; X.:; Xx++$$;&  .&:+;        .&:.&:
 &; Xx          X+X  :&$X$$;+++    X;+x;+&&+  :$;&X;      x&: xx 
 .&. :&&x;X$&$:..&$:  x$.XX.X;$:..+$:x+:&x$   XX&$:  .....   $x  
   $$:     .:X&&XX$$   +&;$ $:;$$$X;:&; +X:  +X+x:. ;$&&Xx$&+X+  
   +x:xX&&X:  ;XX+$x&:Xx X&&:X$X++$+X:&$::X xXx;   +$;. .$X   .$:
 ++   :$: .xX:    X+;xX:X+;+x$XX&&&&X;+. ;;$;++;      :$; ;&XXx+:
  .:;X$  X$       ;+;++x&;+;:X;X+X.x&:+:XX:+:;Xx        $; X+    
     $+ +$        .+.X..&;X&&$;:..:+$&$;++:  X.x        X; X;    
     xx ;$        $&: .X.+++Xxx$XX+X$Xx+.+:;  :+       +X ;$     
      $; ;$       X. .x;xx+   x:Xx:+    .:;$+: :;    .X: ;X      
       xx  x+    ;:.x:.       X:x+ x          ++x   +; :$:       
         xx .X; .&+:          & +x X               X. X:         
           X+ X;             ;x xX ;x          +$&&+:$           
            +X:x;;X$;       +X  X$. +X     :&X.  ;XXx.           
            :&$$Xx:   ;$$$&$; .$::&: .x$$X;  :XX.                
                   ;X+:     ;$$:   $&+;::;+$x.                   
                       :;;;;:  X..X   :::.                       
                                XX                               """)

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def print_log(message, level="info"):
    """Mencetak pesan ke terminal dan mencatat log."""
    # Gunakan \r dan end='' untuk memastikan log tetap di baris baru setelah animasi
    print('\r' + ' ' * 80 + '\r', end='')
    if level == "info":
        print(f"✅ {message}")
        logging.info(message)
    elif level == "warning":
        print(f"⚠️ {message}")
        logging.warning(message)
    elif level == "error":
        print(f"❌ {message}")
        logging.error(message)

def animate_loading(stop_event, command_name):
    """Fungsi untuk menampilkan animasi spinner di thread terpisah."""
    spinner_chars = ['-', '\\', '|', '/']
    idx = 0
    while not stop_event.is_set():
        # Menggunakan \r (carriage return) untuk kembali ke awal baris
        print(f'\r{spinner_chars[idx % len(spinner_chars)]} Menjalankan: {command_name}...', end='')
        idx += 1
        time.sleep(0.1)
    # Membersihkan baris animasi setelah selesai
    print('\r' + ' ' * (len(command_name) + 20) + '\r', end='')

def run_command(command):
    """Menjalankan perintah shell dengan animasi loading dan menangani error."""
    stop_loading_event = threading.Event()
    
    # Mengambil bagian awal dari perintah untuk ditampilkan sebagai nama
    if len(command) > 40:
        command_display_name = command[:37] + "..."
    else:
        command_display_name = command

    loading_thread = threading.Thread(target=animate_loading, args=(stop_loading_event, command_display_name))
    
    try:
        loading_thread.start()
        # Jalankan perintah tanpa menampilkan outputnya (mode senyap)
        subprocess.run(command, check=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Hentikan animasi setelah selesai
        stop_loading_event.set()
        loading_thread.join()
        
        print_log(f"Berhasil menjalankan: {command_display_name}")

    except (subprocess.CalledProcessError, KeyboardInterrupt) as e:
        # Hentikan animasi jika terjadi error atau interupsi
        stop_loading_event.set()
        loading_thread.join()
        print_log(f"Gagal atau dibatalkan: {command_display_name}\nError: {e}", "error")
        # Keluar dari script jika ada perintah yang gagal
        exit(1)

def install_dependencies():
    """Menginstal semua dependensi yang dibutuhkan."""
    print_log("📦 Menginstal dependensi...")
    
    run_command("sudo apt update")
    upgrade_choice = input("❓ Apakah Anda ingin menjalankan full system upgrade? (Ini bisa memakan waktu lama) (y/n): ").strip().lower()
    if upgrade_choice == 'y':
        run_command("sudo apt-get upgrade -y") # Menggunakan apt-get untuk kompatibilitas lebih luas
    else:
        print_log("Proses upgrade dilewati.", "warning")

    dependencies = [
        "sudo apt-get install -y python3-pip git",
        "sudo pip3 install flask requests psutil flask_cors python-dotenv --break-system-packages",
        "sudo apt-get install -y ufw",
        "sudo systemctl start pigpiod",
        "sudo systemctl enable pigpiod"
    ]
    for dep in dependencies:
        run_command(dep)
    print_log("✅ Semua dependensi telah terinstal.")

def replace_line_in_file(filename, pattern, replacement):
    """Mengganti baris dalam file berdasarkan pola tertentu."""
    if not os.path.exists(filename):
        print_log(f"❌ File tidak ditemukan: {filename}", "error")
        return  
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
        
        with open(filename, "w") as file:
            for line in lines:
                if re.search(pattern, line):
                    file.write(replacement + "\n")
                else:
                    file.write(line)
        print_log(f"✅ Berhasil mengedit file: {filename}")
    except FileNotFoundError:
        print_log(f"❌ File tidak ditemukan: {filename}", "error")

def write_env_file(filename, device_id, token_api, invoice_api, bill_api, log_dir, flask_port, hopper_pin, sensor_pin, coin_value):
    with open(filename, "w") as env_file:
        env_file.write("# Konfigurasi Utama\n")
        env_file.write(f'ID_DEVICE="{device_id}"\n')
        env_file.write(f'TOKEN_API="{token_api}"\n')
        env_file.write(f'INVOICE_API="{invoice_api}"\n')
        env_file.write(f'BILL_API="{bill_api}"\n')
        env_file.write(f'LOG_DIR="{log_dir}"\n')
        env_file.write(f'PORT={flask_port}\n\n')
        
        env_file.write("# Konfigurasi Coin Hopper & Sensor\n")
        env_file.write(f'HOPPER_PIN={hopper_pin}\n')
        env_file.write(f'SENSOR_PIN={sensor_pin}\n')
        env_file.write(f'COIN_VALUE={coin_value}\n')

def configure_files(python_path):
    """Mengedit file konfigurasi dengan parameter yang diberikan."""
    print_log("🛠️ Mengonfigurasi file...")
    replace_line_in_file("billacceptor.service", r'ExecStart=.*', f'ExecStart=/usr/bin/python3 {python_path}/billacceptor.py')

def move_files(python_path, rollback_path):
    """Memindahkan file ke lokasi yang sesuai."""
    print_log("📂 Memindahkan file konfigurasi...")
    run_command("sudo mv billacceptor.service /etc/systemd/system/")
    run_command(f"sudo mv billacceptor.py {python_path}")
    run_command(f"sudo mv rollback.py {rollback_path}")
    run_command(f"sudo mv setup.log {rollback_path}")

def configure_ufw(flask_port):
    """Mengonfigurasi firewall UFW."""
    print_log("🔐 Mengonfigurasi UFW...")
    run_command(f"sudo ufw allow {flask_port}")
    run_command("sudo ufw --force enable")

def enable_service():
    """Mengaktifkan service billacceptor."""
    print_log("🚀 Mengaktifkan service Bill Acceptor...")
    run_command("sudo systemctl daemon-reload")
    run_command("sudo systemctl enable billacceptor.service")
    run_command("sudo systemctl start billacceptor.service")

def write_setup_log(filename, data):
    """Menuliskan data setup ke dalam file log."""
    try:
        with open(filename, "a") as log_file:
            log_file.write(data)
    except PermissionError:
        print_log(f"❌ Tidak bisa menulis ke {filename}. Coba jalankan dengan sudo.", "error")
    except Exception as e:
        print_log(f"Gagal menulis log setup: {e}", "error")

def ensure_directory_exists(directory):
    """Membuat folder jika belum ada."""
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        print_log(f"📁 Membuat folder: {directory}")
    else:
        print_log(f"✅ Folder sudah ada: {directory}")

def lmxugmxpolinema(ascii1, ascii2, watermark="--**UGM x POLINEMA**--"):
    lines1 = ascii1.strip('\n').split('\n')
    lines2 = ascii2.strip('\n').split('\n')

    max_lines = max(len(lines1), len(lines2))
    lines1 += [""] * (max_lines - len(lines1))
    lines2 += [""] * (max_lines - len(lines2))

    # Perbaiki jika salah satu ASCII art kosong
    if not any(lines1): max_width1 = 0
    else: max_width1 = max(len(line) for line in lines1)

    output_lines = []

    for line1, line2 in zip(lines1, lines2):
        combined = line1.ljust(max_width1 + 4) + line2
        output_lines.append(combined)

    # Perbaiki jika output_lines kosong
    if not output_lines: total_width = 0
    else: total_width = len(output_lines[0])

    centered_watermark = watermark.center(total_width)
    output_lines.append("")
    output_lines.append(centered_watermark)

    print("\n".join(output_lines))

if __name__ == "__main__":
    setup_log_file = "setup.log"
    # Hapus log setup lama jika ada, untuk memulai sesi baru
    if os.path.exists(setup_log_file):
        os.remove(setup_log_file)
    
    lmxugmxpolinema(ugm, polinema)
    print("\n🔧 **Setup Bill Acceptor**\n")

    # Input dari pengguna
    device_id = input("Masukkan ID Device: ")
    write_setup_log(setup_log_file, f"ID_DEVICE: {device_id}\n")

    token_api = input("Masukkan URL TOKEN_API: ")
    write_setup_log(setup_log_file, f"TOKEN_API: {token_api}\n")

    invoice_api = input("Masukkan URL INVOICE_API: ")
    write_setup_log(setup_log_file, f"INVOICE_API: {invoice_api}\n")

    bill_api = input("Masukkan URL BILL_API: ")
    write_setup_log(setup_log_file, f"BILL_API: {bill_api}\n")

    python_path = input("Masukkan path penyimpanan billacceptor.py (Contoh: /home/eksan/billacceptor): ")
    ensure_directory_exists(python_path)
    write_setup_log(setup_log_file, f"Python Path: {python_path}\n")

    log_dir = python_path
    print_log(f"📁 LOG_DIR disetel ke: {log_dir}")
    write_setup_log(setup_log_file, f"LOG_DIR: {log_dir}\n")

    flask_port = input("Masukkan port Flask (Contoh: 5000): ")
    write_setup_log(setup_log_file, f"Flask Port: {flask_port}\n")

    hopper_pin = input("Masukkan pin GPIO untuk Coin Hopper (Contoh: 18): ")
    write_setup_log(setup_log_file, f"HOPPER_PIN: {hopper_pin}\n")

    sensor_pin = input("Masukkan pin GPIO untuk Sensor Hopper (Contoh: 23): ")
    write_setup_log(setup_log_file, f"SENSOR_PIN: {sensor_pin}\n")
    
    coin_value = input("Masukkan nominal koin di hopper (Contoh: 1000): ")
    write_setup_log(setup_log_file, f"COIN_VALUE: {coin_value}\n")

    rollback_path = input("Masukkan path penyimpanan rollback.py (Contoh: /home/eksan/rollback): ")
    ensure_directory_exists(rollback_path)
    write_setup_log(setup_log_file, f"Rollback Path: {rollback_path}\n")

    # Tulis file .env
    env_path = os.path.join(python_path, ".env")
    write_env_file(
        env_path, device_id, token_api, invoice_api, bill_api, 
        log_dir, flask_port, hopper_pin, sensor_pin, coin_value
    )
    print_log(f"✅ File .env berhasil dibuat di: {env_path}")

    # Jalankan semua fungsi
    install_dependencies()
    configure_files(python_path)
    move_files(python_path, rollback_path)
    configure_ufw(flask_port)
    enable_service()

    print("\n🎉 **Setup selesai! Bill Acceptor sudah terinstal dan berjalan.** 🎉")
    print_log("🎉 Setup selesai! Bill Acceptor sudah terinstal dan berjalan.")