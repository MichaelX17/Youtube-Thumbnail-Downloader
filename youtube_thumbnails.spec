# -*- mode: python -*-
import os

block_cipher = None

script_dir = os.getcwd()

a = Analysis(['youtube_thumbnails.py'],
             pathex=[script_dir],
             binaries=None,
             datas=[('yt_thumb.ico', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='YT_Thumbnail_Downloader',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='yt_thumb.ico')