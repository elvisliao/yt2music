#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick setup script for YouTube MP3 Professional Downloader
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"正在執行: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - 成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - 失敗: {e}")
        if e.stdout:
            print(f"輸出: {e.stdout}")
        if e.stderr:
            print(f"錯誤: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("YouTube MP3 Professional Downloader - 快速安裝")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ 需要 Python 3.10 或更高版本")
        print(f"目前版本: {sys.version}")
        return False
    
    print(f"✅ Python 版本: {sys.version}")
    
    # Install required packages
    packages = [
        ("pip install customtkinter", "安裝 CustomTkinter"),
        ("pip install yt-dlp", "安裝 yt-dlp"),
        ("pip install pyinstaller", "安裝 PyInstaller (可選)")
    ]
    
    success_count = 0
    for command, description in packages:
        if run_command(command, description):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"安裝結果: {success_count}/{len(packages)} 套件安裝成功")
    
    if success_count >= 2:  # At least customtkinter and yt-dlp
        print("🎉 安裝完成！現在可以執行程式了。")
        print("\n執行程式:")
        print("python main.py")
        
        # Ask if user wants to run the application
        try:
            response = input("\n是否現在執行程式？(y/n): ").lower().strip()
            if response in ['y', 'yes', '是']:
                print("正在啟動程式...")
                os.system("python main.py")
        except KeyboardInterrupt:
            print("\n安裝完成。")
    else:
        print("⚠️ 部分套件安裝失敗，請手動安裝:")
        print("pip install customtkinter yt-dlp")

if __name__ == "__main__":
    main()
