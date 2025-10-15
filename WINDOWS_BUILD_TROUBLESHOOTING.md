# Windows 建置問題排除指南

## 🚨 常見問題：Failed to load Python DLL

### 問題描述
```
Failed to load Python DLL
'C:\Users\admin\AppData\Local\Temp\_MEI59322\python311.dll'
LoadLibrary: 記憶體配置存取不正確
```

### 🔧 解決方案

#### 1. 使用 `--noupx` 參數
UPX 壓縮可能導致 DLL 載入問題：
```bash
pyinstaller --onefile --windowed --noupx --name "YouTube_MP3_Downloader" main.py
```

#### 2. 添加隱藏導入
確保所有必要的模組都被包含：
```bash
pyinstaller --onefile --windowed --noupx --hidden-import=customtkinter --hidden-import=yt_dlp --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=tkinter.messagebox --hidden-import=tkinter.filedialog --hidden-import=tkinter.simpledialog --hidden-import=json --hidden-import=subprocess --hidden-import=threading --hidden-import=platform --hidden-import=shutil --hidden-import=pathlib --name "YouTube_MP3_Downloader" main.py
```

#### 3. 使用控制台版本測試
先建置控制台版本來除錯：
```bash
pyinstaller --onefile --name "YouTube_MP3_Downloader_Console" main.py
```

#### 4. 檢查防毒軟體
- 暫時關閉 Windows Defender 即時保護
- 將建置目錄加入排除清單
- 檢查是否有其他防毒軟體干擾

#### 5. 使用虛擬環境
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install --upgrade pyinstaller
pyinstaller --onefile --windowed --noupx --name "YouTube_MP3_Downloader" main.py
```

### 🛠️ 進階修復方法

#### 方法 1：分離建置
```bash
# 先建置目錄版本
pyinstaller --onedir --windowed --noupx --name "YouTube_MP3_Downloader" main.py

# 測試目錄版本是否正常
dist\YouTube_MP3_Downloader\YouTube_MP3_Downloader.exe
```

#### 方法 2：使用 spec 檔案
建立 `build.spec`：
```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'customtkinter',
        'yt_dlp',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.simpledialog',
        'json',
        'subprocess',
        'threading',
        'platform',
        'shutil',
        'pathlib'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='YouTube_MP3_Downloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,  # 關閉 UPX
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

然後使用：
```bash
pyinstaller build.spec
```

### 🔍 除錯步驟

1. **檢查 Python 版本**
   ```bash
   python --version
   pyinstaller --version
   ```

2. **檢查依賴**
   ```bash
   pip list
   python -c "import customtkinter; print('OK')"
   python -c "import yt_dlp; print('OK')"
   ```

3. **測試基本建置**
   ```bash
   pyinstaller --onefile --name "test" --console main.py
   ```

4. **檢查建置日誌**
   - 查看 `build` 目錄中的日誌檔案
   - 檢查是否有警告或錯誤訊息

### 📋 建議的建置流程

1. **清理環境**
   ```bash
   rmdir /s build dist
   del *.spec
   ```

2. **更新套件**
   ```bash
   pip install --upgrade pip pyinstaller
   pip install -r requirements.txt
   ```

3. **使用穩定建置**
   ```bash
   pyinstaller --onefile --windowed --noupx --name "YouTube_MP3_Downloader" --optimize=2 --strip --hidden-import=customtkinter --hidden-import=yt_dlp --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=tkinter.messagebox --hidden-import=tkinter.filedialog --hidden-import=tkinter.simpledialog --hidden-import=json --hidden-import=subprocess --hidden-import=threading --hidden-import=platform --hidden-import=shutil --hidden-import=pathlib main.py
   ```

4. **測試執行檔**
   ```bash
   dist\YouTube_MP3_Downloader.exe
   ```

### ⚠️ 注意事項

- 確保使用 Python 3.10+ 版本
- 在乾淨的環境中建置
- 避免使用過舊的 PyInstaller 版本
- 檢查 Windows 更新是否影響建置

### 🆘 如果問題持續存在

1. 嘗試在不同的 Windows 機器上建置
2. 使用 Docker 容器建置
3. 考慮使用 GitHub Actions 自動建置
4. 回報問題到 PyInstaller GitHub 專案
