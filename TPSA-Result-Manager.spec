# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules("classes")

a = Analysis(
    ["app.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("tpsa_logo.png", "."),
        ("tpsa.db", "."),
        ("Report_Card_Template.xlsx", "."),
        ("template", "template"),
        ("templates", "templates"),
        ("static", "static"),
        ("classes", "classes"),
        ("subjectsfolder", "subjectsfolder"),
    ],
    hiddenimports=hiddenimports,
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="TPSA Result Manager",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon="tpsa_logo.ico" if os.path.exists("tpsa_logo.ico") else None,
)
