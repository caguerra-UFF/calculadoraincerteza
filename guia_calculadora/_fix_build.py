# -*- coding: utf-8 -*-
"""Correcoes pontuais no build_guia.py (QA visual):

1. 'Cleitura' -> 'C<sub>leitura</sub>' nas linhas de prosa (a linha 528 e a
   citacao literal da mensagem da ferramenta e permanece intacta).
2. Largura das colunas da tabela 'Exemplo: as cinco fontes' (o cabecalho
   'Distribuicao' quebrava entre 'Distribui' e 'ao').
3. Legenda da Figura 13 (o recorte novo mostra so o bloco '5. Orcamento').
"""
import io
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_guia.py")
raw = io.open(P, encoding="utf-8", newline="").read()
lines = raw.split("\n")


def put(n, novo):
    """Substitui a linha n (1-based) preservando o terminador original."""
    i = n - 1
    old = lines[i]
    term = old[len(old.rstrip("\r\n")):]
    lines[i] = novo + term
    return old


# ------------------------------------------------------------------ 1) Cleitura
for n in (355, 405, 471, 474, 505, 521, 527, 912):
    old = lines[n - 1]
    assert old.count("Cleitura") == 1, (n, old)
    put(n, old.replace("Cleitura", "C<sub>leitura</sub>"))

# linha 528 = mensagem literal da ferramenta (nao mexer)
assert "Cleitura fora da faixa de trabalho" in lines[527], lines[527]

# ------------------------------------------------- 2) largura da tabela (linha 603)
antigo = "CW * 0.21, CW * 0.19, CW * 0.115, CW * 0.045, CW * 0.135, CW * 0.115"
assert antigo in lines[602], lines[602]
put(603, lines[602].replace(
    antigo, "CW * 0.205, CW * 0.19, CW * 0.115, CW * 0.040, CW * 0.15, CW * 0.115"))
# linha 604 fecha a lista com a largura de 'Tratamento'
assert "CW * 0.19], mono_cols=(2, 5), pad=4))" in lines[603], lines[603]
put(604, lines[603].replace("CW * 0.19],", "CW * 0.185],"))
assert "CW * 0.185], mono_cols=(2, 5), pad=4))" in lines[603], lines[603]
assert abs(sum([0.205, 0.19, 0.115, 0.040, 0.15, 0.115, 0.185]) - 1.0) < 1e-9

# --------------------------------------------- 3) legenda da Figura 13 (905-906)
assert '"Or\\u00e7amento como aparece na calculadora' in lines[904], lines[904]
put(905, '               "Bloco 5 da mem\\u00f3ria de c\\u00e1lculo: fonte, valor de "')
assert lines[905].strip().startswith('"o resultado final'), lines[905]
put(906, '               "entrada, distribui\\u00e7\\u00e3o/divisor, u(x), coeficiente de "')
lines.insert(906, '               "sensibilidade e participa\\u00e7\\u00e3o.", max_h=8.6 * cm)\r')
assert "max_h=8.6 * cm)" in lines[906], lines[906]
assert 'fig_n("memoria_resultado_p1.png"' in lines[907], lines[907]

io.open(P, "w", encoding="utf-8", newline="").write("\n".join(lines))
print("build_guia.py atualizado.")

# --------------------------------------------------------------- verificacao
txt = io.open(P, encoding="utf-8").read()
print("Linhas que ainda contem 'Cleitura':",
      [i + 1 for i, l in enumerate(txt.split("\n")) if "Cleitura" in l])
print("Ocorrencias de C<sub>leitura</sub>:", txt.count("C<sub>leitura</sub>"))
data = io.open(P, "rb").read()
print("CRLF:", data.count(b"\r\n"), "LF:", data.count(b"\n"))
