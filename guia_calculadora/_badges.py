# -*- coding: utf-8 -*-
"""Lista os rotulos (badge) das secoes do HTML. Uso: python guia_calculadora/_badges.py <arquivo>"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

src = open(sys.argv[1], encoding="utf-8").read()
for m in re.finditer(r'<section id="([^"]+)">\s*<span class="badge">([^<]+)</span>\s*<h2>(.*?)</h2>', src, re.S):
    title = re.sub(r"<[^>]+>", "", m.group(3)).strip()
    print("%-14s %-26s %s" % (m.group(1), m.group(2), title.replace("\n", " ")))
