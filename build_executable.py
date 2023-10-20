import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--name brachyapp'
    '--onefile',
    '--debug=all',
    '--console'
])

"""
pyinstaller --noconfirm --onedir --console --icon "C:/Users/nsmel/Downloads/sewing-needle.ico" --name "prodd" --hidden-import "pydicom.encoders.gdcm" --hidden-import "pydicom.encoders.pylibjpeg"  "C:/Users/nsmel/Documents/Programming/nsmela/Modern-GUI-PyQt5/main.py"
"""