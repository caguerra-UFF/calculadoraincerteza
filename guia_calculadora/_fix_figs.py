# -*- coding: utf-8 -*-
"""Corrige a Figura 6 (fig06_vies_check.png): os rotulos 'media do check' e
'valor designado' ficavam encostados/sobre as linhas verticais, e o rotulo de
U do check nao tinha unidade."""

import io
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "make_figures.py")
raw = io.open(P, encoding="utf-8", newline="").read()
lines = raw.split("\n")


def put(n, novo):
    i = n - 1
    old = lines[i]
    term = old[len(old.rstrip("\r\n")):]
    lines[i] = novo + term


# rotulos do eixo (1-based 286-290)
assert 'a.text(ref, 0.22,' in lines[285], lines[285]
assert 'linespacing=1.3' in lines[286], lines[286]
assert 'a.text(mean, 0.22,' in lines[287], lines[287]
assert 'color=BLUE, linespacing=1.3' in lines[288], lines[288]
assert 'U do check = \\u00b10,0048' in lines[289], lines[289]

put(286, '    a.text(ref + 0.00035, 0.14, "valor designado\\n0,800 mg/L", ha="left",')
put(287, '           fontsize=8, color=TEAL, linespacing=1.3)')
put(288, '    a.text(mean - 0.00035, 0.14, "m\\u00e9dia do check\\n0,796 mg/L (n = 10)",')
put(289, '           ha="right", fontsize=8, color=BLUE, linespacing=1.3)')
put(290, lines[289].replace('\\u00b10,0048"', '\\u00b10,0048 mg/L"'))

io.open(P, "w", encoding="utf-8", newline="").write("\n".join(lines))
print("make_figures.py atualizado:")
for i in range(283, 293):
    print(i + 1, lines[i])
