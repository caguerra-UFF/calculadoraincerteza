# -*- coding: utf-8 -*-
"""Mede a largura real dos cabecalhos das tabelas x largura disponivel na coluna."""
import os
import matplotlib
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

FDIR = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
pdfmetrics.registerFont(TTFont("DJV", os.path.join(FDIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DJV-Bold", os.path.join(FDIR, "DejaVuSans-Bold.ttf")))

CW = (21.0 - 3.4) * cm  # largura util da tabela
PAD = 12.0              # 6pt de padding em cada lado


def check(titulo, heads, frac, size=8.6):
    print("=" * 74)
    print(titulo)
    print("-" * 74)
    for h, fr in zip(heads, frac):
        avail = fr * CW - PAD
        w = pdfmetrics.stringWidth(h, "DJV-Bold", size)
        flag = "OK      " if w <= avail else "OVERFLOW"
        print("%-34s avail=%6.1f  need=%6.1f  %s" % (h, avail, w, flag))


check(
    "Tabela: orcamento de incerteza (p10)",
    ["Fonte", "Certificado", "U / \u00b1a / r", "k", "Distribui\u00e7\u00e3o", "u(x)", "Tratamento"],
    [0.21, 0.19, 0.115, 0.045, 0.135, 0.115, 0.19],
)

check(
    "Tabela: alternativas propostas para 'Distribuicao'",
    ["Fonte", "Certificado", "U / \u00b1a / r", "k", "Distribui\u00e7\u00e3o", "u(x)", "Tratamento"],
    [0.205, 0.185, 0.115, 0.045, 0.145, 0.115, 0.19],
)

# ---- largura dos DADOS (fonte regular) da tabela das cinco fontes ----
print("=" * 74)
print("Dados (regular 8.6) da tabela das cinco fontes")
print("-" * 74)
dados = [
    ("Fonte", "\u00b1a / \u2026", ["Padr\u00e3o de nitrito", "Balan\u00e7a anal\u00edtica",
                                   "Bal\u00e3o volum\u00e9trico", "Pipetador 10 mL",
                                   "Espectrofot\u00f4metro", "ESP-1"]),
    ("Certificado", "", ["CRM-NIT-2026-005", "BAL-2026-088", "VOL-100-2026-021",
                         "PIP-010-2026-034", "ESP-2026-011"]),
    ("U / \u00b1a / r", "", ["1,0 mg/L", "0,0002 g", "0,2 mL", "0,05 mL", "0,002 abs"]),
    ("Tratamento", "", ["J\u00e1 incorporada", "N\u00e3o aplic\u00e1vel"]),
]
for nome, _, cells in dados:
    print("%-14s " % nome + "; ".join(
        "%s=%.1f" % (c, pdfmetrics.stringWidth(c, "DJV", 8.6)) for c in cells))

