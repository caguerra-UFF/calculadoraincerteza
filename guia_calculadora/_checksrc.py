"""Conferencia rapida: marcas no fonte do build e no PDF final."""
import re
import sys
from pathlib import Path

import fitz

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(r"F:\Transcricoes_Consolidadas")
SRC = BASE / "guia_calculadora" / "build_guia.py"
PDF = Path(sys.argv[1]) if len(sys.argv) > 1 else (
    BASE / "Guia_Ilustrado_Calculadora_Incerteza_Nitrito.pdf")

src = SRC.read_text(encoding="utf-8")
print("=== build_guia.py ===")
for alvo in [
    "Cleitura",
    "C<sub>leitura</sub>",
    "colWidths",
    "0.205",
    "0.19",
    "0.115",
    "0.040",
    "0.15",
    "0.185",
    "memoria_orcamento_p5.png",
    "memoria_resultado_p1.png",
    "fig_n",
    "Figura 13",
    "Figura 6",
    "Fonte do check",
    r"V\u00ednculo vivo",
    r"Adicionar r\u00e9plica",
    "6 a 10",
    "ANA_05JAN26 NO2- CE",
    "Gerar a coluna",
    "Corrida autom",
]:
    print(f"{src.count(alvo):4d}x  {alvo!r}")
print(f"{src.count(chr(0x301)):4d}x  U+0301 (acento combinante)\n")

doc = fitz.open(PDF)
txt = "\n".join(doc[i].get_text("text") for i in range(doc.page_count))
print("=== PDF final ===")
for alvo in ["Cleitura", "C leitura", "sub>", "distribu\u00e7\u00e3o",
             "distribui\u00e7\u00e3o", "vi\u00e9s", "0,850", "0,052",
             "Fonte do check", "v\u00ednculo com a aba 02",
             "Adicionar r\u00e9plica da \u00faltima", "6 a 10",
             "Fortifica\u00e7\u00e3o: o que \u00e9 e quando ela entra",
             "VERDADE PR\u00c1TICA",
             "N\u00e3o faz fortifica\u00e7\u00e3o no seu laborat\u00f3rio?",
             "0,044 mg/L", "0,02189 mg/L", "Incerteza A/B",
             "Aba 04 \u2014 Veracidade", "opcional",
             "CTRL-NO\u2082\u207b 0,85 mg/L", "CHECK-NO\u2082\u207b 0,80 mg/L",
             "FORT-NO\u2082\u207b 0,85 mg/L", "ANA_05JAN26 NO2- CE"]:
    print(f"{txt.count(alvo):4d}x  {alvo!r}")
print(f"{txt.count(chr(0x301)):4d}x  U+0301 (acento combinante)")

print("\n=== 'Figura N' citadas no PDF ===")
nums = sorted({int(n) for n in re.findall(r"Figura\s*(\d+)", txt)})
print(nums)
