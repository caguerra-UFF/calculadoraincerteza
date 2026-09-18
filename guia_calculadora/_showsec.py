# -*- coding: utf-8 -*-
"""Mostra uma secao do HTML por id. Uso: python guia_calculadora/_showsec.py <arquivo> <id>"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

path, sid = sys.argv[1], sys.argv[2]
src = open(path, encoding="utf-8").read()
m = re.search(r'<section id="%s".*?</section>' % re.escape(sid), src, re.S)
if not m:
    print("secao nao encontrada:", sid)
    sys.exit(1)
txt = m.group(0)
txt = re.sub(r"><", ">\n<", txt)
print(txt)
