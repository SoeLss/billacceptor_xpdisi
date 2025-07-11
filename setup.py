import os
import re
import subprocess
import logging

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
    if level == "info":
        print(f"✅ {message}")
        logging.info(message)
    elif level == "warning":
        print(f"⚠️ {message}")
        logging.warning(message)
    elif level == "error":
        print(f"❌ {message}")
        logging.error(message)

def run_command(command):
    """Menjalankan perintah shell dengan subprocess dan menangani error."""
    try:
        subprocess.run(command, check=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_log(f"Berhasil menjalankan: {command}")
    except subprocess.CalledProcessError as e:
        print_log(f"Gagal menjalankan: {command}\nError: {e}", "error")

def install_dependencies():
    """Menginstal semua dependensi yang dibutuhkan."""
    print_log("📦 Menginstal dependensi...")
    dependencies = [
        "sudo apt update && sudo apt upgrade -y",
        "sudo apt install -y python3-pip git",
        "sudo pip3 install flask requests psutil flask_cors python-dotenv --break-system-packages",
        "sudo apt install -y ufw",
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
            log_file.write(data + "\n")
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

    max_width1 = max(len(line) for line in lines1)
    output_lines = []

    for line1, line2 in zip(lines1, lines2):
        combined = line1.ljust(max_width1 + 4) + line2
        output_lines.append(combined)

    total_width = len(output_lines[0])
    centered_watermark = watermark.center(total_width)
    output_lines.append("")
    output_lines.append(centered_watermark)

    print("\n".join(output_lines))

if __name__ == "__main__":
    setup_log_file = "setup.log"
    
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

    python_path = input("Masukkan path penyimpanan billacceptor.py (Contoh: /home/pi/billacceptor): ")
    ensure_directory_exists(python_path)
    write_setup_log(setup_log_file, f"Python Path: {python_path}\n")

    log_dir = python_path
    print_log(f"📁 LOG_DIR disetel ke: {log_dir}")
    write_setup_log(setup_log_file, f"LOG_DIR: {log_dir}\n")

    flask_port = input("Masukkan port Flask (Contoh: 5000): ")
    write_setup_log(setup_log_file, f"Flask Port: {flask_port}\n")

    hopper_pin = input("Masukkan pin GPIO untuk Coin Hopper (Contoh: 23): ")
    write_setup_log(setup_log_file, f"HOPPER_PIN: {hopper_pin}\n")

    sensor_pin = input("Masukkan pin GPIO untuk Sensor Hopper (Contoh: 24): ")
    write_setup_log(setup_log_file, f"SENSOR_PIN: {sensor_pin}\n")
    
    coin_value = input("Masukkan nominal koin di hopper (Contoh: 1000): ")
    write_setup_log(setup_log_file, f"COIN_VALUE: {coin_value}\n")

    rollback_path = input("Masukkan path penyimpanan rollback.py (Contoh: /home/pi/billacceptor): ")
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