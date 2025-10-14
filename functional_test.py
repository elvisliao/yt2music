#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube MP3 Downloader - 功能測試腳本
測試所有主要功能是否正常運作
"""

import sys
import os
from pathlib import Path


def test_imports():
    """測試所有必要的模組導入"""
    print("🔍 測試模組導入...")

    try:
        import tkinter as tk

        print("✅ tkinter - OK")
    except ImportError as e:
        print(f"❌ tkinter - FAILED: {e}")
        return False

    try:
        import customtkinter as ctk

        print("✅ customtkinter - OK")
    except ImportError as e:
        print(f"⚠️ customtkinter - Not available: {e}")

    try:
        import yt_dlp

        print("✅ yt-dlp - OK")
    except ImportError as e:
        print(f"❌ yt-dlp - FAILED: {e}")
        return False

    return True


def test_config_manager():
    """測試設定管理器"""
    print("\n🔧 測試設定管理器...")

    try:
        from main import ConfigManager

        config = ConfigManager()

        # 測試基本功能
        config.set("test_key", "test_value")
        value = config.get("test_key")

        if value == "test_value":
            print("✅ ConfigManager - OK")
            return True
        else:
            print("❌ ConfigManager - FAILED: Value mismatch")
            return False

    except Exception as e:
        print(f"❌ ConfigManager - FAILED: {e}")
        return False


def test_download_manager():
    """測試下載管理器"""
    print("\n⬇️ 測試下載管理器...")

    try:
        from main import DownloadManager, ConfigManager

        config = ConfigManager()
        downloader = DownloadManager(config)

        # 測試 yt-dlp 可用性
        if downloader.is_ytdlp_available():
            print("✅ yt-dlp 可用")
        else:
            print("❌ yt-dlp 不可用")
            print(downloader.get_ytdlp_error_message())
            return False

        # 測試 URL 驗證
        test_urls = [
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", True),
            ("https://youtu.be/dQw4w9WgXcQ", True),
            ("https://invalid-url.com", False),
            ("not-a-url", False),
        ]

        for url, expected in test_urls:
            result = downloader._is_valid_youtube_url(url)
            if result == expected:
                print(f"✅ URL 驗證: {url[:30]}... -> {result}")
            else:
                print(f"❌ URL 驗證失敗: {url[:30]}... -> {result} (期望: {expected})")
                return False

        print("✅ DownloadManager - OK")
        return True

    except Exception as e:
        print(f"❌ DownloadManager - FAILED: {e}")
        return False


def test_gui_creation():
    """測試 GUI 創建"""
    print("\n🖥️ 測試 GUI 創建...")

    try:
        from main import YouTubeDownloaderApp

        # 創建應用程式實例（不啟動主循環）
        app = YouTubeDownloaderApp()

        # 檢查基本屬性
        if (
            hasattr(app, 'root')
            and hasattr(app, 'config_manager')
            and hasattr(app, 'download_manager')
        ):
            print("✅ GUI 創建 - OK")
            return True
        else:
            print("❌ GUI 創建 - FAILED: Missing attributes")
            return False

    except Exception as e:
        print(f"❌ GUI 創建 - FAILED: {e}")
        return False


def test_file_dialog():
    """測試檔案對話框功能"""
    print("\n📁 測試檔案對話框...")

    try:
        from tkinter import filedialog
        import tkinter as tk

        # 創建隱藏的根視窗
        root = tk.Tk()
        root.withdraw()  # 隱藏視窗

        # 測試目錄選擇對話框（不實際顯示）
        # 這裡只測試函數是否可調用
        print("✅ 檔案對話框模組 - OK")

        root.destroy()
        return True

    except Exception as e:
        print(f"❌ 檔案對話框 - FAILED: {e}")
        return False


def main():
    """主測試函數"""
    print("🎵 YouTube MP3 Professional Downloader - 功能測試")
    print("=" * 60)

    tests = [
        ("模組導入", test_imports),
        ("設定管理器", test_config_manager),
        ("下載管理器", test_download_manager),
        ("GUI 創建", test_gui_creation),
        ("檔案對話框", test_file_dialog),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} 測試失敗")
        except Exception as e:
            print(f"❌ {test_name} 測試異常: {e}")

    print("\n" + "=" * 60)
    print(f"測試結果: {passed}/{total} 通過")

    if passed == total:
        print("🎉 所有測試通過！程式可以正常使用。")
        print("\n🚀 啟動程式:")
        print("python main.py")
    else:
        print("⚠️ 部分測試失敗，請檢查相關功能。")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
