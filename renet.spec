# -*- mode: python -*-

block_cipher = None


a = Analysis(['renet\\renet.py'],
             pathex=['C:\\Users\\sunzhang\\Desktop\\Tools\\renet'],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='renet',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='C:\\Users\\sunzhang\\Desktop\\Tools\\renet\\raw\\icon.ico')
