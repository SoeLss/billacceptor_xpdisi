import os
import subprocess
import logging

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

def read_setup_log(log_path):
    """Membaca setup.log untuk mendapatkan informasi konfigurasi."""
    config = {}
    if not os.path.exists(log_path):
        print_log("setup.log tidak ditemukan, beberapa langkah mungkin gagal.", "error")
        return config
    
    with open(log_path, "r") as file:
        for line in file:
            if ":" in line:
                key, value = line.strip().split(":", 1)
                config[key.strip()] = value.strip()
    return config

def uninstall_dependencies():
    """Menghapus semua dependensi yang telah diinstal."""
    print_log("📦 Menghapus dependensi yang telah diinstal...")
    dependencies = [
        "sudo apt autoremove -y",
        "sudo pip3 uninstall -y flask requests psutil flask_cors python-dotenv", ## DIUBAH ##
        "sudo apt remove --purge -y python3-pip pptp-linux ufw",
    ]
    for dep in dependencies:
        run_command(dep)
    print_log("✅ Semua dependensi telah dihapus.")

def remove_files(python_path, log_dir, vpn_log):
    """Menghapus file konfigurasi, logs, dan service."""
    print_log("🗑️ Menghapus file konfigurasi dan logs...")

    if not python_path:
        print_log("Python Path tidak ditemukan di log, penghapusan file aplikasi dilewati.", "warning")
        return

    files_to_remove = [
        f"{python_path}/billacceptor.py",
        f"{python_path}/.env", ## DITAMBAHKAN ##
        "/etc/systemd/system/billacceptor.service",
        "/etc/ppp/peers/vpn",
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            run_command(f"sudo rm -f {file}")
        else:
            print_log(f"File {file} tidak ditemukan, mungkin sudah dihapus.", "warning")

    if log_dir and os.path.exists(log_dir):
        run_command(f"sudo rm -rf {log_dir}")

    if vpn_log and os.path.exists(vpn_log):
        run_command(f"sudo rm -rf {vpn_log}")

def disable_service():
    """Menonaktifkan dan menghapus service billacceptor."""
    print_log("🚫 Menonaktifkan dan menghapus service Bill Acceptor...")
    run_command("sudo systemctl stop billacceptor.service")
    run_command("sudo systemctl disable billacceptor.service")
    run_command("sudo rm -f /etc/systemd/system/billacceptor.service")
    run_command("sudo systemctl daemon-reload")

def reset_firewall(flask_port):
    """Menghapus aturan firewall UFW yang telah ditambahkan."""
    if not flask_port:
        print_log("Port Flask tidak ditemukan, penghapusan aturan firewall dilewati.", "warning")
        return
    print_log("🔐 Menghapus aturan firewall UFW...")
    run_command(f"sudo ufw delete allow {flask_port}")
    run_command("sudo ufw disable")


if __name__ == "__main__":
    print("\n🔧 **Rollback Bill Acceptor**\n")
    
    setup_log_path = "setup.log"
    config = read_setup_log(setup_log_path)
    
    # Menjalankan rollback otomatis
    remove_files(
        config.get("Python Path"), 
        config.get("LOG_DIR"), 
        config.get("VPN Log Path")
    )
    disable_service()
    reset_firewall(config.get("Flask Port"))
    uninstall_dependencies()
    
    print("\n🎉 **Rollback selesai!** 🎉")