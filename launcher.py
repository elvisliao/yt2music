#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick launcher for YouTube MP3 Professional Downloader
"""

import os
import sys
import subprocess
from pathlib import Path


def main():
    """Quick launcher with options"""
    print("🎵 YouTube MP3 Professional Downloader")
    print("=" * 40)
    print("1. 啟動 GUI 程式")
    print("2. 執行功能測試")
    print("3. 檢查環境")
    print("4. 啟動執行檔 (macOS)")
    print("5. 退出")

    try:
        choice = input("\n請選擇 (1-5): ").strip()

        if choice == "1":
            print("🚀 啟動 GUI 程式...")
            subprocess.run([sys.executable, "main.py"])

        elif choice == "2":
            print("🧪 執行功能測試...")
            subprocess.run([sys.executable, "test.py"])

        elif choice == "3":
            print("🔍 檢查環境...")
            check_environment()

        elif choice == "4":
            print("📱 啟動執行檔...")
            if Path("dist/YouTube_MP3_Downloader").exists():
                subprocess.run(["./dist/YouTube_MP3_Downloader"])
            elif Path("dist/YouTube_MP3_Downloader.app").exists():
                subprocess.run(["open", "dist/YouTube_MP3_Downloader.app"])
            else:
                print("❌ 執行檔不存在，請先執行打包")

        elif choice == "5":
            print("👋 再見！")
            return

        else:
            print("❌ 無效選擇")

    except KeyboardInterrupt:
        print("\n👋 再見！")
    except Exception as e:
        print(f"❌ 錯誤: {e}")


def check_environment():
    """Check system environment"""
    print(f"Python 版本: {sys.version}")
    print(f"作業系統: {os.name}")

    # Check required packages
    packages = ["customtkinter", "yt_dlp", "tkinter"]
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} - 已安裝")
        except ImportError:
            print(f"❌ {package} - 未安裝")

    # Check yt-dlp executable
    import shutil

    ytdlp_path = shutil.which("yt-dlp")
    if ytdlp_path:
        print(f"✅ yt-dlp - 已安裝 ({ytdlp_path})")
    else:
        print("❌ yt-dlp - 未找到")


if __name__ == "__main__":
    main()
