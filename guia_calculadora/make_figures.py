# -*- coding: utf-8 -*-
"""Gera as figuras (recursos visuais) do Guia Ilustrado da Calculadora de Incerteza - Nitrito.
Paleta alinhada com calculadora_incerteza_nitrito_v2.html.
Executar:  python guia_calculadora/make_figures.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figures")
os.makedirs(OUT, exist_ok=True)

NAVY = "#102e46"
BLUE = "#0f4c81"
TEAL = "#087e83"
LIGHT = "#eaf2f7"
LINE = "#b9c9d6"
TEXT = "#203647"
MUTED = "#52697a"
WARN = "#81500a"
WARNB = "#fdf3e0"
DANGER = "#a32832"
DANGERB = "#fbeaec"
OK = "#1f7a4d"
OKB = "#e8f5ee"
AMBER = "#c98a12"
WHITE = "#ffffff"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "text.color": TEXT,
    "axes.edgecolor": LINE,
    "savefig.facecolor": "white",
    "figure.facecolor": "white",
})


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax


def rbox(ax, x, y, w, h, fc=WHITE, ec=LINE, lw=1.2, radius=1.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=%s" % radius,
                                linewidth=lw, edgecolor=ec, facecolor=fc))


def arrow(ax, p1, p2, color=BLUE, lw=1.8, ms=12, rad=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=ms,
                                 linewidth=lw, color=color,
                                 connectionstyle="arc3,rad=%s" % rad))


def txt(ax, x, y, s, size=9, color=TEXT, weight="normal", ha="center", va="center",
        ls=1.35):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va,
            linespacing=ls)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=200, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print("figura:", name)


# ---------------------------------------------------------------- Figura 1
def fig_fluxo_etapas():
    fig, ax = canvas(9.2, 4.6)
    steps = [
        ("01", "Ensaio", "Cleitura, FD\ne faixa", BLUE),
        ("02", "Certificados", "u(x) de padrões\ne equipamentos", TEAL),
        ("03", "Precisão", "Histórico mensal\n(sIP, ANOVA)", BLUE),
        ("04", "Check", "Viés e\nrecuperação", TEAL),
        ("05", "Orçamento", "uc = \u221a\u03a3(ci\u00b7u)\u00b2\ne participações", BLUE),
        ("06", "Resultado", "y \u00b1 U e\nregra de decisão", TEAL),
    ]
    w, gap, y, h = 14.2, 2.6, 44, 30
    x0 = 2.0
    for i, (n, t, b, c) in enumerate(steps):
        x = x0 + i * (w + gap)
        rbox(ax, x, y, w, h, WHITE, c)
        rbox(ax, x, y + h - 7.6, w, 7.6, c, c, 0)
        txt(ax, x + w / 2, y + h - 3.8, n, 11, WHITE, "bold")
        txt(ax, x + w / 2, y + h - 10.5, t, 9.6, NAVY, "bold", va="top")
        txt(ax, x + w / 2, y + h - 17.5, b, 7.9, MUTED, va="top")
        if i < len(steps) - 1:
            arrow(ax, (x + w + 0.2, y + h / 2), (x + w + gap - 0.2, y + h / 2), LINE, 2.2)
    txt(ax, 50, 93, "Fluxo de preenchimento da calculadora", 13, NAVY, "bold")
    txt(ax, 50, 85, "Preencha na ordem das abas. Cada etapa alimenta a seguinte; "
                    "o resultado é recalculado ao vivo.", 8.6, MUTED)
    rbox(ax, 24, 5, 52, 25, WARNB, AMBER, 1.4)
    txt(ax, 50, 25.5, "SAÍDA", 9, WARN, "bold")
    txt(ax, 50, 18,
        "Memória de cálculo (PDF A4)  \u00b7  Estudo JSON\nCSV mensal  \u00b7  CSV do orçamento",
        8.6, TEXT)
    arrow(ax, (50, 43.5), (50, 30.5), AMBER, 2.0)
    save(fig, "fig01_fluxo_etapas.png")


# ---------------------------------------------------------------- Figura 2
def fig_escada_incerteza():
    fig, ax = canvas(9.2, 4.3)
    txt(ax, 50, 95, "Da incerteza-padrão à incerteza expandida", 13, NAVY, "bold")
    cols = [
        (4, "u(x)", "Incerteza-padrão de cada\nfonte (tipo A ou B)",
         "u = U/k  \u00b7  a/\u221a3  \u00b7  r/\u221a12", TEAL),
        (35.5, "uc(y)", "Incerteza combinada das\ncontribuições independentes",
         "uc = \u221a\u03a3 (ci\u00b7u)\u00b2", BLUE),
        (67, "U = k \u00b7 uc", "Incerteza expandida\n(intervalo de abrangência)",
         "U rel = 100\u00b7U/y", NAVY),
    ]
    for x, title, body, formula, c in cols:
        rbox(ax, x, 40, 29, 40, WHITE, c, 1.4)
        txt(ax, x + 14.5, 72, title, 12.5, c, "bold")
        txt(ax, x + 14.5, 60.5, body, 8.6, TEXT)
        rbox(ax, x + 2.2, 44.5, 24.6, 8.5, LIGHT, LIGHT, 0)
        txt(ax, x + 14.5, 48.8, formula, 9, c, "bold")
    arrow(ax, (33.4, 60), (35.1, 60), LINE, 2.4)
    arrow(ax, (64.9, 60), (66.6, 60), LINE, 2.4)
    txt(ax, 50, 29, "Somam-se VARIÂNCIAS (quadrados), nunca as incertezas diretamente. "
                    "Fontes correlacionadas exigem tratamento próprio.", 8.8, MUTED)
    txt(ax, 50, 17, "Regra de ouro: sem declarar k e as hipóteses, U não tem "
                    "significado estatístico garantido.", 8.8, WARN)
    save(fig, "fig02_escada_incerteza.png")


# ---------------------------------------------------------------- Figura 3
def fig_arvore_distribuicao():
    fig, ax = canvas(9.2, 4.9)
    txt(ax, 50, 96, "Como converter cada entrada em u(x)?", 13, NAVY, "bold")
    rbox(ax, 33, 80, 34, 11, NAVY, NAVY, 1.4)
    txt(ax, 50, 85.5, "O que o certificado informa?", 10, WHITE, "bold")
    cards = [
        ("NORMAL", "U e k\n(ex.: U = 0,05 mL; k = 2)",
         "u(x) = U / k\n\u2192 0,05 / 2 = 0,025 mL", "Incerteza expandida\nde certificado", TEAL),
        ("RETANGULAR", "limite \u00b1a\n(ex.: tolerância \u00b10,2 mL)",
         "u(x) = a / \u221a3\n\u2192 0,2 / 1,732 = 0,1155 mL", "Limites sem\ndistribuição declarada", BLUE),
        ("RESOLUÇÃO", "passo r\n(ex.: leitura de 0,1 mL)",
         "u(x) = r / \u221a12\n\u2192 0,1 / 3,464 = 0,0289 mL", "Menor divisão\nnomeável", WARN),
    ]
    w = 30.0
    for i, (tag, inp, form, when, c) in enumerate(cards):
        x = 1.5 + i * 33.0
        rbox(ax, x, 33, w, 40, WHITE, c, 1.5)
        rbox(ax, x, 65, w, 8, c, c, 0)
        txt(ax, x + w / 2, 69, tag, 10, WHITE, "bold")
        txt(ax, x + w / 2, 60, inp, 8.4, TEXT)
        rbox(ax, x + 1.4, 44, w - 2.8, 11, LIGHT, LIGHT, 0)
        txt(ax, x + w / 2, 49.5, form, 9.2, c, "bold", ls=1.5)
        txt(ax, x + w / 2, 38.5, when, 7.9, MUTED)
        arrow(ax, (50, 79.8), (x + w / 2, 73.4), LINE, 1.8)
    txt(ax, 50, 22, "Na calculadora, escolha o seletor \u201cDistribuição\u201d. O divisor é "
                    "aplicado automaticamente e aparece na coluna \u201cDistribuição / divisor\u201d.",
        8.6, TEXT)
    txt(ax, 50, 12, "Atenção: absorbância (unidade fotométrica) não pode ser tratada como "
                    "fonte multiplicativa relativa \u2014 informe o coeficiente de sensibilidade c.",
        8.4, DANGER)
    save(fig, "fig03_arvore_distribuicao.png")


# ---------------------------------------------------------------- Figura 4
def fig_mockup_identidade():
    fig, ax = canvas(9.2, 5.2)
    txt(ax, 50, 96, "Etapa 01 \u00b7 Identificação do ensaio \u2014 campo a campo", 13, NAVY, "bold")
    rbox(ax, 2, 17, 96, 73, "#f7fafc", LINE, 1.2)
    fields = [
        ("Identificação do estudo", "NIT-2026-EXEMPLO", 0),
        ("Método", "Griess \u2014 proc. NIT-01", 0),
        ("Matriz", "Água \u2014 controle estável", 0),
        ("Faixa mínima (mg/L)", "0,05", 1),
        ("Faixa máxima (mg/L)", "2", 1),
        ("Cleitura (mg/L de NO\u2082\u207b)", "0,850", 1),
        ("Fator de diluição FD", "1", 1),
        ("Responsável", "Analista (fictício)", 0),
        ("Data do estudo", "2026-09-11", 2),
        ("Versão do estudo", "1", 2),
    ]
    cw, ch, gx, gy = 45.0, 11.8, 2.6, 1.6
    x0, y0 = 4.0, 75.0
    for i, (lab, val, flag) in enumerate(fields):
        col, row = i // 5, i % 5
        x = x0 + col * (cw + gx)
        y = y0 - row * (ch + gy)
        ec = (BLUE if flag == 1 else TEAL if flag == 2 else LINE)
        rbox(ax, x, y, cw, ch, WHITE, ec, 1.3 if flag else 1.0)
        txt(ax, x + 1.8, y + ch - 3.2, lab, 7.8, MUTED, ha="left", va="center")
        txt(ax, x + 1.8, y + 3.4, val, 9.2, NAVY, "bold", ha="left", va="center")
    txt(ax, 50, 12,
        "Azul = entram na fórmula y = Cleitura \u00d7 FD.  "
        "Teal = apenas identificam o estudo.", 8.4, MUTED)
    txt(ax, 50, 7,
        "Cleitura deve estar dentro de [faixa mínima, faixa máxima]; a faixa se refere à "
        "solução medida ANTES do FD.", 8.2, DANGER)
    save(fig, "fig04_mockup_identidade.png")


# ---------------------------------------------------------------- Figura 5
def fig_precisao_anova():
    import math
    vals = [i - 11.5 for i in range(24)]
    m = sum(vals) / len(vals)
    s = math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))
    scale = 0.021 / s
    results = [0.846 + vals[(i * 7) % 24] * scale for i in range(24)]
    mean = sum(results) / len(results)

    fig = plt.figure(figsize=(9.2, 5.6))
    fig.text(0.5, 0.965, "Precisão intermediária: a série do exemplo e o cálculo do sIP",
             ha="center", fontsize=11.5, fontweight="bold", color=NAVY)
    ap = fig.add_axes([0.085, 0.66, 0.86, 0.25])
    ap.scatter(results, [1] * len(results), s=30, color=BLUE, alpha=0.8, zorder=3,
               edgecolor="white", linewidth=0.6)
    ap.axvline(mean, color=TEAL, lw=2, zorder=4)
    ap.axvspan(mean - 0.021, mean + 0.021, color=TEAL, alpha=0.13, zorder=1)
    ap.axvline(mean + 0.042, color=LINE, lw=1, ls="--")
    ap.axvline(mean - 0.042, color=LINE, lw=1, ls="--")
    ap.set_yticks([])
    ap.set_ylim(0.4, 1.6)
    ap.set_xlabel("resultado do controle (mg/L)  \u2014  24 resultados, 24 corridas",
                  fontsize=8, color=MUTED)
    ap.tick_params(labelsize=8)
    for sp in ("top", "right", "left"):
        ap.spines[sp].set_visible(False)
    ap.annotate("média = 0,846", xy=(mean, 1.18), xytext=(mean + 0.003, 1.42),
                fontsize=8, color=TEAL, fontweight="bold")
    ap.annotate("faixa \u00b1 sIP = 0,021", xy=(mean + 0.021, 0.9),
                xytext=(mean + 0.024, 0.60), fontsize=7.8, color=MUTED)

    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    cards = [
        ("1 resultado por corrida", BLUE,
         "Nenhuma corrida tem réplicas.\nUsa o desvio-padrão amostral s\ndos resultados independentes."),
        ("Réplicas balanceadas", TEAL,
         "Todas as corridas têm m réplicas.\nsIP = \u221a[MSdentro + (MSentre \u2212 MSdentro)/m]\n(ANOVA de efeitos aleatórios)"),
        ("Réplicas desbalanceadas", DANGER,
         "m diferente entre corridas \u2192 ERRO.\nUse desenho balanceado ou avalie\nos componentes de variância fora."),
    ]
    cw = 31.0
    for i, (t, c, b) in enumerate(cards):
        x = 2.0 + i * 32.6
        rbox(ax, x, 30, cw, 22, WHITE, c, 1.4)
        txt(ax, x + cw / 2, 48, t, 8.8, c, "bold")
        txt(ax, x + cw / 2, 39, b, 7.8, TEXT, ls=1.55)
    txt(ax, 50, 24,
        "Cada linha da tabela = uma preparação completa.  "
        "Corrida = preparação da curva + sessão analítica (C1, C2, C3...).", 8.4, MUTED)
    rbox(ax, 2, 7, 96, 13, LIGHT, LIGHT, 0)
    txt(ax, 50, 13.5, "Média = 0,846 mg/L   \u00b7   sIP = 0,021 mg/L   \u00b7   RSD = 2,48 %   \u00b7   "
                      "uprecisão(y) = |y| \u00d7 sIP / |média|", 8.4, NAVY, "bold")
    txt(ax, 50, 3, "Histórico curto ou de um único dia gera AVISO, não erro; "
                   "não é um mínimo prescrito pela ISO 17025.", 8.0, WARN)
    save(fig, "fig05_precisao_anova.png")


# ---------------------------------------------------------------- Figura 6
def fig_vies_check():
    fig = plt.figure(figsize=(9.2, 3.6))
    a = fig.add_axes([0.09, 0.32, 0.84, 0.44])
    a.set_xlim(0.788, 0.812)
    a.set_ylim(0.12, 1.0)
    a.set_yticks([])
    ref, mean = 0.800, 0.796
    uref, uexp = 0.0024, 0.0048
    a.axvspan(ref - uref, ref + uref, color=TEAL, alpha=0.18, zorder=1)
    a.axvspan(ref - uexp, ref + uexp, color=TEAL, alpha=0.08, zorder=0)
    a.axvline(ref, color=TEAL, lw=2.2, zorder=3)
    a.axvline(mean, color=BLUE, lw=2.2, zorder=3)
    sm = 0.009 / (10 ** 0.5)
    a.errorbar([mean], [0.5], xerr=[[sm], [sm]], fmt="o", color=BLUE,
               capsize=3, zorder=4, markersize=5)
    a.annotate("", xy=(ref, 0.86), xytext=(mean, 0.86),
               arrowprops=dict(arrowstyle="<->", color=DANGER, lw=1.6))
    a.text((ref + mean) / 2, 0.90, "viés b = \u22120,5 %", ha="center", fontsize=8.6,
           color=DANGER, fontweight="bold")
    a.text(ref + 0.00035, 0.14, "valor designado\n0,800 mg/L", ha="left",
           fontsize=8, color=TEAL, linespacing=1.3)
    a.text(mean - 0.00035, 0.14, "m\u00e9dia do check\n0,796 mg/L (n = 10)",
           ha="right", fontsize=8, color=BLUE, linespacing=1.3)
    a.text(ref + uexp, 0.72, "U do check = \u00b10,0048 mg/L", fontsize=7.6, color=TEAL,
           ha="right")
    a.set_xlabel("concentração do check (mg/L)", fontsize=8, color=MUTED)
    a.tick_params(labelsize=8)
    for sp in ("top", "right", "left"):
        a.spines[sp].set_visible(False)
    fig.text(0.5, 0.94, "Viés e incerteza do check independente", ha="center",
             fontsize=10.5, fontweight="bold", color=NAVY)
    fig.text(0.5, 0.05,
             "b = (x\u0304check \u2212 Cref) / Cref     \u2022     "
             "ub,rel = \u221a[b\u00b2 + (scheck/(\u221an\u00b7Cref))\u00b2 + (Uref/(kref\u00b7Cref))\u00b2]",
             ha="center", fontsize=8.8, color=TEXT)
    save(fig, "fig06_vies_check.png")


# ---------------------------------------------------------------- Figura 7
def fig_orcamento_barras():
    fig = plt.figure(figsize=(9.2, 3.9))
    a = fig.add_axes([0.30, 0.26, 0.64, 0.58])
    labels = ["Precisão intermediária", "Recuperação residual de matriz",
              "Viés global / check"]
    contrib = [0.0210993, 0.0139669, 0.0058060]
    share = [66.05, 28.94, 5.00]
    colors = [BLUE, TEAL, AMBER]
    ypos = list(range(len(labels)))
    a.barh(ypos, contrib, color=colors, height=0.55)
    a.set_yticks(ypos)
    a.set_yticklabels(labels, fontsize=9)
    a.invert_yaxis()
    a.set_xlim(0, 0.0275)
    a.set_xlabel("|ci \u00b7 u(x)| contribuição à incerteza (mg/L)", fontsize=8.5,
                 color=MUTED)
    a.tick_params(labelsize=8)
    for sp in ("top", "right"):
        a.spines[sp].set_visible(False)
    for i, (c, s) in enumerate(zip(contrib, share)):
        a.text(c + 0.0005, i, "%.5f  (%.2f%%)" % (c, s), va="center", fontsize=8.2,
               color=TEXT, fontweight="bold")
    a.axvline(0.0259608, color=NAVY, lw=1.4, ls="--")
    a.text(0.0259608, -0.62, "uc = 0,02596", fontsize=8, color=NAVY, ha="center")
    fig.text(0.5, 0.94, "Orçamento do exemplo: quem domina a incerteza?",
             ha="center", fontsize=10.5, fontweight="bold", color=NAVY)
    fig.text(0.5, 0.04, "A participação é a fração da VARIÂNCIA total (\u03a3 = 100 %), "
                        "não a fração linear de U.",
             ha="center", fontsize=8.4, color=MUTED)
    save(fig, "fig07_orcamento_barras.png")


# ---------------------------------------------------------------- Figura 8
def fig_resultado_bandas():
    fig = plt.figure(figsize=(9.2, 3.6))
    scen = [
        ("Caso A \u00b7 L = 1,00\nCONFORME", 1.00, OK, OKB,
         "y + U = 0,902 \u2264 L"),
        ("Caso B \u00b7 L = 0,86\nNÃO DEMONSTRADA", 0.86, WARN, WARNB,
         "y \u2212 U < L < y + U"),
        ("Caso C \u00b7 L = 0,79\nNÃO CONFORME", 0.79, DANGER, DANGERB,
         "y \u2212 U = 0,798 > L"),
    ]
    y, U = 0.850, 0.052
    for i, (title, L, c, cb, note) in enumerate(scen):
        a = fig.add_axes([0.07 + i * 0.31, 0.30, 0.27, 0.42])
        a.set_xlim(0.75, 1.05)
        a.set_ylim(0, 1)
        a.set_yticks([])
        a.axvspan(y - U, y + U, color=c, alpha=0.16, zorder=1)
        a.errorbar([y], [0.5], xerr=[[U], [U]], fmt="o", color=c, capsize=4,
                   markersize=6, zorder=3)
        a.axvline(L, color=NAVY, lw=1.8, ls="--", zorder=2)
        a.text(L, 0.85, "L", fontsize=8, color=NAVY, ha="center", fontweight="bold")
        a.text(0.03, 0.06, "y = 0,850\nU = 0,052", fontsize=7.6, color=TEXT,
               transform=a.transAxes, ha="left", va="bottom", linespacing=1.3)
        a.set_xlabel(note, fontsize=7.4, color=c)
        a.tick_params(labelsize=7)
        for sp in ("top", "right", "left"):
            a.spines[sp].set_visible(False)
        a.add_patch(FancyBboxPatch((0.02, 1.04), 0.96, 0.20, transform=a.transAxes,
                                   boxstyle="round,pad=0,rounding_size=0.04",
                                   fc=cb, ec=c, lw=1.2, clip_on=False))
        a.text(0.5, 1.14, title, transform=a.transAxes, ha="center", va="center",
               fontsize=7.8, color=c, fontweight="bold", linespacing=1.35)
    fig.text(0.5, 0.94, "Regra de decisão com banda U: y + U \u2264 L", ha="center",
             fontsize=10.5, fontweight="bold", color=NAVY)
    fig.text(0.5, 0.05, "O limite L é comparado com o intervalo y \u00b1 U, não apenas "
                        "com o valor y.", ha="center", fontsize=8.4, color=MUTED)
    save(fig, "fig08_resultado_bandas.png")


# ---------------------------------------------------------------- Figura 9
def fig_fluxo_dados():
    fig, ax = canvas(9.2, 4.0)
    txt(ax, 50, 94, "O que sai da calculadora e onde termina cada arquivo", 13, NAVY, "bold")
    rbox(ax, 34, 66, 32, 16, NAVY, NAVY, 1.4)
    txt(ax, 50, 74, "Sessão de trabalho\n(estado na tela)", 9.4, WHITE, "bold")
    outs = [
        (2, "Estudo JSON", "Todo o formulário +\ndecisões + certificados", BLUE),
        (26, "CSV mensal", "Tabela de resultados\n(1 linha por ensaio)", TEAL),
        (50, "CSV orçamento", "Fontes, u(x), ci\nparticipação e uc/U", AMBER),
        (74, "Memória (PDF)", "Relatório A4 completo\n+ glossário", NAVY),
    ]
    for x, t, b, c in outs:
        rbox(ax, x, 18, 24, 30, WHITE, c, 1.4)
        rbox(ax, x, 40, 24, 8, c, c, 0)
        txt(ax, x + 12, 44, t, 9.2, WHITE, "bold")
        txt(ax, x + 12, 30, b, 8.2, TEXT)
        arrow(ax, (50, 65.5), (x + 12, 48.6), LINE, 1.6)
    txt(ax, 50, 11,
        "JSON = guardar/retomar o estudo.  CSV = tabelas para planilha.  "
        "PDF = registrar e assinar a memória de cálculo.",
        8.6, MUTED)
    save(fig, "fig09_fluxo_dados.png")


# --------------------------------------------------------------- Figura 10
def fig_tratamento_semaforo():
    fig, ax = canvas(9.2, 4.0)
    txt(ax, 50, 94, "Coluna \u201cTratamento no orçamento\u201d: qual escolher?", 13, NAVY, "bold")
    cards = [
        ("Já incorporada\nao estudo", OK, OKB,
         "O efeito já está coberto pelo\ncheck independente, pela precisão\nou pelo histórico.\n\n\u2192 Registrada, mas NÃO somada.\n(caso típico de padrões e vidraria\nde preparo)"),
        ("Incluir contribuição\nindependente", WARN, WARNB,
         "A fonte traz incerteza que ainda\nNÃO está coberta por nenhum estudo.\n\n\u2192 Somada ao orçamento (tipo B).\nExige justificativa. Bloqueada se\ncitar analista/repetibilidade/precisão."),
        ("Não aplicável\nao resultado", MUTED, "#eef1f4",
         "A fonte não influencia o resultado\n(o equipamento foi usado para\noutra finalidade).\n\n\u2192 Apenas registrada para\nrastreabilidade, sem contribuição."),
    ]
    w = 30.5
    for i, (t, c, cb, b) in enumerate(cards):
        x = 1.5 + i * 33.0
        rbox(ax, x, 14, w, 66, cb, c, 1.6)
        rbox(ax, x, 67, w, 13, c, c, 1.6)
        txt(ax, x + w / 2, 73.5, t, 8.8, WHITE, "bold", ls=1.5)
        txt(ax, x + w / 2, 38, b, 7.9, TEXT, ls=1.55)
    txt(ax, 50, 7,
        "Bloqueio automático: nomear uma fonte como \u201cAnalista\u201d, \u201cRepetibilidade\u201d "
        "ou \u201cPrecisão intermediária\u201d e marcá-la como incluir gera ERRO de dupla contagem.",
        8.2, DANGER)
    save(fig, "fig10_tratamento_semaforo.png")


# --------------------------------------------------------------- Figura 11
def fig_base_nitrito():
    fig, ax = canvas(9.2, 3.4)
    txt(ax, 50, 90, "Base do resultado: tudo em NO\u2082\u207b", 13, NAVY, "bold")
    rbox(ax, 6, 40, 30, 34, WHITE, BLUE, 1.4)
    txt(ax, 21, 66, "Resultado como\nNO\u2082\u207b\u2013N", 9.4, BLUE, "bold")
    txt(ax, 21, 50, "ex.: 0,259 mg/L de N", 8.2, MUTED)
    rbox(ax, 64, 40, 30, 34, WHITE, TEAL, 1.4)
    txt(ax, 79, 66, "Resultado como\nNO\u2082\u207b", 9.4, TEAL, "bold")
    txt(ax, 79, 50, "ex.: 0,850 mg/L de NO\u2082\u207b", 8.2, MUTED)
    arrow(ax, (37, 57), (63, 57), AMBER, 2.4)
    txt(ax, 50, 61, "\u00d7 3,2845", 9.6, WARN, "bold")
    txt(ax, 50, 53, "(concentração e\nincerteza absoluta)", 7.6, MUTED)
    txt(ax, 50, 30,
        "Converta NO\u2082\u207b\u2013N \u2192 NO\u2082\u207b ANTES de digitar: multiplique a concentração E a "
        "incerteza absoluta por \u2248 3,2845.", 8.6, TEXT)
    txt(ax, 50, 18,
        "Mantenha a mesma base em soluções, check, fortificações e resultados. "
        "Nunca misture bases na mesma coluna.", 8.4, DANGER)
    txt(ax, 50, 8, "A faixa de trabalho (mín./máx.) refere-se à solução medida "
                   "antes do fator de diluição.", 8.2, MUTED)
    save(fig, "fig11_base_nitrito.png")


# --------------------------------------------------------------- Figura 12
def fig_faixa_trabalho():
    fig = plt.figure(figsize=(9.2, 2.7))
    a = fig.add_axes([0.07, 0.30, 0.88, 0.36])
    a.set_xlim(-0.2, 2.9)
    a.set_ylim(0, 1)
    a.set_yticks([])
    a.axvspan(0.05, 2.0, color=BLUE, alpha=0.10)
    a.plot([0.05, 2.0], [0.5, 0.5], color=BLUE, lw=3)
    a.plot([0.85], [0.5], "o", color=OK, markersize=9, zorder=4)
    a.plot([2.5], [0.5], "X", color=DANGER, markersize=11, zorder=4)
    a.annotate("Cleitura 0,850\nDENTRO da faixa \u2713", xy=(0.85, 0.5),
               xytext=(0.62, 0.80), fontsize=8.2, color=OK, fontweight="bold",
               arrowprops=dict(arrowstyle="->", color=OK, lw=1.2))
    a.annotate("Cleitura 2,50\nFORA da faixa \u2717", xy=(2.5, 0.5),
               xytext=(2.05, 0.80), fontsize=8.2, color=DANGER, fontweight="bold",
               arrowprops=dict(arrowstyle="->", color=DANGER, lw=1.2))
    a.set_xticks([0.05, 0.5, 1.0, 1.5, 2.0, 2.5])
    a.tick_params(labelsize=8)
    for sp in ("top", "right", "left"):
        a.spines[sp].set_visible(False)
    fig.text(0.5, 0.90, "Faixa de trabalho (mín. 0,05 \u2013 máx. 2,0 mg/L)", ha="center",
             fontsize=10.5, fontweight="bold", color=NAVY)
    fig.text(0.5, 0.06,
             "Fora da faixa a ferramenta bloqueia: \u201cCleitura fora da faixa de trabalho: "
             "avalie diluição ou outro nível.\u201d", ha="center", fontsize=8.2, color=DANGER)
    save(fig, "fig12_faixa_trabalho.png")


if __name__ == "__main__":
    fig_fluxo_etapas()
    fig_escada_incerteza()
    fig_arvore_distribuicao()
    fig_mockup_identidade()
    fig_precisao_anova()
    fig_vies_check()
    fig_orcamento_barras()
    fig_resultado_bandas()
    fig_fluxo_dados()
    fig_tratamento_semaforo()
    fig_base_nitrito()
    fig_faixa_trabalho()
    print("OK: todas as figuras geradas em", OUT)






