# PyInstaller configuration file for YouTube MP3 Professional Downloader

# Basic settings
name = 'YouTube_MP3_Downloader'
main_script = 'main.py'

# Output settings
onefile = True
windowed = True
clean = True

# Icon settings (uncomment and set path if you have an icon)
# icon = 'icon.ico'  # Windows
# icon = 'icon.icns'  # macOS

# Hidden imports (if needed)
hidden_imports = [
    'customtkinter',
    'yt_dlp',
    'json',
    'subprocess',
    'threading',
    'platform',
    'pathlib',
    'shutil'
]

# Exclude unnecessary modules to reduce file size
excludes = [
    'matplotlib',
    'numpy',
    'scipy',
    'pandas',
    'PIL',
    'cv2',
    'tensorflow',
    'torch',
    'sklearn'
]

# Additional files to include
datas = []

# Binary files to include
binaries = []

# Analysis settings
optimize = 2
strip = True
