from setuptools import setup

APP = ['run.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt5', 'ephem', 'requests', 'pyserial', 'yaml', 'rich'],
    'includes': ['PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'PyQt5.QtWebEngineWidgets'],
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleName': '卫星跟踪器',
        'CFBundleDisplayName': '卫星跟踪器',
        'CFBundleIdentifier': 'com.satellitetracker.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
