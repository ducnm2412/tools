#!/usr/bin/env python3
"""
Script để build ứng dụng ADB Scroll Phone Farm thành file executable
"""

import os
import sys
import subprocess

def install_pyinstaller():
    """Cài đặt PyInstaller nếu chưa có"""
    try:
        import PyInstaller
        print("✓ PyInstaller đã được cài đặt")
    except ImportError:
        print("Đang cài đặt PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ Đã cài đặt PyInstaller thành công")

def build_app():
    """Build ứng dụng thành file executable"""
    print("Bắt đầu build ứng dụng...")
    
    # Tên ứng dụng
    app_name = "ADB_Scroll_Phone_Farm"
    
    # Lệnh build
    build_command = [
        "pyinstaller",
        "--onefile",                    # Tạo 1 file duy nhất
        "--windowed",                   # Không hiển thị console (cho GUI app)
        "--name", app_name,             # Tên file output
        "--icon=icon.ico",              # Icon (nếu có)
        "--add-data", "requirements.txt;.",  # Thêm file requirements
        "watch_video.py"                # File source chính
    ]
    
    # Nếu không có icon, bỏ qua tham số icon
    if not os.path.exists("icon.ico"):
        build_command = [cmd for cmd in build_command if not cmd.startswith("--icon")]
    
    try:
        subprocess.check_call(build_command)
        print(f"✓ Build thành công! File executable: dist/{app_name}")
        
        # Hiển thị thông tin về file đã tạo
        exe_path = f"dist/{app_name}"
        if os.path.exists(exe_path):
            size = os.path.getsize(exe_path) / (1024 * 1024)  # Convert to MB
            print(f"📁 Kích thước file: {size:.2f} MB")
            print(f"📍 Đường dẫn: {os.path.abspath(exe_path)}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi build: {e}")
        return False
    
    return True

def create_installer_script():
    """Tạo script cài đặt đơn giản"""
    installer_content = """#!/bin/bash
# Script cài đặt ADB Scroll Phone Farm

echo "=== Cài đặt ADB Scroll Phone Farm ==="
echo ""

# Kiểm tra ADB
if ! command -v adb &> /dev/null; then
    echo "❌ ADB chưa được cài đặt!"
    echo "Vui lòng cài đặt Android SDK Platform Tools trước:"
    echo "https://developer.android.com/studio/releases/platform-tools"
    exit 1
fi

echo "✓ ADB đã được cài đặt"

# Tạo desktop shortcut (cho Linux/macOS)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Tạo desktop shortcut..."
    cat > ~/Desktop/ADB_Scroll_Phone_Farm.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=ADB Scroll Phone Farm
Comment=Ứng dụng scroll tự động cho phone farm
Exec=$(pwd)/ADB_Scroll_Phone_Farm
Icon=$(pwd)/icon.png
Terminal=false
Categories=Utility;
EOF
    chmod +x ~/Desktop/ADB_Scroll_Phone_Farm.desktop
    echo "✓ Đã tạo desktop shortcut"
fi

echo ""
echo "🎉 Cài đặt hoàn tất!"
echo "Bạn có thể chạy ứng dụng bằng cách:"
echo "1. Double-click vào file ADB_Scroll_Phone_Farm"
echo "2. Hoặc chạy từ terminal: ./ADB_Scroll_Phone_Farm"
"""

    with open("install.sh", "w") as f:
        f.write(installer_content)
    
    # Làm cho script có thể thực thi (Linux/macOS)
    os.chmod("install.sh", 0o755)
    print("✓ Đã tạo script cài đặt: install.sh")

def main():
    """Hàm chính"""
    print("🚀 ADB Scroll Phone Farm - Builder")
    print("=" * 40)
    
    # Cài đặt PyInstaller
    install_pyinstaller()
    
    # Build ứng dụng
    if build_app():
        print("\n🎯 Build hoàn tất!")
        
        # Tạo script cài đặt
        create_installer_script()
        
        print("\n📋 Hướng dẫn sử dụng:")
        print("1. File executable nằm trong thư mục 'dist/'")
        print("2. Copy file này đến máy đích")
        print("3. Chạy file để sử dụng ứng dụng")
        print("4. Đảm bảo máy đích đã cài ADB")
        
        if os.name == "nt":  # Windows
            print("\n💡 Trên Windows, bạn có thể:")
            print("- Tạo shortcut trên desktop")
            print("- Pin vào Start menu")
            print("- Thêm vào PATH để chạy từ Command Prompt")
        else:  # Linux/macOS
            print("\n💡 Trên Linux/macOS:")
            print("- Chạy ./install.sh để tạo desktop shortcut")
            print("- Hoặc chạy trực tiếp: ./ADB_Scroll_Phone_Farm")
    
    else:
        print("\n❌ Build thất bại!")
        print("Vui lòng kiểm tra lỗi và thử lại")

if __name__ == "__main__":
    main()
