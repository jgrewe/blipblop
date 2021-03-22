# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['blipblop_main.py'],
             pathex=['/Users/jan/projects/programming/blipblop'],
             binaries=[],
             datas=[('docs/index.md', "docs"), 
                    ('docs/visual_task.md', "docs"), 
                    ('docs/auditory_task.md', "docs"),
                    ('docs/license.md', "docs"),
                    ('docs/tasks.md', "docs"),
                    ('docs/results.md', "docs"),
                    ('docs/images/blipblop_main.png', "docs/images"),
                    ('docs/images/blipblop_logo.png', "docs/images"),
                    ('docs/images/auditory_settings.png', "docs/images"),
                    ('docs/images/visual_settings.png', "docs/images"),
                    ('docs/images/auditory_task_screen.png', "docs/images"),
                    ('docs/images/visual_task_screen.png', "docs/images"),
                    ('docs/images/results_table.png', "docs/images"),
                    ('sounds/bell.wav', "sounds"),
                    ('sounds/complete.wav', "sounds"),
                    ('sounds/message.wav', "sounds"),
                    ('icons/blipblop_logo.icns', "."),
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='BlipBlop',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='icons/blipblop_logo.icns')

app = BUNDLE(exe,
            name='BlipBlop.app',
            icon='icons/blipblop_logo.icns',
            bundle_identifier='de.uni-tuebingen.neuroetho.blipblop',
            version="0.1.0",
            info_plist={
                'NSPrincipalClass': 'NSApplication',
                'NSAppleScriptEnabled': False,
            },
)
