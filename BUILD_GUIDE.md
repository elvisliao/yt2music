# 🏗️ YouTube MP3 Professional Downloader - 建置指南

## 📋 建置方式總覽

### 1. 自動建置 (推薦)

```bash
# 使用自動建置腳本
python build.py
```

### 2. 手動建置

```bash
# 基本建置
pyinstaller --onefile --windowed --name YouTube_MP3_Downloader main.py

# 優化建置 (推薦)
pyinstaller --onefile --windowed --name YouTube_MP3_Downloader --optimize=2 --strip main.py
```

### 3. 進階建置選項

#### macOS 建置

```bash
# 基本 macOS 建置
pyinstaller --onefile --windowed --name YouTube_MP3_Downloader main.py

# 包含圖示 (如果有 icon.icns)
pyinstaller --onefile --windowed --icon=icon.icns --name YouTube_MP3_Downloader main.py

# 排除不需要的模組 (減少檔案大小)
pyinstaller --onefile --windowed --exclude-module matplotlib --exclude-module numpy --name YouTube_MP3_Downloader main.py
```

#### Windows 建置

```bash
# 基本 Windows 建置
pyinstaller --onefile --windowed --name YouTube_MP3_Downloader main.py

# 包含圖示 (如果有 icon.ico)
pyinstaller --onefile --windowed --icon=icon.ico --name YouTube_MP3_Downloader main.py

# Windows 特定優化
pyinstaller --onefile --windowed --name YouTube_MP3_Downloader --optimize=2 --strip --exclude-module matplotlib main.py
```

## 🔧 建置參數說明

### 基本參數

- `--onefile`: 打包成單一執行檔
- `--windowed`: 隱藏控制台視窗 (GUI 應用程式)
- `--name`: 指定執行檔名稱

### 優化參數

- `--optimize=2`: 最高級別優化
- `--strip`: 移除除錯符號
- `--exclude-module`: 排除不需要的模組

### 進階參數

- `--icon`: 指定圖示檔案
- `--hidden-import`: 強制包含隱藏模組
- `--add-data`: 添加額外資料檔案

## 📁 建置輸出

### macOS

```
dist/
├── YouTube_MP3_Downloader          # 獨立執行檔
└── YouTube_MP3_Downloader.app/     # macOS 應用程式套件
    └── Contents/
        ├── MacOS/
        │   └── YouTube_MP3_Downloader
        ├── Resources/
        └── Info.plist
```

### Windows

```
dist/
└── YouTube_MP3_Downloader.exe     # Windows 執行檔
```

## 🚀 建置步驟

### 步驟 1: 準備環境

```bash
# 確保 Python 3.10+ 已安裝
python --version

# 安裝必要套件
pip install -r requirements.txt

# 或手動安裝
pip install customtkinter yt-dlp pyinstaller
```

### 步驟 2: 測試程式

```bash
# 執行功能測試
python functional_test.py

# 手動測試
python main.py
```

### 步驟 3: 執行建置

```bash
# 清理舊的建置檔案
rm -rf build dist *.spec

# 執行建置
pyinstaller --onefile --windowed --name YouTube_MP3_Downloader --optimize=2 --strip main.py
```

### 步驟 4: 測試執行檔

```bash
# macOS
./dist/YouTube_MP3_Downloader
# 或
open dist/YouTube_MP3_Downloader.app

# Windows
dist\YouTube_MP3_Downloader.exe
```

## 🔍 建置問題排除

### 常見問題

#### 1. 模組未找到

```bash
# 解決方案：添加隱藏導入
pyinstaller --onefile --windowed --hidden-import=customtkinter --hidden-import=yt_dlp main.py
```

#### 2. 檔案過大

```bash
# 解決方案：排除不需要的模組
pyinstaller --onefile --windowed --exclude-module matplotlib --exclude-module numpy --exclude-module scipy main.py
```

#### 3. 執行檔無法啟動

```bash
# 檢查依賴
ldd dist/YouTube_MP3_Downloader  # Linux
otool -L dist/YouTube_MP3_Downloader  # macOS
```

#### 4. macOS 安全警告

```bash
# 解決方案：移除隔離屬性
xattr -d com.apple.quarantine dist/YouTube_MP3_Downloader
```

### 除錯模式

```bash
# 建置除錯版本
pyinstaller --onefile --name YouTube_MP3_Downloader main.py

# 查看詳細輸出
pyinstaller --onefile --name YouTube_MP3_Downloader --log-level=DEBUG main.py
```

## 📊 建置結果比較

### 檔案大小對比

| 建置方式 | macOS | Windows | 說明           |
| -------- | ----- | ------- | -------------- |
| 基本建置 | ~15MB | ~12MB   | 包含所有模組   |
| 優化建置 | ~10MB | ~8MB    | 移除除錯符號   |
| 精簡建置 | ~8MB  | ~6MB    | 排除不必要模組 |

### 啟動時間對比

| 建置方式 | 冷啟動 | 熱啟動 | 說明     |
| -------- | ------ | ------ | -------- |
| 基本建置 | 3-5 秒 | 1-2 秒 | 標準配置 |
| 優化建置 | 2-3 秒 | <1 秒  | 優化配置 |
| 精簡建置 | 1-2 秒 | <1 秒  | 最小配置 |

## 🎯 建置最佳實踐

### 1. 開發階段

```bash
# 快速建置測試
pyinstaller --onefile --name YouTube_MP3_Downloader main.py
```

### 2. 測試階段

```bash
# 完整功能建置
pyinstaller --onefile --windowed --name YouTube_MP3_Downloader --optimize=2 main.py
```

### 3. 發布階段

```bash
# 最終優化建置
pyinstaller --onefile --windowed --name YouTube_MP3_Downloader --optimize=2 --strip --exclude-module matplotlib --exclude-module numpy main.py
```

## 📝 建置檢查清單

### 建置前檢查

- [ ] Python 3.10+ 已安裝
- [ ] 所有依賴套件已安裝
- [ ] 程式功能測試通過
- [ ] 無語法錯誤

### 建置後檢查

- [ ] 執行檔成功生成
- [ ] 檔案大小合理
- [ ] 執行檔可正常啟動
- [ ] GUI 介面正常顯示
- [ ] 所有功能正常運作

### 發布前檢查

- [ ] 跨平台測試通過
- [ ] 效能測試通過
- [ ] 錯誤處理測試通過
- [ ] 使用者體驗測試通過

---

## 🎉 建置完成！

建置成功後，您將獲得：

- ✅ 跨平台執行檔
- ✅ 現代化 GUI 介面
- ✅ 完整功能支援
- ✅ 優化的效能表現

**建置指令總結**:

```bash
# 一鍵建置
pyinstaller --onefile --windowed --name YouTube_MP3_Downloader --optimize=2 --strip main.py
```
