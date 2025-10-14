#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for YouTube MP3 Professional Downloader
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import json
        print("✅ json - OK")
    except ImportError as e:
        print(f"❌ json - FAILED: {e}")
        return False
    
    try:
        import subprocess
        print("✅ subprocess - OK")
    except ImportError as e:
        print(f"❌ subprocess - FAILED: {e}")
        return False
    
    try:
        import threading
        print("✅ threading - OK")
    except ImportError as e:
        print(f"❌ threading - FAILED: {e}")
        return False
    
    try:
        import platform
        print("✅ platform - OK")
    except ImportError as e:
        print(f"❌ platform - FAILED: {e}")
        return False
    
    try:
        import shutil
        print("✅ shutil - OK")
    except ImportError as e:
        print(f"❌ shutil - FAILED: {e}")
        return False
    
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
        print("⚠️ customtkinter - Not available (will use tkinter fallback)")
    
    return True

def test_ytdlp():
    """Test if yt-dlp is available"""
    print("\nTesting yt-dlp availability...")
    
    try:
        import shutil
        ytdlp_path = shutil.which("yt-dlp")
        if ytdlp_path:
            print(f"✅ yt-dlp found at: {ytdlp_path}")
            return True
        else:
            print("❌ yt-dlp not found in PATH")
            return False
    except Exception as e:
        print(f"❌ Error checking yt-dlp: {e}")
        return False

def test_config_manager():
    """Test ConfigManager functionality"""
    print("\nTesting ConfigManager...")
    
    try:
        # Import the main module
        sys.path.insert(0, str(Path(__file__).parent))
        from main import ConfigManager
        
        config = ConfigManager()
        print("✅ ConfigManager created successfully")
        
        # Test getting default values
        bitrate = config.get("mp3_bitrate", 192)
        print(f"✅ Default bitrate: {bitrate}")
        
        # Test setting values
        config.set("test_key", "test_value")
        retrieved_value = config.get("test_key")
        if retrieved_value == "test_value":
            print("✅ Config save/load working")
        else:
            print("❌ Config save/load failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ ConfigManager test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("YouTube MP3 Professional Downloader - Test Suite")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    if test_imports():
        tests_passed += 1
    
    if test_ytdlp():
        tests_passed += 1
    
    if test_config_manager():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The application should work correctly.")
    else:
        print("⚠️ Some tests failed. Please check the requirements.")
    
    print("\nTo run the application:")
    print("python main.py")

if __name__ == "__main__":
    main()
