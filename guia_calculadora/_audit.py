# -*- coding: utf-8 -*-
"""Auditoria de layout: para cada pagina do PDF, lista cabecalhos, legendas de figura
e a extensao vertical ocupada (para detectar paginas quase vazias)."""
import os
import sys
import fitz

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PDF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    ROOT, "Guia_Ilustrado_Calculadora_Incerteza_Nitrito.pdf")

PT_CM = 28.3465
HEAD_LIMIT = 1.6 * PT_CM      # abaixo do cabecalho do template
FOOT_LIMIT = 27.6 * PT_CM     # acima do rodape do template

doc = fitz.open(PDF)
print("paginas:", doc.page_count)
for i, page in enumerate(doc, start=1):
    d = page.get_text("dict")
    heads, caps, top, bottom = [], [], None, None
    for b in d["blocks"]:
        y0b, y1b = b["bbox"][1], b["bbox"][3]
        if 0.5 * PT_CM < y0b < FOOT_LIMIT and (b["type"] == 1 or b["type"] == 0):
            top = y0b if top is None else min(top, y0b)
            if b["type"] == 1:
                bottom = y1b if bottom is None else max(bottom, y1b)
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            txt = "".join(s["text"] for s in l["spans"]).strip()
            size = max(s["size"] for s in l["spans"])
            y0, y1 = l["bbox"][1], l["bbox"][3]
            if not txt or y0 < HEAD_LIMIT or y1 > FOOT_LIMIT:
                continue
            top = y0 if top is None else min(top, y0)
            bottom = y1 if bottom is None else max(bottom, y1)
            if size >= 13:
                heads.append(f"{size:.1f}pt '{txt[:46]}'")
            if txt.startswith("Figura "):
                caps.append(f"'{txt[:34]}'")
    if top is None:
        print(f"--- p{i:02d}  (sem conteudo de texto/imagem no miolo)")
        continue
    print(f"--- p{i:02d}  bloco {top/PT_CM:5.1f} -> {bottom/PT_CM:5.1f} cm  "
          f"(livre embaixo: {(28.05 - bottom/PT_CM):4.1f} cm)")
    for b in d["blocks"]:
        if b["type"] == 1:
            print(f"    IMG y {b['bbox'][1]/PT_CM:5.2f} -> {b['bbox'][3]/PT_CM:5.2f} cm "
                  f"(altura {(b['bbox'][3]-b['bbox'][1])/PT_CM:4.2f} cm)")
    for x in heads:
        print("    H:", x)
    for x in caps:
        print("    F:", x)

print("\n=== detalhe da capa (p01) ===")
for b in doc[0].get_text("dict")["blocks"]:
    if b["type"] != 0:
        continue
    for l in b["lines"]:
        txt = "".join(s["text"] for s in l["spans"]).strip()
        if txt:
            print(f"  y0={l['bbox'][1]/PT_CM:5.2f} y1={l['bbox'][3]/PT_CM:5.2f} "
                  f"sz={max(s['size'] for s in l['spans']):4.1f}  {txt[:60]}")
