# -*- coding: utf-8 -*-
"""Extrai o texto de paginas especificas: python _dump.py 18 19"""
import os
import sys
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(os.path.dirname(HERE),
                   "Guia_Ilustrado_Calculadora_Incerteza_Nitrito.pdf")
doc = fitz.open(PDF)
for arg in sys.argv[1:]:
    i = int(arg) - 1
    print("=" * 24, "pagina", arg, "=" * 24)
    print(doc[i].get_text().strip())
