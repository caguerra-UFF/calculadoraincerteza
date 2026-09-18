# -*- coding: utf-8 -*-
"""Depuracao da pagina de Sumario: links internos e linhas extraidas."""
import os

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PDF = os.path.join(ROOT, "Guia_Ilustrado_Calculadora_Incerteza_Nitrito.pdf")

doc = fitz.open(PDF)
for i in range(min(4, doc.page_count)):
    page = doc[i]
    links = page.get_links()
    print(f"--- p{i + 1}: {len(links)} links")
    for l in links[:4]:
        print("    ", {k: l[k] for k in l if k in ("kind", "page", "from", "uri", "to")})
    linhas = [t for t in page.get_text("text").split("\n") if t.strip()]
    for t in linhas[:12]:
        print(f"    TXT {t!r}")
doc.close()
