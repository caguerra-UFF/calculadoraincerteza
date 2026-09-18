import sys, pathlib
"""Localiza linhas por substring e imprime em repr (evita problemas de aspas no shell).
Uso: python _find.py <arquivo> <substring>"""
p = pathlib.Path(sys.argv[1])
needle = sys.argv[2]
text = p.read_text(encoding="utf-8")
for i, line in enumerate(text.splitlines(), 1):
    if needle in line:
        print(i, repr(line))
