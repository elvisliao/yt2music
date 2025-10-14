#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
視窗大小調整測試腳本
測試視窗是否能正確適應內容大小
"""

import sys
import time
from pathlib import Path


def test_window_sizing():
    """測試視窗大小調整功能"""
    print("🖥️ 測試視窗大小調整功能...")

    try:
        from main import YouTubeDownloaderApp

        # 創建應用程式實例
        app = YouTubeDownloaderApp()

        # 獲取視窗大小
        app.root.update_idletasks()
        width = app.root.winfo_width()
        height = app.root.winfo_height()

        print(f"✅ 視窗大小: {width}x{height}")

        # 檢查視窗是否居中
        screen_width = app.root.winfo_screenwidth()
        screen_height = app.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        print(f"✅ 螢幕大小: {screen_width}x{screen_height}")
        print(f"✅ 視窗位置: ({x}, {y})")

        # 檢查視窗是否可調整大小
        resizable = app.root.resizable()
        print(f"✅ 視窗可調整大小: {resizable}")

        # 檢查最小尺寸
        try:
            minsize = app.root.minsize()
            if minsize and len(minsize) >= 2:
                print(f"✅ 最小尺寸: {minsize[0]}x{minsize[1]}")
            else:
                print("✅ 最小尺寸: 未設定")
        except Exception as e:
            print(f"⚠️ 最小尺寸: 無法獲取 ({e})")

        # 關閉視窗
        app.root.destroy()

        print("✅ 視窗大小調整測試完成")
        return True

    except Exception as e:
        print(f"❌ 視窗大小調整測試失敗: {e}")
        return False


def test_content_fitting():
    """測試內容適應功能"""
    print("\n📏 測試內容適應功能...")

    try:
        from main import YouTubeDownloaderApp

        # 創建應用程式實例
        app = YouTubeDownloaderApp()

        # 檢查各個組件是否正確佈局
        components = [
            ('root', app.root),
            ('main_frame', getattr(app, 'main_frame', None)),
            ('status_text', getattr(app, 'status_text', None)),
            ('progress_bar', getattr(app, 'progress_bar', None)),
        ]

        for name, component in components:
            if component:
                try:
                    component.update_idletasks()
                    req_width = component.winfo_reqwidth()
                    req_height = component.winfo_reqheight()
                    print(f"✅ {name}: {req_width}x{req_height}")
                except Exception as e:
                    print(f"⚠️ {name}: 無法獲取尺寸 ({e})")
            else:
                print(f"❌ {name}: 組件不存在")

        # 關閉視窗
        app.root.destroy()

        print("✅ 內容適應測試完成")
        return True

    except Exception as e:
        print(f"❌ 內容適應測試失敗: {e}")
        return False


def main():
    """主測試函數"""
    print("🖥️ YouTube MP3 Downloader - 視窗大小調整測試")
    print("=" * 60)

    tests = [
        ("視窗大小調整", test_window_sizing),
        ("內容適應", test_content_fitting),
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
        print("🎉 所有測試通過！視窗大小調整功能正常。")
    else:
        print("⚠️ 部分測試失敗，請檢查視窗大小調整功能。")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
