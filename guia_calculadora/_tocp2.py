"""Mostra como a pagina do Sumario e agrupada por linha (y) e o que e descartado."""
import sys

import fitz

sys.path.insert(0, r"F:\Transcricoes_Consolidadas\guia_calculadora")
import _toccheck as tc  # noqa: E402

PDF = r"F:\Transcricoes_Consolidadas\Guia_Ilustrado_Calculadora_Incerteza_Nitrito.pdf"

doc = fitz.open(PDF)
idx, entradas = tc.entradas_sumario(doc)
print(f"Sumario: paginas {(idx or 0) + 1}..  entradas detectadas: {len(entradas)}\n")
for size, texto in tc.linhas_por_y(doc[idx]):
    print(f"{size:5.1f}  {texto[:96]!r}")
