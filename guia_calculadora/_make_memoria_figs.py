# -*- coding: utf-8 -*-
"""Gera os recortes da memoria de calculo usados como Figura 13 e Figura 14.

Antes: as figuras eram as paginas A4 inteiras (909x1287) renderizadas com
largura util -> texto ilegivel (~6 cm de largura).
Agora: recorta apenas o bloco util de cada pagina e re-renderiza em 220 dpi,
para a figura ocupar a largura total da coluna do guia com texto legivel.
"""
import os
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "tmp", "memoria_exemplo.pdf")
FIG = os.path.join(HERE, "figures")
REV = os.path.join(HERE, "review")
DPI = 220

doc = fitz.open(SRC)


def marca(page, texto):
    hits = page.search_for(texto)
    assert hits, "nao encontrei %r" % texto
    return hits[0]


def caixa(page, y_min, y_max):
    """Uniao dos textos e dos desenhos (linhas de tabela, bordas) na faixa."""
    xs0, xs1, ys0, ys1 = [], [], [], []
    for b in page.get_text("blocks"):
        if len(b) > 6 and b[6] != 0:
            continue
        if not str(b[4]).strip():
            continue
        if b[1] >= y_min - 0.5 and b[3] <= y_max + 0.5:
            xs0.append(b[0]); xs1.append(b[2]); ys0.append(b[1]); ys1.append(b[3])
    for d in page.get_drawings():
        r = d["rect"]
        if r.y0 >= y_min - 0.5 and r.y1 <= y_max + 0.5:
            xs0.append(r.x0); xs1.append(r.x1); ys0.append(r.y0); ys1.append(r.y1)
    assert xs0, "faixa vazia"
    return fitz.Rect(min(xs0), min(ys0), max(xs1), max(ys1))


def salvar(page, clip, nome, pad=6.0):
    clip = fitz.Rect(clip.x0 - pad, clip.y0 - pad, clip.x1 + pad, clip.y1 + pad)
    pix = page.get_pixmap(clip=clip, dpi=DPI)
    pix.save(os.path.join(FIG, nome))
    pix.save(os.path.join(REV, "_" + nome))
    print("%-34s clip=%s  %.0fx%.0f px  aspecto=%.3f  -> largura 17,6 cm = %.2f cm"
          % (nome, [round(v, 1) for v in clip], pix.width, pix.height,
             pix.height / pix.width, 17.6 * pix.height / pix.width))


# ---------------------------------------------------------------- Figura 13
p5 = doc[4]
h5 = marca(p5, "Or\u00e7amento")
h6 = marca(p5, "F\u00f3rmulas")
salvar(p5, caixa(p5, h5.y0 - 14, h6.y0 - 12), "memoria_orcamento_p5.png")

# ---------------------------------------------------------------- Figura 14
p1 = doc[0]
aviso = marca(p1, "FICT\u00cdCIO")
decisao = marca(p1, "conformidade")
salvar(p1, caixa(p1, aviso.y0 - 14, decisao.y1 + 12), "memoria_resultado_p1.png")

doc.close()
