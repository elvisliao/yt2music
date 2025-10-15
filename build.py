#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for YouTube MP3 Professional Downloader
Creates executable files for different platforms
"""

import os
import sys
import platform
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"正在執行: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} - 成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - 失敗: {e}")
        return False

def build_executable():
    """Build executable using PyInstaller"""
    system = platform.system()
    
    print(f"正在為 {system} 平台建置執行檔...")
    
    # Base PyInstaller command
    base_cmd = "pyinstaller --onefile --windowed"
    
    # Platform-specific settings
    if system == "Windows":
        name = "YouTube_MP3_Downloader.exe"
        # Enhanced Windows build with better compatibility
        cmd = f"{base_cmd} --name YouTube_MP3_Downloader --noupx --hidden-import=customtkinter --hidden-import=yt_dlp --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=tkinter.messagebox --hidden-import=tkinter.filedialog --hidden-import=tkinter.simpledialog --hidden-import=json --hidden-import=subprocess --hidden-import=threading --hidden-import=platform --hidden-import=shutil --hidden-import=pathlib main.py"
    elif system == "Darwin":  # macOS
        name = "YouTube_MP3_Downloader"
        cmd = f"{base_cmd} --name YouTube_MP3_Downloader main.py"
    else:  # Linux
        name = "YouTube_MP3_Downloader"
        cmd = f"pyinstaller --onefile --name YouTube_MP3_Downloader main.py"
    
    # Add optimization flags
    cmd += " --optimize=2 --strip"
    
    # Ensure vendor binaries are included (yt-dlp external binary)
    vendor_dir = os.path.join(os.getcwd(), "vendor")
    if os.path.isdir(vendor_dir):
        cmd += f" --add-data \"{vendor_dir}{os.sep}*;vendor\""

    # Exclude unnecessary modules
    excludes = [
        "matplotlib", "numpy", "scipy", "pandas", "PIL", 
        "cv2", "tensorflow", "torch", "sklearn"
    ]
    
    for exclude in excludes:
        cmd += f" --exclude-module {exclude}"
    
    print(f"建置指令: {cmd}")
    
    if run_command(cmd, f"建置 {name}"):
        print(f"\n🎉 建置完成！")
        print(f"執行檔位置: dist/{name}")
        print(f"檔案大小: {get_file_size(f'dist/{name}')}")
        return True
    else:
        print("\n❌ 建置失敗")
        return False

def get_file_size(filepath):
    """Get file size in MB"""
    try:
        size_bytes = os.path.getsize(filepath)
        size_mb = size_bytes / (1024 * 1024)
        return f"{size_mb:.1f} MB"
    except FileNotFoundError:
        return "檔案不存在"

def clean_build():
    """Clean build directories"""
    print("正在清理建置檔案...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    files_to_clean = ["*.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            import shutil
            shutil.rmtree(dir_name)
            print(f"✅ 已刪除 {dir_name}")
    
    import glob
    for pattern in files_to_clean:
        for file_path in glob.glob(pattern):
            os.remove(file_path)
            print(f"✅ 已刪除 {file_path}")

def main():
    """Main build function"""
    print("YouTube MP3 Professional Downloader - 建置腳本")
    print("=" * 50)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"✅ PyInstaller 版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller 未安裝")
        print("請執行: pip install pyinstaller")
        return False
    
    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("❌ main.py 檔案不存在")
        return False
    
    print("✅ main.py 檔案存在")
    
    # Ask user for build options
    print("\n建置選項:")
    print("1. 清理並建置")
    print("2. 直接建置")
    print("3. 僅清理")
    
    try:
        choice = input("請選擇 (1-3): ").strip()
        
        if choice == "1":
            clean_build()
            print()
            build_executable()
        elif choice == "2":
            build_executable()
        elif choice == "3":
            clean_build()
        else:
            print("無效選擇，執行預設建置...")
            build_executable()
            
    except KeyboardInterrupt:
        print("\n建置已取消")
        return False
    
    print("\n建置完成！")

if __name__ == "__main__":
    main()
