# -*- coding: utf-8 -*-
"""Confere o Sumario do guia: compara o numero IMPRESSO em cada entrada com a
pagina REAL onde o titulo aparece no corpo do documento.

Executar:  python guia_calculadora/_toccheck.py
"""
import os
import re
import sys
import unicodedata

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PDF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    ROOT, "Guia_Ilustrado_Calculadora_Incerteza_Nitrito.pdf")

DOTS = re.compile(r"(?:\s*\.){2,}")
STOP = {"pagina", "sumario", "indice", "guia", "nitrito"}


def norm(txt):
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(c for c in txt if not unicodedata.combining(c))
    txt = txt.replace("\u2014", "-").replace("\u2013", "-").replace("\u00b7", " ")
    txt = txt.replace("\u201c", '"').replace("\u201d", '"').replace("\u00ba", "o")
    return re.sub(r"\s+", " ", txt).strip().lower()


def limpa(txt):
    return re.sub(r"\s+", " ", txt).strip()


def linhas_por_y(page, tol=2.5):
    """Agrupa spans por linha fisica (y proximo) -> [(tamanho, texto), ...]."""
    itens = []
    for bloco in page.get_text("dict").get("blocks", []):
        for linha in bloco.get("lines", []):
            spans = [s for s in linha.get("spans", []) if s["text"].strip()]
            if spans:
                itens.append((linha["bbox"][1], spans))
    itens.sort(key=lambda it: it[0])
    grupos = []
    for y, spans in itens:
        if grupos and abs(y - grupos[-1][0]) <= tol:
            grupos[-1][1].extend(spans)
            grupos[-1][0] = (grupos[-1][0] + y) / 2.0
        else:
            grupos.append([y, list(spans)])
    saida = []
    for _, spans in grupos:
        spans.sort(key=lambda s: s["bbox"][0])
        texto = limpa("".join(s["text"] for s in spans))
        if texto:
            saida.append((spans[0]["size"], texto))
    return saida


def entradas_pagina(page):
    entradas = []
    for size, texto in linhas_por_y(page):
        m = re.match(r"^(?P<t>.+?)[\s.]+(?P<p>\d{1,3})$", texto)
        if not m:
            continue
        titulo = limpa(DOTS.sub(" ", m.group("t")))
        if not titulo:
            continue
        n_ = norm(titulo)
        if n_ in STOP or n_.startswith("pagina") or "iso/iec 17025 (7" in n_:
            continue
        nivel = 0 if size > 10.0 else 1
        entradas.append((nivel, titulo, int(m.group("p"))))
    return entradas


def entradas_sumario(doc):
    """Pagina inicial do Sumario + todas as entradas (pode passar de uma pagina)."""
    inicio = None
    for i in range(doc.page_count):
        if norm("Sumario") in norm(doc[i].get_text("text"))[:400]:
            inicio = i
            break
    if inicio is None:
        return None, []
    entradas = []
    for i in range(inicio, doc.page_count):
        locais = entradas_pagina(doc[i])
        if i > inicio and len(locais) < 2:
            break
        entradas.extend(locais)
    return inicio, entradas


def titulos_corpo(doc, inicio):
    """Titulos reais do corpo: H1 (14,5 pt) e H2 (11,8 pt) em DJV-Bold."""
    saida = []
    for i in range(inicio, doc.page_count):
        for bloco in doc[i].get_text("dict")["blocks"]:
            for linha in bloco.get("lines", []):
                spans = [s for s in linha.get("spans", []) if s["text"].strip()]
                if not spans:
                    continue
                s0 = spans[0]
                if "Bold" not in s0["font"]:
                    continue
                if 14.2 <= s0["size"] <= 14.8:
                    nivel = 0
                elif 11.5 <= s0["size"] <= 12.1:
                    nivel = 1
                else:
                    continue
                txt = limpa("".join(s["text"] for s in spans))
                if txt:
                    saida.append((i + 1, nivel, txt))
    return saida


def main():
    doc = fitz.open(PDF)
    n = doc.page_count
    print(f"PDF: {os.path.basename(PDF)}  ({n} paginas)")

    idx, entradas = entradas_sumario(doc)
    if idx is None:
        print("!! Nao localizei a pagina do Sumario.")
        return
    print(f"Sumario a partir da pagina {idx + 1}, {len(entradas)} entradas "
          f"({sum(1 for e in entradas if e[0] == 0)} capitulos)")

    corpo = titulos_corpo(doc, idx + 1)
    print(f"Titulos localizados no corpo: {len(corpo)}")
    if not corpo:
        print("!! Nenhum titulo de corpo localizado.")
        return

    cursor = idx + 1
    erros = 0
    print("\n%-5s %-9s %-6s  %s" % ("st", "impresso", "real", "entrada"))
    print("-" * 86)
    for nivel, titulo, impressa in entradas:
        alvo = norm(titulo)
        real = None
        for pag, niv, txt in corpo:
            if niv != nivel or pag < cursor:
                continue
            h = norm(txt)
            if h == alvo or (len(h) > 8 and alvo.startswith(h)):
                real = pag
                break
        if real is None:  # fallback: procura sem respeitar o cursor
            for pag, niv, txt in corpo:
                if niv != nivel:
                    continue
                h = norm(txt)
                if h == alvo or (len(h) > 8 and alvo.startswith(h)):
                    real = pag
                    break
        if real is not None:
            cursor = real
        ok = real == impressa
        if not ok:
            erros += 1
        print("%-5s %-9s %-6s  %s" % ("ok" if ok else "DIVERG",
                                      impressa, real if real else "?",
                                      ("  " * nivel) + titulo))
    print("-" * 86)
    print(f"{len(entradas)} entradas conferidas, {erros} divergencia(s).")
    doc.close()


if __name__ == "__main__":
    main()
