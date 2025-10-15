#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube MP3 Professional Downloader (YT-MP3 Pro Downloader)
A cross-platform YouTube to MP3 downloader with modern GUI

Author: elvis.liao
Version: 1.0.0
Python: 3.10+
"""

import os
import sys
import json
import subprocess
import threading
import platform
from pathlib import Path
from typing import Optional, Dict, Any
import shutil

# Try to import CustomTkinter, fallback to Tkinter if not available
try:
    import customtkinter as ctk
    from customtkinter import (
        CTk,
        CTkFrame,
        CTkLabel,
        CTkEntry,
        CTkButton,
        CTkOptionMenu,
        CTkTextbox,
    )
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox

    CUSTOM_TKINTER_AVAILABLE = True
except ImportError:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox

    CUSTOM_TKINTER_AVAILABLE = False
    # Create aliases for compatibility
    CTk = tk.Tk
    CTkFrame = tk.Frame
    CTkLabel = tk.Label
    CTkEntry = tk.Entry
    CTkButton = tk.Button
    CTkOptionMenu = ttk.Combobox
    CTkTextbox = tk.Text


class ConfigManager:
    """Manages application configuration persistence"""

    def __init__(self):
        self.config_dir = self._get_config_directory()
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_default_config()
        self._ensure_config_dir()
        self.load_config()

    def _get_config_directory(self) -> Path:
        """Get platform-specific config directory"""
        system = platform.system()

        if system == "Windows":
            config_dir = Path(os.environ.get("APPDATA", "")) / "yt2d"
        elif system == "Darwin":  # macOS
            config_dir = Path.home() / "Library" / "Application Support" / "yt2d"
        else:  # Linux and others
            config_dir = Path.home() / ".config" / "yt2d"

        return config_dir

    def _get_default_download_dir(self) -> str:
        """Get platform-specific default download directory"""
        system = platform.system()

        if system == "Windows":
            downloads_dir = Path.home() / "Downloads"
        elif system == "Darwin":  # macOS
            downloads_dir = Path.home() / "Downloads"
        else:  # Linux and others
            downloads_dir = Path.home() / "Downloads"

        return str(downloads_dir)

    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration"""
        return {
            "mp3_bitrate": 192,
            "output_directory": self._get_default_download_dir(),
            "window_geometry": "800x600",
            "theme": "dark",
            # External yt-dlp updater
            "ytdlp_auto_update": True,
            "ytdlp_update_channel": "nightly",
        }

    def _ensure_config_dir(self):
        """Ensure config directory exists"""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}")
                # Use default config if loading fails

    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving config: {e}")

    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Set configuration value and save immediately"""
        self.config[key] = value
        self.save_config()


class DownloadManager:
    """Manages YouTube download operations using yt-dlp"""

    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        # Prefer external managed yt-dlp so it can auto-update
        try:
            from ytdlp_manager import find_or_install_ytdlp  # lazy import

            update_channel = str(self.config.get("ytdlp_update_channel", "nightly"))
            auto_update = bool(self.config.get("ytdlp_auto_update", True))
            external = find_or_install_ytdlp(Path.cwd(), channel=update_channel, auto_update=auto_update)
        except Exception:
            external = None

        self.ytdlp_path = external or self._find_ytdlp_executable()
        self.is_downloading = False
        self.current_process = None

    def _find_ytdlp_executable(self) -> Optional[str]:
        """Find yt-dlp executable in system PATH or common locations"""
        # First try to find in PATH
        ytdlp_path = shutil.which("yt-dlp")
        if ytdlp_path:
            return ytdlp_path

        # Try platform-specific executable names
        system = platform.system()
        if system == "Windows":
            executable_names = ["yt-dlp.exe", "yt-dlp"]
        else:
            executable_names = ["yt-dlp"]

        for name in executable_names:
            path = shutil.which(name)
            if path:
                return path

        # Try common installation locations
        common_paths = [
            Path.cwd() / "yt-dlp.exe" if system == "Windows" else Path.cwd() / "yt-dlp",
            Path.home() / ".local" / "bin" / "yt-dlp",
            Path("/usr/local/bin/yt-dlp"),
            Path("/usr/bin/yt-dlp"),
        ]

        for path in common_paths:
            if path.exists() and path.is_file():
                return str(path)

        return None

    def is_ytdlp_available(self) -> bool:
        """Check if yt-dlp is available"""
        return self.ytdlp_path is not None and Path(self.ytdlp_path).exists()

    def get_ytdlp_error_message(self) -> str:
        """Get error message for missing yt-dlp"""
        system = platform.system()
        if system == "Windows":
            return (
                "yt-dlp 未找到或無法執行。程式將嘗試自動下載最新 yt-dlp.exe 到 _bin 資料夾。\n"
                "若仍無法使用，請手動下載 yt-dlp.exe 並放置於程式目錄或加入 PATH，\n"
                "或使用 pip install yt-dlp 安裝。"
            )
        else:
            return (
                "yt-dlp 未找到或無法執行。程式將嘗試自動安裝到 _bin。\n"
                "若失敗，請手動安裝：pip install yt-dlp 或使用系統套件管理工具。"
            )

    def _build_command(self, url: str) -> list:
        """Build yt-dlp command with current settings"""
        bitrate = self.config.get("mp3_bitrate", 192)
        output_dir = self.config.get("output_directory", "")

        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Build command
        cmd = [
            self.ytdlp_path,
            "-x",  # Extract audio only
            "--audio-format",
            "mp3",
            "--audio-quality",
            f"{bitrate}K",
            "--embed-thumbnail",
            "--add-metadata",
            "-o",
            f"{output_dir}/%(title)s.%(ext)s",
            url,
        ]

        return cmd

    def download(self, url: str, progress_callback=None, completion_callback=None):
        """Start download in background thread"""
        if self.is_downloading:
            if progress_callback:
                progress_callback("下載進行中，請稍候...")
            return False

        if not self.is_ytdlp_available():
            if progress_callback:
                progress_callback(f"錯誤：{self.get_ytdlp_error_message()}")
            return False

        if not url.strip():
            if progress_callback:
                progress_callback("請輸入有效的 YouTube URL")
            return False

        # Validate URL
        if not self._is_valid_youtube_url(url):
            if progress_callback:
                progress_callback("請輸入有效的 YouTube URL")
            return False

        self.is_downloading = True

        def download_thread():
            try:
                cmd = self._build_command(url)

                if progress_callback:
                    progress_callback("正在準備下載...")

                # Start process
                if platform.system() == "Windows":
                    self.current_process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW,
                    )
                else:
                    self.current_process = subprocess.Popen(
                        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                    )

                if progress_callback:
                    progress_callback("開始下載... 請稍候")

                # Wait for completion
                stdout, stderr = self.current_process.communicate()

                if self.current_process.returncode == 0:
                    if progress_callback:
                        progress_callback("✅ 下載完成！")
                    if completion_callback:
                        completion_callback(True, "下載成功完成")
                else:
                    error_msg = stderr.strip() or stdout.strip() or "未知錯誤"
                    if progress_callback:
                        progress_callback(f"❌ 下載失敗：{error_msg}")
                    if completion_callback:
                        completion_callback(False, error_msg)

            except Exception as e:
                error_msg = f"下載過程中發生錯誤：{str(e)}"
                if progress_callback:
                    progress_callback(f"❌ {error_msg}")
                if completion_callback:
                    completion_callback(False, error_msg)
            finally:
                self.is_downloading = False
                self.current_process = None

        # Start download in background thread
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()

        return True

    def _is_valid_youtube_url(self, url: str) -> bool:
        """Basic YouTube URL validation"""
        youtube_domains = [
            "youtube.com",
            "www.youtube.com",
            "youtu.be",
            "m.youtube.com",
        ]

        url_lower = url.lower().strip()
        return any(domain in url_lower for domain in youtube_domains)

    def cancel_download(self):
        """Cancel current download"""
        if self.current_process and self.is_downloading:
            try:
                self.current_process.terminate()
                self.is_downloading = False
                return True
            except Exception:
                return False
        return False


class YouTubeDownloaderApp:
    """Main application GUI"""

    def __init__(self):
        self.config_manager = ConfigManager()
        self.download_manager = DownloadManager(self.config_manager)

        # Initialize GUI
        if CUSTOM_TKINTER_AVAILABLE:
            self.root = CTk()
            self._setup_customtkinter()
        else:
            self.root = CTk()
            self._setup_tkinter()

        self._setup_ui()
        self._load_settings()
        # Adjust window size to fit content
        self._adjust_window_size()

    def _setup_customtkinter(self):
        """Setup CustomTkinter theme and appearance"""
        ctk.set_appearance_mode(self.config_manager.get("theme", "dark"))
        ctk.set_default_color_theme("blue")

        self.root.title("YouTube MP3 Professional Downloader")
        # Set initial size but allow content to determine final size
        self.root.geometry("800x500")
        self.root.minsize(600, 400)
        # Allow window to resize based on content
        self.root.resizable(True, True)

    def _setup_tkinter(self):
        """Setup standard Tkinter appearance"""
        self.root.title("YouTube MP3 Professional Downloader")
        # Set initial size but allow content to determine final size
        self.root.geometry("800x500")
        self.root.minsize(600, 400)
        # Allow window to resize based on content
        self.root.resizable(True, True)

        # Configure style for ttk widgets
        style = ttk.Style()
        style.theme_use('clam')

    def _setup_ui(self):
        """Setup user interface"""
        # Main container
        if CUSTOM_TKINTER_AVAILABLE:
            main_frame = CTkFrame(self.root)
        else:
            main_frame = CTkFrame(self.root, bg='#2b2b2b')

        main_frame.pack(fill="x", padx=20, pady=20)

        # Banner section
        self._create_banner(main_frame)

        # Input section
        self._create_input_section(main_frame)

        # Settings section
        self._create_settings_section(main_frame)

        # Status section
        self._create_status_section(main_frame)

        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_banner(self, parent):
        """Create banner section"""
        if CUSTOM_TKINTER_AVAILABLE:
            banner_frame = CTkFrame(parent)
            banner_label = CTkLabel(
                banner_frame,
                text="▶️ YouTube MP3 Professional Downloader",
                font=("Arial", 24, "bold"),
            )
        else:
            banner_frame = CTkFrame(parent, bg='#2b2b2b')
            banner_label = CTkLabel(
                banner_frame,
                text="▶️ YouTube MP3 Professional Downloader",
                font=("Arial", 24, "bold"),
                bg='#2b2b2b',
                fg='white',
            )

        banner_frame.pack(fill="x", pady=(0, 20))
        banner_label.pack(pady=20)

    def _create_input_section(self, parent):
        """Create URL input section"""
        if CUSTOM_TKINTER_AVAILABLE:
            input_frame = CTkFrame(parent)
            url_label = CTkLabel(
                input_frame, text="YouTube URL:", font=("Arial", 14, "bold")
            )
            self.url_entry = CTkEntry(
                input_frame, placeholder_text="請輸入 YouTube 影片連結...", height=40
            )
            self.download_btn = CTkButton(
                input_frame,
                text="開始下載",
                command=self._start_download,
                height=40,
                font=("Arial", 14, "bold"),
            )
        else:
            input_frame = CTkFrame(parent, bg='#2b2b2b')
            url_label = CTkLabel(
                input_frame,
                text="YouTube URL:",
                font=("Arial", 14, "bold"),
                bg='#2b2b2b',
                fg='white',
            )
            self.url_entry = CTkEntry(input_frame, height=2, font=("Arial", 12))
            self.download_btn = CTkButton(
                input_frame,
                text="開始下載",
                command=self._start_download,
                height=2,
                font=("Arial", 14, "bold"),
            )

        input_frame.pack(fill="x", pady=(0, 20))
        url_label.pack(anchor="w", pady=(0, 10))
        self.url_entry.pack(fill="x", pady=(0, 10))
        self.download_btn.pack(fill="x")

    def _create_settings_section(self, parent):
        """Create settings section"""
        if CUSTOM_TKINTER_AVAILABLE:
            settings_frame = CTkFrame(parent)

            # Bitrate selection
            bitrate_frame = CTkFrame(settings_frame)
            bitrate_label = CTkLabel(
                bitrate_frame, text="MP3 位元率 (kbps):", font=("Arial", 12)
            )
            self.bitrate_var = tk.StringVar(value="192")
            self.bitrate_menu = CTkOptionMenu(
                bitrate_frame,
                values=["128", "192", "256", "320"],
                variable=self.bitrate_var,
                command=self._on_bitrate_change,
            )

            # Output directory selection
            output_frame = CTkFrame(settings_frame)
            output_label = CTkLabel(
                output_frame, text="輸出資料夾:", font=("Arial", 12)
            )
            self.output_path_var = tk.StringVar()
            self.output_path_label = CTkLabel(
                output_frame, textvariable=self.output_path_var, font=("Arial", 10)
            )
            self.browse_btn = CTkButton(
                output_frame,
                text="瀏覽...",
                command=self._browse_output_directory,
                width=100,
            )

        else:
            settings_frame = CTkFrame(parent, bg='#2b2b2b')

            # Bitrate selection
            bitrate_frame = CTkFrame(settings_frame, bg='#2b2b2b')
            bitrate_label = CTkLabel(
                bitrate_frame,
                text="MP3 位元率 (kbps):",
                font=("Arial", 12),
                bg='#2b2b2b',
                fg='white',
            )
            self.bitrate_var = tk.StringVar(value="192")
            self.bitrate_menu = CTkOptionMenu(
                bitrate_frame,
                textvariable=self.bitrate_var,
                values=["128", "192", "256", "320"],
                state="readonly",
            )
            self.bitrate_menu.bind("<<ComboboxSelected>>", self._on_bitrate_change)

            # Output directory selection
            output_frame = CTkFrame(settings_frame, bg='#2b2b2b')
            output_label = CTkLabel(
                output_frame,
                text="輸出資料夾:",
                font=("Arial", 12),
                bg='#2b2b2b',
                fg='white',
            )
            self.output_path_var = tk.StringVar()
            self.output_path_label = CTkLabel(
                output_frame,
                textvariable=self.output_path_var,
                font=("Arial", 10),
                bg='#2b2b2b',
                fg='white',
            )
            self.browse_btn = CTkButton(
                output_frame, text="瀏覽...", command=self._browse_output_directory
            )

        settings_frame.pack(fill="x", pady=(0, 20))

        # Pack bitrate section
        bitrate_frame.pack(fill="x", pady=(0, 15))
        bitrate_label.pack(anchor="w")
        self.bitrate_menu.pack(fill="x", pady=(5, 0))

        # Pack output directory section
        output_frame.pack(fill="x")
        output_label.pack(anchor="w")
        self.output_path_label.pack(anchor="w", pady=(5, 0))
        self.browse_btn.pack(anchor="w", pady=(5, 0))

    def _create_status_section(self, parent):
        """Create status section"""
        if CUSTOM_TKINTER_AVAILABLE:
            status_frame = CTkFrame(parent)

            # Status text - remove fixed height to fit content
            self.status_text = CTkTextbox(status_frame, height=60)

            # Progress bar
            self.progress_bar = CTkFrame(status_frame, height=25)
            self.progress_label = CTkLabel(
                self.progress_bar, text="", font=("Arial", 10)
            )

            author_label = CTkLabel(
                status_frame, text="Made with ❤️ by elvis.liao", font=("Arial", 10)
            )
        else:
            status_frame = CTkFrame(parent, bg='#2b2b2b')

            # Status text - remove fixed height to fit content
            self.status_text = CTkTextbox(
                status_frame, height=4, bg='#1a1a1a', fg='white'
            )

            # Progress bar
            self.progress_bar = CTkFrame(status_frame, bg='#2b2b2b', height=25)
            self.progress_label = CTkLabel(
                self.progress_bar,
                text="",
                font=("Arial", 10),
                bg='#2b2b2b',
                fg='white',
            )

            author_label = CTkLabel(
                status_frame,
                text="Made with ❤️ by elvis.liao",
                font=("Arial", 10),
                bg='#2b2b2b',
                fg='white',
            )

        status_frame.pack(fill="x", pady=(0, 10))
        self.status_text.pack(fill="x", pady=(0, 5))

        # Progress bar
        self.progress_bar.pack(fill="x", pady=(0, 5))
        self.progress_label.pack(pady=2)

        author_label.pack()

        # Initial status message
        self._update_status("準備就緒。請輸入 YouTube URL 開始下載。")
        self._update_progress("")

    def _adjust_window_size(self):
        """Adjust window size to fit content without scrolling"""
        # Update the window to calculate the required size
        self.root.update_idletasks()

        # Get the required size for the content
        req_width = self.root.winfo_reqwidth()
        req_height = self.root.winfo_reqheight()

        # Add some padding
        padding = 50
        new_width = max(600, req_width + padding)
        new_height = max(400, req_height + padding)

        # Set the new geometry
        self.root.geometry(f"{new_width}x{new_height}")

        # Center the window on screen
        self._center_window()

    def _center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()

        # Get window size
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Get screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position (ensure positive values)
        x = max(0, (screen_width - width) // 2)
        y = max(0, (screen_height - height) // 2)

        # Set position
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _load_settings(self):
        """Load settings from config"""
        # Load bitrate
        bitrate = self.config_manager.get("mp3_bitrate", 192)
        self.bitrate_var.set(str(bitrate))

        # Load output directory
        output_dir = self.config_manager.get("output_directory", "")
        self.output_path_var.set(output_dir)

    def _on_bitrate_change(self, *args):
        """Handle bitrate change"""
        try:
            bitrate = int(self.bitrate_var.get())
            self.config_manager.set("mp3_bitrate", bitrate)
            self._update_status(f"位元率已設定為 {bitrate} kbps")
        except ValueError:
            pass

    def _browse_output_directory(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(
            title="選擇輸出資料夾", initialdir=self.output_path_var.get()
        )

        if directory:
            self.output_path_var.set(directory)
            self.config_manager.set("output_directory", directory)
            self._update_status(f"輸出資料夾已設定為：{directory}")

    def _start_download(self):
        """Start download process"""
        url = self.url_entry.get().strip()

        if not url:
            self._update_status("請輸入 YouTube URL")
            return

        if not self.download_manager.is_ytdlp_available():
            self._update_status(
                f"錯誤：{self.download_manager.get_ytdlp_error_message()}"
            )
            return

        # Disable download button during download
        self.download_btn.configure(state="disabled", text="下載中...")

        # Start download
        success = self.download_manager.download(
            url,
            progress_callback=self._update_download_status,
            completion_callback=self._on_download_complete,
        )

        if not success:
            self.download_btn.configure(state="normal", text="開始下載")

    def _on_download_complete(self, success: bool, message: str):
        """Handle download completion"""
        self.download_btn.configure(state="normal", text="開始下載")

        if success:
            self._update_status(f"✅ {message}")
        else:
            self._update_status(f"❌ {message}")

    def _update_status(self, message: str):
        """Update status display"""
        if CUSTOM_TKINTER_AVAILABLE:
            self.status_text.delete("1.0", "end")
            self.status_text.insert("1.0", message)
        else:
            self.status_text.delete("1.0", "end")
            self.status_text.insert("1.0", message)

    def _update_progress(self, message: str):
        """Update progress display"""
        if CUSTOM_TKINTER_AVAILABLE:
            self.progress_label.configure(text=message)
        else:
            self.progress_label.configure(text=message)

    def _update_download_status(self, message: str):
        """Update download status with progress"""
        self._update_status(message)

        # Update progress bar based on message content
        if "準備" in message:
            self._update_progress("🔄 準備中...")
        elif "開始下載" in message:
            self._update_progress("⬇️ 下載中...")
        elif "完成" in message:
            self._update_progress("✅ 完成")
        elif "失敗" in message or "錯誤" in message:
            self._update_progress("❌ 失敗")
        else:
            self._update_progress("⏳ 處理中...")

    def _on_closing(self):
        """Handle window closing"""
        # Save window geometry
        geometry = self.root.geometry()
        self.config_manager.set("window_geometry", geometry)

        # Cancel any ongoing download
        if self.download_manager.is_downloading:
            self.download_manager.cancel_download()

        self.root.destroy()

    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    try:
        app = YouTubeDownloaderApp()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
