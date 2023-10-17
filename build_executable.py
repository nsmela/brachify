import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--name brachyapp'
    '--onefile',
    '--debug=all',
    '--console'
])