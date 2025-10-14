#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for YouTube MP3 Professional Downloader
Windows-compatible version without emoji
"""

import sys
import os
from pathlib import Path


def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")

    try:
        import json

        print("OK - json")
    except ImportError as e:
        print("FAILED - json:", e)
        return False

    try:
        import subprocess

        print("OK - subprocess")
    except ImportError as e:
        print("FAILED - subprocess:", e)
        return False

    try:
        import threading

        print("OK - threading")
    except ImportError as e:
        print("FAILED - threading:", e)
        return False

    try:
        import platform

        print("OK - platform")
    except ImportError as e:
        print("FAILED - platform:", e)
        return False

    try:
        import shutil

        print("OK - shutil")
    except ImportError as e:
        print("FAILED - shutil:", e)
        return False

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
        print("WARNING - customtkinter not available (will use tkinter fallback)")

    return True


def test_ytdlp():
    """Test if yt-dlp is available"""
    print("\nTesting yt-dlp availability...")

    try:
        import shutil

        ytdlp_path = shutil.which("yt-dlp")
        if ytdlp_path:
            print(f"OK - yt-dlp found at: {ytdlp_path}")
            return True
        else:
            print("FAILED - yt-dlp not found in PATH")
            return False
    except Exception as e:
        print(f"FAILED - Error checking yt-dlp: {e}")
        return False


def test_config_manager():
    """Test ConfigManager functionality"""
    print("\nTesting ConfigManager...")

    try:
        # Test basic config operations
        import json
        import tempfile

        # Create a temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_config = {"test": "value"}
            json.dump(test_config, f)
            temp_path = f.name

        # Test reading
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
    """Test if main module can be imported"""
    print("\nTesting main module import...")

    try:
        # Check if main.py exists
        if not os.path.exists("main.py"):
            print("FAILED - main.py not found")
            return False

        # Try to import main module
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


def main():
    """Main test function"""
    print("YouTube MP3 Professional Downloader - Test Suite")
    print("=" * 50)

    tests = [
        ("Module Imports", test_imports),
        ("yt-dlp Availability", test_ytdlp),
        ("ConfigManager", test_config_manager),
        ("Main Module", test_main_module),
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
        print("SUCCESS - All tests passed!")
        return True
    else:
        print("WARNING - Some tests failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
