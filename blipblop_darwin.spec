# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['blipblop_main.py'],
             pathex=['.'],
             binaries=[],
             datas=[('docs/index.md', "docs"), 
                    ('docs/visual_task.md', "docs"), 
                    ('docs/auditory_task.md', "docs"),
                    ('docs/license.md', "docs"),
                    ('docs/tasks.md', "docs"),
                    ('docs/images/blipblop_main.png', "docs/images"),
                    ('docs/images/blipblop_logo.png', "docs/images"),
                    ('sounds/bell.wav', "sounds"),
                    ('sounds/complete.wav', "sounds"),
                    ('sounds/message.wav', "sounds"),
                    ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='BlipBlop',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='icons/blipblop_logo.icns'
          )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='BlipBlop')
