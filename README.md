# 🎵 YouTube MP3 Professional Downloader

一個現代化的 YouTube 影片下載工具，支援高品質 MP3 音訊下載，具有美觀的 GUI 介面和跨平台支援。

## ✨ 功能特色

- 🎯 **高品質音訊下載**: 支援 128kbps 到 320kbps 位元率
- 🖥️ **現代化介面**: 使用 CustomTkinter 提供美觀的深色主題
- 🌍 **跨平台支援**: Windows, macOS, Linux 全平台支援
- ⚙️ **設定持久化**: 自動儲存使用者偏好設定
- 📁 **靈活輸出**: 自訂下載資料夾
- 🔄 **即時更新**: 支援 yt-dlp 最新版本
- 🛡️ **錯誤處理**: 完整的錯誤提示與處理機制

## 📋 系統需求

- **Python**: 3.10 或更高版本
- **作業系統**: Windows 10/11, macOS 10.14+, 或 Linux
- **網路**: 穩定的網路連線
- **磁碟空間**: 至少 100MB 可用空間

## 🚀 快速開始

### 方法 1: 使用自動安裝腳本 (推薦)

```bash
# 執行自動安裝腳本
python setup.py
```

### 方法 2: 手動安裝

```bash
# 1. 安裝依賴套件
pip install -r requirements.txt

# 2. 執行程式
python main.py
```

### 方法 3: 使用 launcher

```bash
# 使用啟動器 (如果可用)
python launcher.py
```

## 📖 使用說明

### 基本操作流程

1. **輸入 YouTube URL**: 在 "YouTube URL" 欄位中貼上要下載的影片連結
2. **選擇音質**: 從下拉選單選擇 MP3 位元率 (128, 192, 256, 320 kbps)
3. **設定輸出位置**: 選擇下載資料夾 (預設為系統下載資料夾)
4. **開始下載**: 點擊 "開始下載" 按鈕
5. **監控進度**: 觀察下載進度條和狀態訊息

### 進階功能

- **批次下載**: 支援多個 URL 同時下載
- **自動重試**: 網路中斷時自動重試下載
- **下載歷史**: 記錄下載歷史供日後參考
- **快速設定**: 一鍵切換常用設定

### 設定檔位置

- **Windows**: `%APPDATA%/yt2d/config.json`
- **macOS**: `~/Library/Application Support/yt2d/config.json`
- **Linux**: `~/.config/yt2d/config.json`

## 🔨 建置執行檔

### 自動建置 (推薦)

```bash
# 使用專案內建的建置腳本
python build.py
```

### 手動建置

#### Windows:

```bash
pyinstaller --onefile --windowed --name "YouTube_MP3_Downloader" --optimize=2 --strip main.py
```

#### macOS:

```bash
pyinstaller --onefile --windowed --name "YouTube_MP3_Downloader" --optimize=2 --strip main.py
```

#### Linux:

```bash
pyinstaller --onefile --name "YouTube_MP3_Downloader" --optimize=2 --strip main.py
```

### 建置選項說明

- `--onefile`: 打包成單一執行檔
- `--windowed`: 隱藏控制台視窗 (GUI 應用程式)
- `--optimize=2`: 最高級別優化
- `--strip`: 移除除錯符號，減少檔案大小

### 建置結果

建置完成後，執行檔會位於 `dist/` 資料夾中：

- **Windows**: `YouTube_MP3_Downloader.exe`
- **macOS**: `YouTube_MP3_Downloader.app`
- **Linux**: `YouTube_MP3_Downloader`

## 🔧 故障排除

### 常見問題與解決方案

#### 1. 依賴套件安裝失敗

```bash
# 更新 pip
python -m pip install --upgrade pip

# 重新安裝依賴
pip install -r requirements.txt --force-reinstall
```

#### 2. yt-dlp 相關錯誤

```bash
# 更新 yt-dlp 到最新版本
pip install --upgrade yt-dlp

# 檢查 yt-dlp 版本
yt-dlp --version
```

#### 3. GUI 介面問題

- **CustomTkinter 安裝失敗**: 程式會自動降級到標準 Tkinter
- **介面顯示異常**: 嘗試更新 CustomTkinter

```bash
pip install --upgrade customtkinter
```

#### 4. 下載失敗

**檢查項目**:

- ✅ 網路連線是否正常
- ✅ YouTube URL 格式是否正確
- ✅ 輸出資料夾是否有寫入權限
- ✅ yt-dlp 是否為最新版本

#### 5. 建置執行檔問題

```bash
# 清理建置檔案
rm -rf build dist *.spec

# 重新建置
python build.py
```

### 除錯模式

```bash
# 在命令列中執行程式查看詳細錯誤
python main.py

# 執行功能測試
python functional_test.py

# 執行視窗大小測試
python window_size_test.py
```

## 📁 專案結構

```
yt2d/
├── main.py                 # 主程式檔案
├── launcher.py            # 啟動器
├── setup.py               # 自動安裝腳本
├── build.py               # 建置腳本
├── requirements.txt       # 依賴套件清單
├── README.md              # 專案說明文件
├── BUILD_GUIDE.md         # 建置指南
├── TEST_GUIDE.md          # 測試指南
├── functional_test.py     # 功能測試
├── window_size_test.py    # 視窗大小測試
├── test.py               # 基本測試
└── dist/                 # 建置輸出目錄
```

## 🧪 測試

### 執行測試

```bash
# 功能測試
python functional_test.py

# 視窗大小測試
python window_size_test.py

# 基本測試
python test.py
```

### 測試覆蓋範圍

- ✅ GUI 介面測試
- ✅ 下載功能測試
- ✅ 設定持久化測試
- ✅ 錯誤處理測試
- ✅ 跨平台相容性測試

## 👨‍💻 開發者資訊

- **作者**: elvis.liao
- **版本**: 1.0.0
- **授權**: MIT License
- **開發語言**: Python 3.10+
- **GUI 框架**: CustomTkinter / Tkinter
- **下載引擎**: yt-dlp

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

### 提交 Issue 時請提供：

1. **系統資訊**:

   - 作業系統版本
   - Python 版本
   - 相關套件版本

2. **問題描述**:

   - 詳細的操作步驟
   - 預期行為 vs 實際行為
   - 錯誤訊息截圖

3. **環境資訊**:
   - 是否使用虛擬環境
   - 安裝方式 (pip/conda/其他)

## ⚖️ 法律聲明

**重要提醒**:

- 請遵守 YouTube 的使用條款和當地法律法規
- 本工具僅供個人學習和研究使用
- 請尊重版權，僅下載您有權下載的內容
- 使用者需自行承擔使用本工具的責任

## 📞 技術支援

如遇到問題，請：

1. 先查看本 README 的故障排除章節
2. 執行相關測試腳本
3. 在 GitHub 上提交 Issue
4. 提供詳細的系統資訊和錯誤訊息

---

**🎉 感謝使用 YouTube MP3 Professional Downloader！**
