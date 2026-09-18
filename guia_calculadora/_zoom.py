# -*- coding: utf-8 -*-
"""Recorta e amplia regioes das imagens de revisao para inspecao fina."""
import os
from PIL import Image

REV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "review")

# (pagina, esquerda, topo, direita, base) em fracao da pagina
REGIOES = [
    (10, 0.03, 0.34, 1.00, 0.58, "z10_tabela"),
    (12, 0.04, 0.33, 1.00, 0.72, "z12_fig"),
    (16, 0.04, 0.50, 1.00, 0.70, "z16_tabela"),
    (17, 0.04, 0.20, 1.00, 0.60, "z17_fig"),
    (9, 0.04, 0.50, 1.00, 0.72, "z09_fig"),
]

for pag, l, t, r, b, nome in REGIOES:
    im = Image.open(os.path.join(REV, "p%02d.png" % pag))
    W, H = im.size
    box = (int(l * W), int(t * H), int(r * W), int(b * H))
    crop = im.crop(box)
    crop = crop.resize((crop.width * 2, crop.height * 2), Image.LANCZOS)
    saida = os.path.join(REV, "_%s.png" % nome)
    crop.save(saida)
    print(saida, crop.size)
