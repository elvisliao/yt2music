# YouTube MP3 Professional Downloader - 測試指南

## 🧪 完整測試流程

### 前置檢查

1. **檢查 Python 版本**

   ```bash
   python --version
   # 應該顯示 Python 3.10 或更高版本
   ```

2. **檢查依賴套件**
   ```bash
   python test.py
   # 應該顯示 "All tests passed!"
   ```

### GUI 功能測試

#### 1. 啟動程式

```bash
python main.py
```

#### 2. 介面測試

- ✅ **Banner 區域**: 檢查是否顯示 "▶️ YouTube MP3 Professional Downloader"
- ✅ **URL 輸入框**: 檢查是否顯示佔位符文字 "請輸入 YouTube 影片連結..."
- ✅ **位元率選擇**: 檢查下拉選單是否包含 128, 192, 256, 320 選項
- ✅ **輸出資料夾**: 檢查是否顯示預設下載資料夾路徑
- ✅ **瀏覽按鈕**: 點擊測試資料夾選擇功能
- ✅ **狀態區域**: 檢查是否顯示 "準備就緒。請輸入 YouTube URL 開始下載。"
- ✅ **作者聲明**: 檢查是否顯示 "Made with ❤️ by elvis.liao"

#### 3. 設定持久化測試

1. **改變位元率**: 選擇不同的位元率 (如 256)
2. **改變輸出資料夾**: 點擊瀏覽選擇新資料夾
3. **關閉程式**: 關閉 GUI 視窗
4. **重新啟動**: 再次執行 `python main.py`
5. **驗證設定**: 檢查位元率和輸出資料夾是否保持上次的設定

#### 4. 下載功能測試

**測試 URL 範例**:

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/dQw4w9WgXcQ
```

**測試步驟**:

1. **輸入 URL**: 在 URL 輸入框中貼上測試連結
2. **選擇位元率**: 選擇 192 kbps (預設)
3. **確認輸出資料夾**: 確保有寫入權限
4. **開始下載**: 點擊 "開始下載" 按鈕
5. **觀察狀態**: 檢查狀態區域是否顯示下載進度
6. **等待完成**: 等待下載完成訊息
7. **檢查檔案**: 確認 MP3 檔案已下載到指定資料夾

#### 5. 錯誤處理測試

**無效 URL 測試**:

```
https://invalid-url.com
not-a-url
```

**預期行為**:

- 顯示錯誤訊息 "請輸入有效的 YouTube URL"
- 下載按鈕保持可用狀態

**網路問題測試**:

- 斷開網路連線
- 嘗試下載
- 預期顯示網路相關錯誤訊息

### 執行檔測試

#### macOS 測試

```bash
# 測試獨立執行檔
./dist/YouTube_MP3_Downloader

# 測試應用程式套件
open dist/YouTube_MP3_Downloader.app
```

#### Windows 測試

```bash
# 在 Windows 命令提示字元中
dist\YouTube_MP3_Downloader.exe
```

### 跨平台測試

#### macOS 特定測試

- ✅ GUI 主題是否正確顯示
- ✅ 檔案權限是否正常
- ✅ 設定檔是否儲存在正確位置 (`~/Library/Application Support/yt2d/`)

#### Windows 特定測試

- ✅ 程式是否在 Windows 上正常啟動
- ✅ 設定檔是否儲存在正確位置 (`%APPDATA%/yt2d/`)
- ✅ 中文顯示是否正常

### 效能測試

#### 1. 記憶體使用

```bash
# macOS
top -pid $(pgrep -f "python main.py")

# Windows
tasklist /fi "imagename eq python.exe"
```

#### 2. 下載速度測試

- 測試不同長度的影片下載
- 測試不同位元率的轉換速度
- 測試多個下載的處理能力

### 故障排除測試

#### 1. yt-dlp 未安裝

```bash
# 暫時移除 yt-dlp
pip uninstall yt-dlp
python main.py
# 應該顯示 yt-dlp 未找到的錯誤訊息
pip install yt-dlp
```

#### 2. CustomTkinter 未安裝

```bash
# 暫時移除 CustomTkinter
pip uninstall customtkinter
python main.py
# 應該自動降級到標準 Tkinter
pip install customtkinter
```

#### 3. 權限問題

- 測試在沒有寫入權限的資料夾中下載
- 測試設定檔目錄的權限問題

## 📊 測試結果記錄

### 測試環境

- **作業系統**:
- **Python 版本**:
- **測試日期**:
- **測試人員**:

### 功能測試結果

- [ ] GUI 啟動正常
- [ ] 介面元素顯示正確
- [ ] 設定持久化正常
- [ ] URL 驗證正常
- [ ] 下載功能正常
- [ ] 錯誤處理正常
- [ ] 執行檔運行正常

### 效能測試結果

- **啟動時間**: \_\_\_ 秒
- **記憶體使用**: \_\_\_ MB
- **下載速度**: \_\_\_ MB/s

### 發現問題

1.
2.
3.

### 建議改進

1.
2.
3.

---

## 🎯 快速測試指令

```bash
# 1. 檢查環境
python test.py

# 2. 啟動程式
python main.py

# 3. 測試執行檔 (macOS)
./dist/YouTube_MP3_Downloader

# 4. 測試執行檔 (Windows)
dist\YouTube_MP3_Downloader.exe
```

## 📝 測試報告範本

```
測試報告 - YouTube MP3 Professional Downloader
===============================================

測試環境:
- OS: macOS 15.6.1
- Python: 3.13.5
- 測試日期: 2024-10-14

測試結果:
✅ 所有基本功能正常
✅ GUI 介面美觀且易用
✅ 設定持久化正常
✅ 下載功能穩定
✅ 錯誤處理完善
✅ 跨平台相容性良好

建議:
- 程式運行穩定，可以正式使用
- 建議定期更新 yt-dlp 以獲得最佳相容性
```
