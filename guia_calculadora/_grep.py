"""Busca por expressao regular (case-insensitive) e mostra contexto curto.

uso: python _grep.py <arquivo> <regex> [largura_contexto]
"""
import re
import sys
from pathlib import Path

base = Path(r"F:\Transcricoes_Consolidadas")
alvo = Path(sys.argv[1])
if not alvo.is_absolute():
    alvo = base / alvo
padrao = re.compile(sys.argv[2], re.I)
largura = int(sys.argv[3]) if len(sys.argv) > 3 else 70

texto = alvo.read_text(encoding="utf-8")
n = 0
for i, linha in enumerate(texto.split("\n"), 1):
    for m in padrao.finditer(linha):
        a = max(0, m.start() - largura)
        b = min(len(linha), m.end() + largura)
        print(f"{i:4d}: ...{linha[a:b]}...")
        n += 1
print(f"--- {n} ocorrencia(s) ---")
