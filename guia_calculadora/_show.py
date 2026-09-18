"""Mostra linhas longas de um arquivo, quebrando antes de cada tag (leitura por seção).

uso: python _show.py <arquivo>                       -> lista o indice das linhas
     python _show.py <arquivo> <inicio> [fim]        -> imprime as linhas quebradas
"""
import sys
from pathlib import Path

base = Path(r"F:\Transcricoes_Consolidadas")
alvo = Path(sys.argv[1])
if not alvo.is_absolute():
    alvo = base / alvo
linhas = alvo.read_text(encoding="utf-8").split("\n")

if len(sys.argv) < 3:
    for i, t in enumerate(linhas, 1):
        print(f"{i:4d} {len(t):6d}  {t[:70]}")
    sys.exit()

ini = int(sys.argv[2])
fim = int(sys.argv[3]) if len(sys.argv) > 3 else ini
for i in range(ini, fim + 1):
    print(f"===== linha {i} ({len(linhas[i-1])} chars) =====")
    print(linhas[i - 1].replace("><", ">\n<"))
