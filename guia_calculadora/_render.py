# -*- coding: utf-8 -*-
"""Renderiza cada pagina do guia em PNG para a revisao visual.
Executar:  python guia_calculadora/_render.py"""
import os
import glob
import sys
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PDF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    ROOT, "Guia_Ilustrado_Calculadora_Incerteza_Nitrito.pdf")
OUT = os.path.join(HERE, "review")
os.makedirs(OUT, exist_ok=True)
for old in glob.glob(os.path.join(OUT, "p*.png")):
    os.remove(old)

doc = fitz.open(PDF)
n = doc.page_count
for i in range(n):
    pix = doc[i].get_pixmap(dpi=110)
    pix.save(os.path.join(OUT, f"p{i + 1:02d}.png"))
doc.close()
print(f"{n} paginas renderizadas em {OUT}")
