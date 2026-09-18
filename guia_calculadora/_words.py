# -*- coding: utf-8 -*-
"""Lista as palavras acentuadas do PDF final para revisao ortografica rapida.

Executar:  python guia_calculadora/_words.py
"""
import os
import re
import unicodedata
from collections import Counter

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PDF = os.path.join(ROOT, "Guia_Ilustrado_Calculadora_Incerteza_Nitrito.pdf")

ACENTOS = "áàâãäéèêëíìîïóòôõöúùûüçÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇ"

doc = fitz.open(PDF)
texto = "\n".join(doc[i].get_text("text") for i in range(doc.page_count))
doc.close()

palavras = re.findall(r"[A-Za-zÀ-ÿ]+", texto)
c = Counter(p for p in palavras if any(a in p for a in ACENTOS))
print(f"{len(c)} palavras acentuadas distintas:")
for p, n in sorted(c.items(), key=lambda kv: (kv[0].lower(), kv[0])):
    print(f"{n:3d}  {p}")
