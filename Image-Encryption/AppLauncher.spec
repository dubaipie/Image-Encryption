# -*- mode: python -*-

block_cipher = None


a = Analysis(['src/API/AppLauncher.py'],
             pathex=['/home/pierre/PycharmProjects/Image-Encryption/Image-Encryption'],
             binaries=[],
             datas=[('ressources/pictures', 'ressources/pictures')],
             hiddenimports=['tkinter.filedialog', 'tkinter.messagebox', 'numbers'],
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
          exclude_binaries=True,
          name='ImageEncryption',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='ImageEncryption')
