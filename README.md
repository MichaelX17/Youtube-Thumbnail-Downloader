# Youtube Thumbnail Downloader

| ![image](https://github.com/user-attachments/assets/4a9a9f78-dc1e-4260-933d-b416130b5385) | ![image](https://github.com/user-attachments/assets/9e09fa80-86d8-4893-987e-3f12eb5149f7) |
|:--:|:--:|




*A lightweight utility to download YT Thumbnails on Windows systems (x86/x64).*

---

## 📥 Prerequisites

- **Windows 7/8/10/11 (Not tested in WinXP)** (32-bit or 64-bit)
- **Git Bash** (recommended for compilation)
- Files from `./assets` folder:
  - `python-3.4.0.msi`
  - `pywin32-221.win32-py3.4.exe`
  - `pefile-2017.11.5.tar.gz`
  - `PyInstaller-3.2.tar.gz`
  - `vcredist_x86.exe ` ( Visual Studio 2010 (VC++ 10.0) SP1 )

---

## 🛠 Full Compilation Guide

### 1. Install Python 3.4

```bash
# Install File: "assets\python-3.4.0.msi"
./assets/python-3.4.0.msi
```

### 2. Install pywin32

```bash
# Install File: "./assets/vcredist_x86.exe"
./assets/vcredist_x86.exe
```

### 3. Install Visual Studio 2010 (VC++ 10.0) SP1

```bash
# Install File: "./assets/pywin32-221.win32-py3.4.exe"
./assets/pywin32-221.win32-py3.4.exe
```

### 4. Install pip for Python 3.4

```bash
curl -O https://bootstrap.pypa.io/pip/3.4/get-pip.py
/c/Python34/python.exe get-pip.py --trusted-host pypi.python.org
```

### 5. Install required packages

```bash
/c/Python34/Scripts/pip.exe install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org future==0.18.2
/c/Python34/Scripts/pip.exe install ./assets/pefile-2017.11.5.tar.gz
/c/Python34/Scripts/pip.exe install ./assets/PyInstaller-3.2.tar.gz
```

### 6. Install Pillow

```bash
/c/Python34/python.exe -m pip install pillow
```

### 7. Compile Executable

```bash
/c/Python34/python.exe -m PyInstaller youtube_thumbnails.spec
```

### 8. Compress with UPX (OPTIONAL)

```bash
# Extract UPX from assets to C:\upx first
/c/upx/upx.exe --best --lzma --ultra-brute --force ./dist/YT_Thumbnail_Downloader.exe
```

---

## 🚀 Usage Instructions

1. Navigate to `dist` folder  
2. Open `YT_Thumbnail_Downloader.exe`
3. Paste / Type your Youtube URL and start searching  
4. Select the images you want to download
5. Click **Download Selected** to download your images 
   *Success message will appear when done.*
6. Looks for your images in the created Thumb folder
7. **IT'S DONE**  

---

## ⚠️ Troubleshooting

### Common UPX Error

**Error**:  
`GUARD_CF enabled PE files are not supported`

**Solution**:

```bash
/c/upx/upx.exe --best --ultra-brute --force ./dist/YT_Thumbnail_Downloader.exe
```

### Missing Registry Entries

- Verify Python 3.4 is installed at `C:\Python34`
- Check error logs in the application directory

---

## 📂 Repository Structure

```
PES-6-Registry-Installer/
├── assets/                   # Local dependencies
│   ├── python-3.4.0.msi
│   ├── pywin32-221.win32-py3.4.exe
│   ├── pefile-2017.11.5.tar.gz
│   ├── PyInstaller-3.2.tar.gz
│   ├── upx-*.zip
│   └── vcredist_x86.exe
├── yt_thumb.ico                # Application icon
├── youtube_thumbnails.py       # Main script
├── youtube_thumbnails.spec     # PyInstaller config
└── README.md                   # This file
```

---

## 👥 Credits & Legal

- Developer: [MichaelX17](https://github.com/MichaelX17)  
- Icon Designer: MichaelX17  
- Tools: PyInstaller, UPX, pefile, Pillow 

*Educational/preservation project. Not affiliated with Youtube.*

**⚠️ Note**: All assets in `/assets` are provided for archival purposes only. Use at your own risk.
