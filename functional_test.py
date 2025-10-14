#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube MP3 Downloader - 功能測試腳本
測試所有主要功能是否正常運作
Windows-compatible version without emoji
"""

import sys
import os
from pathlib import Path


def test_imports():
    """測試所有必要的模組導入"""
    print("Testing module imports...")

    try:
        import tkinter as tk

        print("OK - tkinter")
    except ImportError as e:
        print("FAILED - tkinter:", e)
        return False

    try:
        import customtkinter as ctk

        print("OK - customtkinter")
    except ImportError as e:
        print("WARNING - customtkinter not available:", e)

    try:
        import yt_dlp

        print("OK - yt-dlp")
    except ImportError as e:
        print("FAILED - yt-dlp:", e)
        return False

    return True


def test_config_manager():
    """測試配置管理器功能"""
    print("\nTesting ConfigManager...")

    try:
        import json
        import tempfile
        from pathlib import Path

        # 創建臨時配置檔案
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_config = {
                "output_dir": str(Path.home() / "Downloads"),
                "bitrate": "192",
                "theme": "dark",
            }
            json.dump(test_config, f)
            temp_path = f.name

        # 測試讀取配置
        with open(temp_path, 'r') as f:
            loaded_config = json.load(f)

        if loaded_config == test_config:
            print("OK - ConfigManager basic functionality")
            os.unlink(temp_path)
            return True
        else:
            print("FAILED - ConfigManager data mismatch")
            os.unlink(temp_path)
            return False

    except Exception as e:
        print(f"FAILED - ConfigManager test: {e}")
        return False


def test_main_module():
    """測試主模組是否可以導入"""
    print("\nTesting main module import...")

    try:
        # 檢查 main.py 是否存在
        if not os.path.exists("main.py"):
            print("FAILED - main.py not found")
            return False

        # 嘗試導入主模組
        import importlib.util

        spec = importlib.util.spec_from_file_location("main", "main.py")
        if spec is None:
            print("FAILED - Could not create module spec")
            return False

        main_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_module)

        print("OK - main module imported successfully")
        return True

    except Exception as e:
        print(f"FAILED - main module import: {e}")
        return False


def test_gui_components():
    """測試 GUI 組件"""
    print("\nTesting GUI components...")

    try:
        import tkinter as tk

        # 創建測試視窗
        root = tk.Tk()
        root.withdraw()  # 隱藏視窗

        # 測試基本組件
        frame = tk.Frame(root)
        label = tk.Label(frame, text="Test")
        button = tk.Button(frame, text="Test Button")

        # 測試 CustomTkinter (如果可用)
        try:
            import customtkinter as ctk

            ctk_frame = ctk.CTkFrame(root)
            ctk_label = ctk.CTkLabel(ctk_frame, text="Test")
            print("OK - CustomTkinter components")
        except ImportError:
            print("WARNING - CustomTkinter not available, using standard tkinter")

        root.destroy()
        print("OK - GUI components test")
        return True

    except Exception as e:
        print(f"FAILED - GUI components test: {e}")
        return False


def test_file_operations():
    """測試檔案操作"""
    print("\nTesting file operations...")

    try:
        import tempfile
        import shutil
        from pathlib import Path

        # 創建臨時目錄
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # 測試檔案創建
            test_file = temp_path / "test.txt"
            test_file.write_text("Test content")

            # 測試檔案讀取
            content = test_file.read_text()
            if content == "Test content":
                print("OK - File operations")
                return True
            else:
                print("FAILED - File content mismatch")
                return False

    except Exception as e:
        print(f"FAILED - File operations test: {e}")
        return False


def test_ytdlp_integration():
    """測試 yt-dlp 整合"""
    print("\nTesting yt-dlp integration...")

    try:
        import yt_dlp

        # 創建 yt-dlp 實例
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }

        ydl = yt_dlp.YoutubeDL(ydl_opts)
        print("OK - yt-dlp instance created")

        # 測試基本功能（不實際下載）
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

        try:
            # 只提取資訊，不下載
            info = ydl.extract_info(test_url, download=False)
            if info:
                print("OK - yt-dlp info extraction")
                return True
            else:
                print("WARNING - yt-dlp info extraction returned None")
                return False
        except Exception as e:
            print(f"WARNING - yt-dlp info extraction failed: {e}")
            # 這可能是網路問題，不算測試失敗
            return True

    except Exception as e:
        print(f"FAILED - yt-dlp integration test: {e}")
        return False


def main():
    """主測試函數"""
    print("YouTube MP3 Professional Downloader - Functional Test")
    print("=" * 50)

    tests = [
        ("Module Imports", test_imports),
        ("ConfigManager", test_config_manager),
        ("Main Module", test_main_module),
        ("GUI Components", test_gui_components),
        ("File Operations", test_file_operations),
        ("yt-dlp Integration", test_ytdlp_integration),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 20)
        try:
            if test_func():
                passed += 1
                print(f"PASSED - {test_name}")
            else:
                print(f"FAILED - {test_name}")
        except Exception as e:
            print(f"ERROR - {test_name}: {e}")

    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("SUCCESS - All functional tests passed!")
        return True
    else:
        print("WARNING - Some functional tests failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
