# -*- mode: python ; coding: utf-8 -*-

import os
import sys

# 动态获取项目根目录
project_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

block_cipher = None

a = Analysis(['Archer-Legends.py'],
             pathex=[project_dir],
             binaries=[],
             datas=[
                 ('pictures/background.png', 'pictures'),
                 ('fonts/font.ttf', 'fonts'),
                 ('pictures/arrow.png', 'pictures'),
		 ('pictures/home.png', 'pictures'),
		 ('pictures/player.png', 'pictures'),
		 ('pictures/bat/death.png', 'pictures'),
		 ('pictures/bat/origin.png', 'pictures'),
		 ('pictures/bat/move.png', 'pictures')
			],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Archer-Legends',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='C:\\Users\\dgsjk\\PyCharmMiscProject\\shoot\\pictures\\icon.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Archer-Legends')