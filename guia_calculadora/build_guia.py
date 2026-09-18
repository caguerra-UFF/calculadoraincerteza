# -*- coding: utf-8 -*-
"""Gera o PDF 'Guia Ilustrado da Calculadora de Incerteza (Nitrito - v2)'.
Skill de PDF: geração com reportlab + revisão visual renderizando as páginas (PyMuPDF).
Executar:  python guia_calculadora/build_guia.py
"""
import os
import matplotlib
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, Image,
                                KeepTogether, NextPageTemplate,
                                PageBreak, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIG = os.path.join(HERE, "figures")
OUT = os.path.join(ROOT, "Guia_Ilustrado_Calculadora_Incerteza_Nitrito.pdf")

NAVY = colors.HexColor("#102e46")
BLUE = colors.HexColor("#0f4c81")
TEAL = colors.HexColor("#087e83")
LIGHT = colors.HexColor("#eaf2f7")
LINE = colors.HexColor("#c6d4df")
TEXT = colors.HexColor("#203647")
MUTED = colors.HexColor("#52697a")
WARN = colors.HexColor("#81500a")
WARNB = colors.HexColor("#fdf3e0")
DANGER = colors.HexColor("#a32832")
DANGERB = colors.HexColor("#fbeaec")
OK = colors.HexColor("#1f7a4d")
OKB = colors.HexColor("#e8f5ee")
AMBER = colors.HexColor("#c98a12")
GREY = colors.HexColor("#eef1f4")

# ---------------------------------------------------------------- fontes (Unicode)
_fdir = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
pdfmetrics.registerFont(TTFont("DJV", os.path.join(_fdir, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DJV-Bold", os.path.join(_fdir, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DJV-It", os.path.join(_fdir, "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("DJV-BoldIt", os.path.join(_fdir, "DejaVuSans-BoldOblique.ttf")))
pdfmetrics.registerFont(TTFont("MONO", os.path.join(_fdir, "DejaVuSansMono.ttf")))
pdfmetrics.registerFont(TTFont("MONO-Bold", os.path.join(_fdir, "DejaVuSansMono-Bold.ttf")))
pdfmetrics.registerFontFamily("DJV", normal="DJV", bold="DJV-Bold", italic="DJV-It",
                              boldItalic="DJV-BoldIt")

PAGE_W, PAGE_H = A4
ML = MR = 1.7 * cm
MT, MB = 2.15 * cm, 1.65 * cm
CW = PAGE_W - ML - MR  # largura útil

# ---------------------------------------------------------------- estilos
def st(name, **kw):
    base = dict(fontName="DJV", fontSize=9.7, leading=13.6, textColor=TEXT,
                alignment=TA_JUSTIFY, spaceBefore=0, spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(name, **base)


S = {
    "H1": st("H1", fontName="DJV-Bold", fontSize=14.5, leading=18.5, textColor=colors.white,
             backColor=NAVY, borderPadding=(7, 9, 6, 9), alignment=TA_LEFT,
             spaceBefore=16, spaceAfter=11),
    "H2": st("H2", fontName="DJV-Bold", fontSize=11.8, leading=15, textColor=BLUE,
             alignment=TA_LEFT, spaceBefore=11, spaceAfter=4),
    "H3": st("H3", fontName="DJV-Bold", fontSize=10.2, leading=13, textColor=NAVY,
             alignment=TA_LEFT, spaceBefore=8, spaceAfter=3),
    "BODY": st("BODY"),
    "BULLET": st("BULLET", leftIndent=13, bulletIndent=3, spaceAfter=3.5),
    "CAP": st("CAP", fontSize=8.3, leading=11, textColor=MUTED, alignment=TA_CENTER,
              spaceBefore=3, spaceAfter=10),
    "TH": st("TH", fontName="DJV-Bold", fontSize=8.6, leading=10.8,
             textColor=colors.white, alignment=TA_LEFT, spaceAfter=0),
    "TD": st("TD", fontSize=8.5, leading=11.1, alignment=TA_LEFT, spaceAfter=0),
    "TDB": st("TDB", fontName="DJV-Bold", fontSize=8.5, leading=11.1, alignment=TA_LEFT,
              spaceAfter=0),
    "TDM": st("TDM", fontName="MONO", fontSize=8.2, leading=11, alignment=TA_LEFT,
              spaceAfter=0),
    "CAL": st("CAL", fontSize=9.1, leading=12.6, alignment=TA_LEFT, spaceAfter=0),
    "FORM": st("FORM", fontName="MONO-Bold", fontSize=8.9, leading=12.4,
               textColor=NAVY, alignment=TA_LEFT, spaceAfter=0),
    "COVER_T": st("COVER_T", fontName="DJV-Bold", fontSize=30, leading=34,
                  textColor=colors.white, alignment=TA_LEFT),
    "COVER_S": st("COVER_S", fontSize=12.5, leading=17, textColor=colors.HexColor("#c7dce9"),
                  alignment=TA_LEFT),
    "TOC_T": st("TOC_T", fontName="DJV-Bold", fontSize=20, leading=24, textColor=NAVY,
                alignment=TA_LEFT, spaceAfter=12),
}


# ---------------------------------------------------------------- helpers
def P(text, style="BODY"):
    return Paragraph(text, S[style])


def bullets(items, style="BULLET", mark="\u2022"):
    return [Paragraph(f"{mark}&nbsp;&nbsp;{t}", S[style]) for t in items]


def formula(lines):
    content = "<br/>".join(lines)
    t = Table([[Paragraph(content, S["FORM"])]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("LINEBEFORE", (0, 0), (0, -1), 2.2, BLUE),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


_CAL = {
    "dica": ("DICA", TEAL, LIGHT),
    "atencao": ("ATENÇÃO", WARN, WARNB),
    "erro": ("ERRO COMUM", DANGER, DANGERB),
    "nota": ("NOTA", BLUE, LIGHT),
    "ok": ("BOA PRÁTICA", OK, OKB),
}


def callout(kind, text, title=None):
    tag, c, bg = _CAL[kind]
    ttl = title or tag
    inner = (f'<font name="DJV-Bold" color="{c.hexval()}">{ttl}</font>&nbsp; {text}')
    t = Table([[Paragraph(inner, S["CAL"])]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 2.6, c),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def table(header, rows, widths, mono_cols=(), pad=5):
    data = [[Paragraph(h, S["TH"]) for h in header]]
    for r in rows:
        data.append([Paragraph(c, S["TDM"] if i in mono_cols else S["TD"])
                     for i, c in enumerate(r)])
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
        ("BOX", (0, 0), (-1, -1), 0.6, LINE),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f7fafc")))
    t.setStyle(TableStyle(style))
    return t


def fig(name, num, caption, max_w=None, max_h=9.7 * cm):
    path = os.path.join(FIG, name)
    iw, ih = PILImage.open(path).size
    w = max_w or CW
    h = w * ih / iw
    if h > max_h:
        h = max_h
        w = h * iw / ih
    img = Image(path, width=w, height=h)
    img.hAlign = "CENTER"
    # imagem + legenda viajam juntas: a legenda nunca fica orfa em outra pagina
    return [KeepTogether([Spacer(1, 5), img,
                          Paragraph(f"<b>Figura {num}.</b> {caption}", S["CAP"])])]


_last = {"n": 0}


def fig_n(name, caption, **kw):
    _last["n"] += 1
    return fig(name, _last["n"], caption, **kw)


# ---------------------------------------------------------------- documento e páginas
class GuiaDoc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            name = flowable.style.name
            if name == "H1":
                self.notify("TOCEntry", (0, flowable.getPlainText(), self.page))
            elif name == "H2":
                self.notify("TOCEntry", (1, flowable.getPlainText(), self.page))


def decorate(canvas, doc):
    canvas.saveState()
    page = doc.page
    if page == 1:
        # faixa superior da capa
        canvas.setFillColor(NAVY)
        canvas.rect(0, PAGE_H - 11.4 * cm, PAGE_W, 11.4 * cm, stroke=0, fill=1)
        canvas.setFillColor(TEAL)
        canvas.rect(0, PAGE_H - 11.4 * cm - 0.28 * cm, PAGE_W, 0.28 * cm, stroke=0, fill=1)
        canvas.restoreState()
        return
    # cabeçalho
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 1.02 * cm, PAGE_W, 1.02 * cm, stroke=0, fill=1)
    canvas.setFillColor(TEAL)
    canvas.rect(0, PAGE_H - 1.02 * cm, PAGE_W, 0.13 * cm, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("DJV-Bold", 7.4)
    canvas.drawString(ML, PAGE_H - 0.68 * cm,
                      "GUIA ILUSTRADO  \u00b7  CALCULADORA DE INCERTEZA DE MEDIÇÃO  \u00b7  NITRITO (v2)")
    canvas.setFont("DJV", 7.4)
    canvas.drawRightString(PAGE_W - MR, PAGE_H - 0.68 * cm,
                           "uso interno \u00b7 treinamento")
    # rodapé
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(ML, 1.16 * cm, PAGE_W - MR, 1.16 * cm)
    canvas.setFillColor(MUTED)
    canvas.setFont("DJV", 7.4)
    canvas.drawString(ML, 0.82 * cm,
                      "Memória de cálculo baseada no Guia Eurachem/CITAC e na abordagem Nordtest \u00b7 ISO/IEC 17025 (7.6, 7.7, 7.8)")
    canvas.setFont("DJV-Bold", 7.4)
    canvas.drawRightString(PAGE_W - MR, 0.82 * cm, f"página {page}")
    canvas.restoreState()


def first_page(canvas, doc):
    decorate(canvas, doc)


def make_doc():
    doc = GuiaDoc(OUT, pagesize=A4, leftMargin=ML, rightMargin=MR, topMargin=MT,
                  bottomMargin=MB, title="Guia Ilustrado da Calculadora de Incerteza "
                  "(Nitrito v2)", author="LMA - Estação de Estudo", subject="Incerteza "
                  "de medição - nitrito")
    frame = Frame(ML, MB, CW, PAGE_H - MT - MB, id="body",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="body", frames=[frame], onPage=decorate)])
    return doc


# ================================================================ CAPA
def ch_cover():
    s = [Spacer(1, 0.6 * cm)]
    s.append(Table([[Paragraph('<font color="#8ed9d6">ESTA\u00c7\u00c3O DE ESTUDO \u00b7 '
                               'QUALIDADE E METROLOGIA</font>',
                               ParagraphStyle("eyebrow", fontName="DJV-Bold", fontSize=9.2,
                                              leading=12, textColor=colors.HexColor("#8ed9d6")))]],
                    colWidths=[CW], style=TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0),
                                                      ("TOPPADDING", (0, 0), (-1, -1), 0),
                                                      ("BOTTOMPADDING", (0, 0), (-1, -1), 0)])))
    s.append(Spacer(1, 0.5 * cm))
    s.append(Paragraph("Guia Ilustrado da<br/>Calculadora de Incerteza", S["COVER_T"]))
    s.append(Spacer(1, 0.25 * cm))
    s.append(Paragraph("Nitrito (NO\u2082\u207b) \u00b7 determina\u00e7\u00e3o por Griess \u00b7 vers\u00e3o 2 "
                       "da calculadora<br/>Instru\u00e7\u00f5es de preenchimento, exemplos comentados "
                       "e como interpretar os resultados", S["COVER_S"]))
    s.append(Spacer(1, 3.3 * cm))
    s.append(Paragraph(
        '<b>Neste guia:</b> o passo a passo das seis etapas da calculadora, com figuras, '
        'tabelas campo a campo, um exemplo completo resolvido (0,850 \u00b1 0,052 mg/L de '
        'NO\u2082\u207b) e a leitura correta do or\u00e7amento e da decis\u00e3o.',
        ParagraphStyle("cov_lead", fontName="DJV", fontSize=10.5, leading=15, textColor=TEXT)))
    s.append(Spacer(1, 0.5 * cm))
    s.append(Paragraph(
        '<b>Como usar:</b> leia os capítulos 1 a 3 uma vez (conceitos e conven\u00e7\u00f5es); '
        'depois use os capítulos 4 a 9 no formato "consulte a etapa enquanto preenche"; '
        'termine pelo capítulo 10 (exemplo resolvido) e pelos ap\u00eandices.',
        ParagraphStyle("cov_how", fontName="DJV", fontSize=9.5, leading=13.5, textColor=MUTED)))
    s.append(Spacer(1, 1.1 * cm))
    s.append(table(["Documento", "Finalidade", "Base"],
                   [["Guia Ilustrado \u00b7 Calculadora de Incerteza (Nitrito v2)",
                     "Treinar e padronizar o preenchimento e a interpreta\u00e7\u00e3o",
                     "GUM / Eurachem-CITAC + abordagem Nordtest"],
                    ["P\u00fablico", "Analistas, revisores e respons\u00e1veis t\u00e9cnicos do laborat\u00f3rio",
                     "ISO/IEC 17025 itens 7.6, 7.7 e 7.8"]],
                   [CW * 0.40, CW * 0.32, CW * 0.28]))
    s.append(Spacer(1, 0.5 * cm))
    s.append(callout("atencao",
                     "Todos os n\u00fameros deste guia v\u00eam do <b>exemplo fict\u00edcio</b> da "
                     "pr\u00f3pria calculadora (banner \u201cEXEMPLO FICT\u00cdCIO\u201d). "
                     "Eles n\u00e3o representam nenhum ensaio real e n\u00e3o devem ser copiados "
                     "para uma mem\u00f3ria de c\u00e1lculo oficial."))
    s.append(Spacer(1, 0.45 * cm))
    s.append(Paragraph(
        '<font color="#52697a">Vers\u00e3o do guia 1.3 (calculadora 2.2) \u00b7 gerado a partir de '
        'calculadora_incerteza_nitrito_v2.html. Na ferramenta os textos s\u00e3o curtos: '
        'a defini\u00e7\u00e3o de cada termo sublinhado aparece ao passar o mouse e no '
        'gloss\u00e1rio. Este guia traz a mesma mat\u00e9ria explicada por extenso e foi '
        'conferido p\u00e1gina a p\u00e1gina (diagrama\u00e7\u00e3o e recortes) antes da entrega.</font>',
        ParagraphStyle("cov_foot", fontName="DJV", fontSize=8, leading=11, textColor=MUTED)))
    s.append(PageBreak())
    return s


# ================================================================ 1. VISÃO GERAL
def ch1():
    s = [Paragraph("1. A ferramenta em uma p\u00e1gina", S["H1"])]
    s.append(P("A calculadora organiza o c\u00e1lculo da <b>incerteza de medi\u00e7\u00e3o</b> de um "
               "ensaio de nitrito (NO\u2082\u207b, m\u00e9todo de Griess) em seis etapas encadeadas. "
               "Voc\u00ea informa o resultado medido e os documentos metrol\u00f3gicos; a ferramenta "
               "monta o or\u00e7amento de incerteza, combina as contribui\u00e7\u00f5es e expressa o "
               "resultado final no formato <b>y \u00b1 U</b>. Tudo roda no navegador, offline, e o "
               "resultado \u00e9 recalculado a cada digita\u00e7\u00e3o."))
    s.append(Paragraph("O que a ferramenta faz", S["H2"]))
    s += bullets([
        "Converte a incerteza dos certificados (padr\u00f5es, balan\u00e7as, vidraria, "
        "espectrofot\u00f4metro) em incerteza-padr\u00e3o u(x).",
        "Calcula a <b>precis\u00e3o intermedi\u00e1ria</b> a partir do hist\u00f3rico de controle "
        "(desvio-padr\u00e3o ou ANOVA de corridas/r\u00e9plicas).",
        "Avalia o <b>vi\u00e9s</b> com um check independente e, <b>se houver</b> estudo de "
        "fortifica\u00e7\u00e3o, a <b>recupera\u00e7\u00e3o</b> residual de matriz (opcional).",
        "Combina tudo em uc e U = k\u00b7uc, mostrando a <b>participa\u00e7\u00e3o</b> de cada fonte.",
        "Aplica a <b>regra de decis\u00e3o</b> quando h\u00e1 limite de conformidade.",
        "Emite a <b>mem\u00f3ria de c\u00e1lculo</b> (PDF/A4) e exporta JSON e CSV.",
    ])
    s += fig_n("fig01_fluxo_etapas.png",
               "As seis etapas da calculadora e os quatro produtos de sa\u00edda. "
               "Preencha na ordem das abas (01 a 06).")
    s.append(Paragraph("O que a ferramenta N\u00c3O faz", S["H2"]))
    s.append(table(["Limite", "Por qu\u00ea \u00e9 importante"],
                   [["N\u00e3o calcula graus de liberdade efetivos",
                     "O fator k \u00e9 declarado por voc\u00ea. k = 2 s\u00f3 equivale a ~95% se a "
                     "distribui\u00e7\u00e3o e os graus de liberdade justificarem."],
                    ["N\u00e3o trata correla\u00e7\u00f5es automaticamente",
                     "Fontes correlacionadas (mesma calibra\u00e7\u00e3o, mesma dilui\u00e7\u00e3o) devem "
                     "ser agrupadas em uma contribui\u00e7\u00e3o efetiva avaliada antes."],
                    ["N\u00e3o inclui a amostragem",
                     "A estimativa refere-se \u00e0 <b>amostra recebida</b>. Conserva\u00e7\u00e3o, "
                     "transporte e representatividade ficam em outro escopo."],
                    ["N\u00e3o decide sozinha a conformidade",
                     "Ela aplica a regra declarada (y + U \u2264 L). A escolha da regra e do risco "
                     "associado \u00e9 uma decis\u00e3o documentada do laborat\u00f3rio."],
                    ["N\u00e3o substitui a valida\u00e7\u00e3o",
                     "A calculadora estima; a adequa\u00e7\u00e3o do m\u00e9todo \u00e0 finalidade continua "
                     "sendo julgamento t\u00e9cnico registrado."]],
                   [CW * 0.34, CW * 0.66]))
    s.append(Spacer(1, 4))
    s.append(callout("nota",
                     "A ferramenta segue a l\u00f3gica do <b>GUM/Eurachem-CITAC</b> (or\u00e7amento de "
                     "incerteza) combinada \u00e0 <b>abordagem Nordtest</b> (precis\u00e3o "
                     "intermedi\u00e1ria + vi\u00e9s + recupera\u00e7\u00e3o). Ela apoia a conformidade "
                     "com os itens <b>7.6, 7.7 e 7.8</b> da ISO/IEC 17025."))
    s.append(Paragraph("Mapa das abas", S["H2"]))
    s.append(table(["Aba", "Etapa", "O que voc\u00ea registra"],
                   [["01", "Identifica\u00e7\u00e3o do ensaio", "C<sub>leitura</sub>, fator de dilui\u00e7\u00e3o, faixa "
                     "de trabalho, m\u00e9todo, matriz, respons\u00e1vel"],
                    ["02", "Padr\u00f5es, equipamentos e volumetria", "Certificados, validade, "
                     "distribui\u00e7\u00e3o e tratamento de cada fonte"],
                    ["03", "Precis\u00e3o intermedi\u00e1ria", "Hist\u00f3rico mensal de controle: corrida, "
                     "analista, equipamento, lote, r\u00e9plica e resultado"],
                    ["04", "Check e recupera\u00e7\u00e3o", "Valor designado, U e k do check e "
                     "resultados do check. Recupera\u00e7\u00e3o de fortifica\u00e7\u00e3o: "
                     "<b>opcional</b>"],
                    ["05", "Or\u00e7amento de incerteza", "Leitura das contribui\u00e7\u00f5es "
                     "(somente consulta \u2014 voc\u00ea n\u00e3o digita aqui)"],
                    ["06", "Resultado e regra de decis\u00e3o", "Fator k, modo de decis\u00e3o, limite "
                     "superior L e a base do acordo"]],
                   [CW * 0.08, CW * 0.26, CW * 0.66]))
    s.append(PageBreak())
    return s


# ================================================================ SUMÁRIO
def ch_toc():
    s = [Paragraph("Sum\u00e1rio", S["TOC_T"])]
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("toc0", fontName="DJV-Bold", fontSize=10.2, leading=15.5,
                       textColor=NAVY, spaceBefore=4, leftIndent=0, firstLineIndent=0),
        ParagraphStyle("toc1", fontName="DJV", fontSize=9.2, leading=13,
                       textColor=MUTED, leftIndent=16, firstLineIndent=0),
    ]
    toc.dotsMinLevel = 0
    s.append(toc)
    s.append(Spacer(1, 0.6 * cm))
    s.append(callout("dica",
                     "O sum\u00e1rio \u00e9 gerado automaticamente: os n\u00fameros de p\u00e1gina "
                     "correspondem \u00e0s p\u00e1ginas reais deste PDF. As figuras tamb\u00e9m s\u00e3o "
                     "numeradas em sequ\u00eancia (Figura 1 a 14)."))
    s.append(PageBreak())
    return s


# ================================================================ 2. CONCEITOS
def ch2():
    s = [Paragraph("2. Conceitos essenciais", S["H1"])]
    s.append(P("Antes de digitar o primeiro n\u00famero, vale fixar cinco ideias. Elas aparecem "
               "em todos os c\u00e1lculos seguintes e explicam por que a ferramenta pede cada "
               "informa\u00e7\u00e3o."))
    s += fig_n("fig02_escada_incerteza.png",
               "A incerteza cresce em tr\u00eas degraus: incerteza-padr\u00e3o u(x) de cada fonte, "
               "combina\u00e7\u00e3o em uc e expans\u00e3o em U = k\u00b7uc.")
    s.append(Paragraph("Cinco ideias-chave", S["H2"]))
    s.append(table(["Ideia", "Em uma frase", "Onde aparece na calculadora"],
                   [["Mensurando", "A grandeza que se quer reportar: a concentra\u00e7\u00e3o de "
                     "NO\u2082\u207b na amostra recebida.", "Resultado y = C<sub>leitura</sub> \u00d7 FD."],
                    ["Incerteza tipo A", "Avaliada por estat\u00edstica de r\u00e9plicas e do "
                     "hist\u00f3rico de controle.", "Precis\u00e3o intermedi\u00e1ria e dispers\u00e3o do check."],
                    ["Incerteza tipo B", "Avaliada por informa\u00e7\u00e3o externa: certificados, "
                     "toler\u00e2ncias, resolu\u00e7\u00e3o.", "Aba 02 (certificados)."],
                    ["Incerteza A/B", "Mistura dos dois: a estat\u00edstica fica com a "
                     "dispers\u00e3o e o documento responde pelo valor de refer\u00eancia.",
                     "Aba 04: no or\u00e7amento o vi\u00e9s do check e a recupera\u00e7\u00e3o "
                     "aparecem como <b>A/B</b>."],
                    ["Combinar incertezas", "Somam-se as vari\u00e2ncias; as incertezas nunca se "
                     "somam diretamente.", "Aba 05: uc = \u221a\u03a3(ci\u00b7u)\u00b2."],
                    ["Expandir", "Multiplica-se uc pelo fator de abrang\u00eancia k para obter o "
                     "intervalo declarado U.", "Aba 06: U = k \u00b7 uc."]],
                   [CW * 0.20, CW * 0.50, CW * 0.30]))
    s.append(Paragraph("S\u00edmbolos e unidades usados neste guia", S["H2"]))
    s.append(table(["S\u00edmbolo", "Significado", "Unidade t\u00edpica"],
                   [["y", "Resultado (concentra\u00e7\u00e3o) reportado", "mg/L de NO\u2082\u207b"],
                    ["C<sub>leitura</sub>", "Leitura da solu\u00e7\u00e3o na curva", "mg/L"],
                    ["FD", "Fator de dilui\u00e7\u00e3o da amostra", "adimensional"],
                    ["u(x)", "Incerteza-padr\u00e3o de uma fonte", "mesma unidade de x"],
                    ["c<sub>i</sub>", "Coeficiente de sensibilidade (\u2202y/\u2202x)", "adimensional "
                     "ou (mg/L)/unidade"],
                    ["u<sub>c</sub>", "Incerteza combinada do resultado", "mg/L"],
                    ["U", "Incerteza expandida (U = k\u00b7u<sub>c</sub>)", "mg/L"],
                    ["k", "Fator de abrang\u00eancia (declarado por voc\u00ea)", "adimensional"],
                    ["s<sub>IP</sub>", "Desvio-padr\u00e3o de precis\u00e3o intermedi\u00e1ria", "mg/L"],
                    ["b", "Vi\u00e9s relativo do check", "adimensional (%)"],
                    ["R", "Recupera\u00e7\u00e3o da fortifica\u00e7\u00e3o <i>(opcional)</i>", "%"],
                    ["L", "Limite superior de conformidade", "mg/L"]],
                   [CW * 0.14, CW * 0.62, CW * 0.24]))
    s.append(Spacer(1, 4))
    s.append(callout("atencao",
                     "O fator <b>k = 2</b> \u00e9 o mais comum, mas s\u00f3 corresponde a "
                     "aproximadamente 95% de abrang\u00eancia quando a distribui\u00e7\u00e3o e os graus "
                     "de liberdade justificam essa aproxima\u00e7\u00e3o. Declarar k e as hip\u00f3teses "
                     "\u00e9 responsabilidade de quem assina a mem\u00f3ria de c\u00e1lculo."))
    s.append(PageBreak())
    return s


# ================================================================ 3. CONVENÇÕES
def ch3():
    s = [Paragraph("3. Conven\u00e7\u00f5es de entrada (evitam a maioria dos erros)", S["H1"])]
    s.append(P("A calculadora \u00e9 tolerante com formatos, mas algumas conven\u00e7\u00f5es de "
               "entrada s\u00e3o obrigat\u00f3rias para que o n\u00famero digitado signifique o que "
               "voc\u00ea espera."))
    s.append(Paragraph("N\u00fameros e separadores", S["H2"]))
    s += bullets([
        "Use <b>v\u00edrgula</b> como separador decimal (0,850) ou ponto (0.850) \u2014 a ferramenta "
        "interpreta os dois.",
        "Nota\u00e7\u00e3o cient\u00edfica \u00e9 aceita (ex.: 1,2e-3); letras ou espa\u00e7os no "
        "meio tornam o campo inv\u00e1lido.",
        "Em listas de resultados (check, fortifica\u00e7\u00e3o), digite <b>um valor por linha</b>: "
        "\u00e9 o separador de registros.",
    ])
    s.append(Paragraph("A mesma base para todo o estudo", S["H2"]))
    s.append(P("O resultado \u00e9 sempre expresso como <b>NO\u2082\u207b</b>. Se o m\u00e9todo "
               "relatar nitrito como nitrog\u00eanio (NO\u2082\u207b\u2013N), converta "
               "<b>antes</b> de digitar, aplicando o fator 3,2845 tanto \u00e0 concentra\u00e7\u00e3o "
               "quanto \u00e0 incerteza absoluta."))
    s += fig_n("fig11_base_nitrito.png",
               "Convers\u00e3o de base NO\u2082\u207b\u2013N \u2192 NO\u2082\u207b. Converta a "
               "concentra\u00e7\u00e3o e a incerteza absoluta pelo mesmo fator.")
    s.append(callout("erro",
                     "Nunca misture bases na mesma coluna. Se check, fortifica\u00e7\u00f5es e "
                     "resultados mensais estiverem em bases diferentes, o vi\u00e9s e a incerteza "
                     "ficam sem sentido \u2014 mesmo que cada n\u00famero isolado esteja correto."))
    s.append(Paragraph("Faixa de trabalho", S["H2"]))
    s.append(P("A faixa m\u00ednima/m\u00e1xima descreve a <b>solu\u00e7\u00e3o efetivamente medida</b> "
               "(antes de aplicar o FD). A C<sub>leitura</sub> precisa cair dentro dessa faixa; caso "
               "contr\u00e1rio o c\u00e1lculo \u00e9 bloqueado."))
    s += fig_n("fig12_faixa_trabalho.png",
               "A C<sub>leitura</sub> \u00e9 validada contra a faixa de trabalho. Fora dela, a ferramenta "
               "orienta a avaliar dilui\u00e7\u00e3o ou outro n\u00edvel.")
    s.append(callout("dica",
                     "O fator de dilui\u00e7\u00e3o multiplica o resultado: y = C<sub>leitura</sub> "
                     "\u00d7 FD. Se houver dilui\u00e7\u00e3o extra al\u00e9m do que o estudo de "
                     "precis\u00e3o cobre, a ferramenta avisa (FD \u2260 1) para voc\u00ea verificar se "
                     "essa etapa est\u00e1 coberta ou se precisa de contribui\u00e7\u00e3o independente."))
    s.append(PageBreak())
    return s


# ================================================================ 4. ETAPA 01
def ch4():
    s = [Paragraph("4. Etapa 01 \u00b7 Identifica\u00e7\u00e3o do ensaio", S["H1"])]
    s.append(P("Esta aba define <b>o que</b> est\u00e1 sendo medido e <b>como</b> o resultado "
               "\u00e9 calculado. A f\u00f3rmula central \u00e9 simples: "
               "<b>y = C<sub>leitura</sub> \u00d7 FD</b>, em mg/L de NO\u2082\u207b."))
    s += fig_n("fig04_mockup_identidade.png",
               "Os dez campos da etapa 01 com os valores do exemplo. Em azul, os campos que "
               "entram no c\u00e1lculo; em teal, os que apenas identificam o estudo.",
               max_h=8.8 * cm)
    s.append(Paragraph("Campo a campo", S["H2"]))
    s.append(table(["Campo", "O que \u00e9", "Como preencher", "Exemplo"],
                   [["Identifica\u00e7\u00e3o do estudo", "C\u00f3digo \u00fanico do estudo de incerteza",
                     "Use um c\u00f3digo rastre\u00e1vel (ano e sequ\u00eancia)",
                     "NO\u2082\u207b-2026-EXEMPLO"],
                    ["M\u00e9todo", "Procedimento e vers\u00e3o", "Cite o procedimento interno "
                     "vigente", "Griess \u2014 proc. NO\u2082\u207b-01"],
                    ["Matriz", "Tipo de amostra / material de controle", "Descreva a matriz do "
                     "hist\u00f3rico", "\u00c1gua \u2014 controle est\u00e1vel"],
                    ["Faixa m\u00ednima / m\u00e1xima", "Limites da solu\u00e7\u00e3o medida",
                     "Faixa em que a curva foi validada", "0,05 \u2013 2 mg/L"],
                    ["C<sub>leitura</sub>", "Leitura da solu\u00e7\u00e3o na curva", "Resultado bruto da "
                     "amostra (antes do FD)", "0,850 mg/L"],
                    ["Fator de dilui\u00e7\u00e3o FD", "Quantas vezes a amostra foi dilu\u00edda",
                     "1 quando n\u00e3o h\u00e1 dilui\u00e7\u00e3o", "1"],
                    ["Respons\u00e1vel", "Quem conduziu o estudo", "Nome/fun\u00e7\u00e3o",
                     "Analista (fict\u00edcio)"],
                    ["Data do estudo", "Data de refer\u00eancia", "Formato AAAA-MM-DD",
                     "2026-09-11"],
                    ["Vers\u00e3o do estudo", "Controle de revis\u00e3o", "Incremente a cada "
                     "revis\u00e3o relevante", "1"]],
                   [CW * 0.20, CW * 0.30, CW * 0.30, CW * 0.20]))
    s.append(Paragraph("Passo a passo", S["H2"]))
    s += bullets([
        "Preencha os campos de identifica\u00e7\u00e3o (estudo, m\u00e9todo, matriz, "
        "respons\u00e1vel, data, vers\u00e3o).",
        "Informe a faixa de trabalho em que o m\u00e9todo foi validado.",
        "Digite a C<sub>leitura</sub> e o fator de dilui\u00e7\u00e3o. Confira a unidade exibida: mg/L de "
        "NO\u2082\u207b.",
        "Observe o rodap\u00e9: os indicadores de estat\u00edstica s\u00f3 ganham sentido depois "
        "que as abas 03 e 04 estiverem preenchidas.",
    ])
    s.append(callout("erro",
                     "Se a C<sub>leitura</sub> ficar <b>fora da faixa</b>, o c\u00e1lculo \u00e9 bloqueado com "
                     "a mensagem \u201cCleitura fora da faixa de trabalho: avalie dilui\u00e7\u00e3o "
                     "ou outro n\u00edvel.\u201d Isso evita extrapolar a curva."))
    s.append(callout("ok",
                     "Mantenha a faixa >= 2 valores significativos e coerente com a curva de "
                     "calibra\u00e7\u00e3o. Um estudo feito fora da faixa validada enfraquece toda "
                     "a mem\u00f3ria de c\u00e1lculo."))
    s.append(PageBreak())
    return s


# ================================================================ 5. ETAPA 02
def ch5():
    s = [Paragraph("5. Etapa 02 \u00b7 Padr\u00f5es, equipamentos e volumetria", S["H1"])]
    s.append(P("Aqui entram as contribui\u00e7\u00f5es <b>tipo B</b>: cada certificado, toler\u00e2ncia "
               "ou resolu\u00e7\u00e3o que influencia a concentra\u00e7\u00e3o. A tabela tem "
               "<b>uma linha por fonte</b>; compare os valores nas colunas e expanda os "
               "detalhes para revisar a aplica\u00e7\u00e3o."))
    s.append(Paragraph("As colunas da tabela", S["H2"]))
    s.append(table(["Coluna", "O que registrar", "Aten\u00e7\u00e3o"],
                   [["Fonte / equipamento", "Nome do padr\u00e3o, balan\u00e7a, vidraria, "
                     "instrumento", "Nomeie de forma reconhec\u00edvel no or\u00e7amento"],
                    ["Certificado / lote", "Identifica\u00e7\u00e3o do certificado ou do lote",
                     "Obrigat\u00f3rio para rastreabilidade"],
                    ["Validade (prazo)", "Prazo definido no seu sistema de gest\u00e3o",
                     "Vencido na data do estudo \u2192 aviso"],
                    ["Valor utilizado", "Valor <b>corrigido</b> do certificado",
                     "Para padr\u00e3o em solu\u00e7\u00e3o, use a concentra\u00e7\u00e3o final"],
                    ["Unidade", "mg/L, mL, mg, absorb\u00e2ncia...", "Unidade n\u00e3o "
                     "reconhecida exige coeficiente c expl\u00edcito"],
                    ["U / \u00b1a / r", "Incerteza expandida, limite ou passo de resolu\u00e7\u00e3o",
                     "Depende da distribui\u00e7\u00e3o escolhida"],
                    ["k", "Fator de abrang\u00eancia do certificado", "Habilitado s\u00f3 na "
                     "distribui\u00e7\u00e3o normal"],
                    ["Distribui\u00e7\u00e3o", "normal, retangular ou resolu\u00e7\u00e3o",
                     "Define o divisor aplicado"],
                    ["Tratamento", "J\u00e1 incorporada / Incluir / N\u00e3o aplic\u00e1vel",
                     "Evita contar a mesma incerteza duas vezes"],
                    ["Coeficiente c", "Sensibilidade do resultado \u00e0 fonte",
                     "Relativo usa y/x; absoluto informa o valor"],
                    ["Aplica\u00e7\u00e3o no modelo", "Justificativa do tratamento",
                     "Obrigat\u00f3ria quando a fonte \u00e9 inclu\u00edda"]],
                   [CW * 0.20, CW * 0.44, CW * 0.36]))
    s.append(Paragraph("Como converter cada entrada em u(x)", S["H2"]))
    s.append(P("O tipo de informa\u00e7\u00e3o no certificado decide a f\u00f3rmula. A calculadora faz "
               "a conta sozinha assim que voc\u00ea escolhe a distribui\u00e7\u00e3o."))
    s += fig_n("fig03_arvore_distribuicao.png",
               "\u00c1rvore de decis\u00e3o da distribui\u00e7\u00e3o. Normal usa U/k; retangular usa "
               "a/\u221a3; resolu\u00e7\u00e3o usa r/\u221a12.", max_h=7.0 * cm)
    s.append(formula([
        "u(x) = U<sub>cert</sub> / k        (normal)",
        "u(x) = a / \u221a3              (retangular, limite \u00b1a)",
        "u(x) = r / \u221a12             (resolu\u00e7\u00e3o, passo r)",
        "u<sub>rel</sub>(x) = u(x) / |x|   ;   contribui\u00e7\u00e3o = |c\u1d62 \u00b7 u(x)|",
    ]))
    # CH5_PART2
    s.append(Paragraph("O tratamento decide se a fonte entra na soma", S["H2"]))
    s.append(P("Registrar uma fonte <b>n\u00e3o</b> significa som\u00e1-la. A coluna \u201cTratamento\u201d "
               "define se a contribui\u00e7\u00e3o entra no or\u00e7amento. Essa \u00e9 a prote\u00e7\u00e3o "
               "contra a dupla contagem."))
    s += fig_n("fig10_tratamento_semaforo.png",
               "Os tr\u00eas tratamentos poss\u00edveis. S\u00f3 \u201cIncluir contribui\u00e7\u00e3o "
               "independente\u201d acrescenta algo \u00e0 soma \u2014 e exige justificativa.")
    s.append(callout("dica",
                     "Uma linha desta tabela pode ser <b>vinculada como fonte do check</b> "
                     "(aba 04): valor, U, k, certificado e validade passam a ser lidos daqui, "
                     "sem redigitar \u2014 e a linha \u00e9 marcada como \u201cj\u00e1 "
                     "incorporada\u201d, para n\u00e3o somar a mesma incerteza duas vezes."))
    s.append(Paragraph("Exemplo: as cinco fontes do estudo fict\u00edcio", S["H2"]))
    s.append(table(["Fonte", "Certificado", "U / \u00b1a / r", "k", "Distribui\u00e7\u00e3o",
                    "u(x)", "Tratamento"],
                   [["Padr\u00e3o de nitrito", "CRM-NO\u2082\u207b-2026-014", "1,0 mg/L", "2", "normal",
                     "0,5 mg/L", "J\u00e1 incorporada"],
                    ["Balan\u00e7a anal\u00edtica", "BAL-2026-008", "0,0002 g", "2", "normal",
                     "0,0001 g", "N\u00e3o aplic\u00e1vel"],
                    ["Bal\u00e3o volum\u00e9trico 100 mL", "VOL-100-2026-021", "0,2 mL", "2",
                     "normal", "0,1 mL", "J\u00e1 incorporada"],
                    ["Pipetador 10 mL", "PIP-010-2026-034", "0,05 mL", "2", "normal",
                     "0,025 mL", "J\u00e1 incorporada"],
                    ["Espectrofot\u00f4metro ESP-1", "ESP-2026-011", "0,002 abs", "2", "normal",
                     "0,001 abs", "J\u00e1 incorporada"]],
                   [CW * 0.205, CW * 0.19, CW * 0.115, CW * 0.040, CW * 0.15, CW * 0.115,
                    CW * 0.185], mono_cols=(2, 5), pad=4))
    s.append(Spacer(1, 5))
    s.append(Paragraph("Armadilhas frequentes nesta aba", S["H3"]))
    s += bullets([
        "<b>Balan\u00e7a em padr\u00e3o pronto em solu\u00e7\u00e3o:</b> se a balan\u00e7a foi usada "
        "apenas para reagentes, ela n\u00e3o entra na concentra\u00e7\u00e3o \u2014 registre como "
        "\u201cn\u00e3o aplic\u00e1vel\u201d.",
        "<b>Absorb\u00e2ncia:</b> a incerteza fotom\u00e9trica em absorb\u00e2ncia n\u00e3o pode ser "
        "dividida diretamente pela concentra\u00e7\u00e3o. Informe o coeficiente de sensibilidade.",
        "<b>Padr\u00f5es e vidraria de preparo:</b> normalmente j\u00e1 est\u00e3o cobertos pelo "
        "check independente e pelo hist\u00f3rico \u2014 marque \u201cj\u00e1 incorporada\u201d para "
        "n\u00e3o contar duas vezes.",
        "<b>Validade:</b> informe o prazo do seu sistema de gest\u00e3o; certificado vencido na "
        "data do estudo gera aviso.",
    ])
    s.append(callout("erro",
                     "Nomear uma fonte como \u201cAnalista\u201d, \u201cRepetibilidade\u201d ou "
                     "\u201cPrecis\u00e3o intermedi\u00e1ria\u201d e marc\u00e1-la como \u201cIncluir\u201d "
                     "dispara erro de <b>dupla contagem</b> \u2014 esse efeito j\u00e1 est\u00e1 na aba 03."))
    s.append(PageBreak())
    return s


# ================================================================ 6. ETAPA 03
def ch6():
    s = [Paragraph("6. Etapa 03 \u00b7 Precis\u00e3o intermedi\u00e1ria", S["H1"])]
    s.append(P("A precis\u00e3o intermedi\u00e1ria \u00e9 a contribui\u00e7\u00e3o <b>tipo A</b> mais "
               "importante: mede a dispers\u00e3o do m\u00e9todo ao longo do tempo, com trocas de "
               "analista, equipamento, lote e dia. Ela vem do hist\u00f3rico de um material de "
               "controle est\u00e1vel."))
    s += fig_n("fig05_precisao_anova.png",
               "Como o sIP \u00e9 obtido (desvio-padr\u00e3o ou ANOVA) e a s\u00e9rie do exemplo, "
               "com m\u00e9dia 0,846 mg/L e sIP = 0,021 mg/L.")
    s.append(Paragraph("A linha mensal, coluna por coluna", S["H2"]))
    s.append(table(["Coluna", "O que registrar", "Regra pr\u00e1tica"],
                   [["Grupo", "Material / matriz / n\u00edvel selecionado",
                     "Amostras ambientais distintas n\u00e3o formam s\u00e9rie de precis\u00e3o"],
                    ["Data", "Data da corrida", "Um valor por linha"],
                    ["Corrida", "C\u00f3digo da corrida (prepara\u00e7\u00e3o da curva + sess\u00e3o)",
                     "Pode ser gerado da data + analista; releituras da mesma solu\u00e7\u00e3o "
                     "n\u00e3o s\u00e3o prepara\u00e7\u00f5es independentes"],
                    ["Analista", "Quem executou", "Deixe variar: \u00e9 o que mede a "
                     "intermedi\u00e1ria"],
                    ["Equipamento", "Instrumento usado", "Idem \u2014 a varia\u00e7\u00e3o entre "
                     "equipamentos entra aqui"],
                    ["Lote", "Lote do material de controle", "\u00c9poca do controle"],
                    ["R\u00e9plica", "Identificador da r\u00e9plica na corrida",
                     "Duplicatas (1, 2) s\u00f3 quando houver mais de uma"],
                    ["Resultado", "Concentra\u00e7\u00e3o do controle", "mg/L de NO\u2082\u207b, "
                     "mesma base"]],
                   [CW * 0.14, CW * 0.36, CW * 0.50]))
    s.append(Paragraph("Rotina e controle: qual s\u00e9rie entra aqui", S["H2"]))
    s.append(P("As amostras ambientais do m\u00eas (por exemplo, tr\u00eas amostras coletadas) "
               "<b>n\u00e3o</b> formam a s\u00e9rie de precis\u00e3o: cada uma tem matriz e "
               "n\u00edvel pr\u00f3prios. O que entra nesta aba \u00e9 o <b>mesmo material de "
               "controle</b>, medido de novo a cada sess\u00e3o. Se o laborat\u00f3rio l\u00ea um "
               "<b>check</b> todo m\u00eas, ele \u00e9 o controle natural: registre cada leitura "
               "tamb\u00e9m como uma linha desta aba \u2014 e mantenha as mesmas leituras na aba "
               "04, onde elas respondem pelo vi\u00e9s."))
    s.append(table(["Desenho", "Como preencher", "O que a ferramenta usa"],
                   [["1 medi\u00e7\u00e3o por corrida (m = 1)", "Uma linha por sess\u00e3o; "
                     "R\u00e9plica = 1", "s amostral de todos os resultados"],
                    ["R\u00e9plicas balanceadas (m = 2, 3\u2026)", "O mesmo n\u00famero de "
                     "linhas em todas as corridas; R\u00e9plica = 1, 2, 3\u2026",
                     "ANOVA: MS<sub>dentro</sub> e MS<sub>entre</sub>"],
                    ["Desenho misto", "Uma corrida com 1 e outra com 2",
                     "Erro: r\u00e9plicas desbalanceadas"]],
                   [CW * 0.30, CW * 0.38, CW * 0.32]))
    s += bullets([
        "S\u00e3o necess\u00e1rias <b>duas corridas independentes</b> no m\u00ednimo; "
        "abaixo disso a ferramenta bloqueia o c\u00e1lculo.",
        "As linhas entram pelo <b>\u201c+\u201d</b> no fim da tabela. Para o desenho em "
        "duplicata, use <b>\u201cAdicionar r\u00e9plica da \u00faltima linha\u201d</b>: ela "
        "copia grupo, data, corrida, analista, equipamento e lote e incrementa a r\u00e9plica.",
        "Os campos Analista, Equipamento, Lote e Corrida t\u00eam <b>listas de "
        "sugest\u00e3o</b> com o que j\u00e1 foi digitado \u2014 evita redigitar e criar "
        "grupos diferentes por erro de digita\u00e7\u00e3o.",
    ])
    s.append(Paragraph("O que significa \u201cgrupo\u201d", S["H2"]))
    s.append(P("O grupo \u00e9 o <b>mesmo material de controle, na matriz do ensaio, na mesma "
               "concentra\u00e7\u00e3o</b>. O nome \u00e9 um r\u00f3tulo curto: <i>tipo do "
               "material + concentra\u00e7\u00e3o</i>. Como a matriz \u00e9 sempre a mesma "
               "(\u00e1gua, neste m\u00e9todo), ela n\u00e3o se repete no nome; o n\u00edvel "
               "j\u00e1 est\u00e1 na concentra\u00e7\u00e3o. Use a concentra\u00e7\u00e3o mais "
               "pr\u00f3xima das amostras que voc\u00ea reporta, porque no or\u00e7amento o "
               "s\u1d62\u209a entra como s\u1d62\u209a \u00d7 y / m\u00e9dia."))
    s.append(table(["Exemplo de grupo", "Quando usar", "O que entra no c\u00e1lculo"],
                   [["CTRL-NO\u2082\u207b 0,85 mg/L",
                     "o controle interno de nitrito, medido de novo todo m\u00eas \u2014 "
                     "\u00e9 o grupo do exemplo carregado na ferramenta",
                     "as prepara\u00e7\u00f5es independentes do controle (sIP)"],
                    ["CHECK-NO\u2082\u207b 0,80 mg/L",
                     "o check de origem independente relido todo m\u00eas \u2014 ele passa a "
                     "ser o controle natural",
                     "as leituras do check (sIP e vi\u00e9s)"],
                    ["CTRL-NO\u2082\u207b 0,20 mg/L",
                     "o mesmo controle, em outro n\u00edvel de concentra\u00e7\u00e3o",
                     "outro grupo: o estudo \u00e9 recalculado por n\u00edvel"],
                    ["FORT-NO\u2082\u207b 0,85 mg/L",
                     "fortifica\u00e7\u00e3o no n\u00edvel das amostras",
                     "as recupera\u00e7\u00f5es do estudo de fortifica\u00e7\u00e3o"]],
                   [CW * 0.42, CW * 0.30, CW * 0.28]))
    s.append(P("<b>O que significam os prefixos:</b> <b>CTRL</b> = controle interno do "
               "laborat\u00f3rio; <b>CHECK</b> = material de verifica\u00e7\u00e3o de origem "
               "independente, que responde pelo vi\u00e9s e completa o sIP "
               "(<b>CHECK-NO\u2082\u207b-2026-019</b> \u00e9 o n\u00famero do certificado, n\u00e3o "
               "o nome do grupo); <b>FORT</b> = fortifica\u00e7\u00e3o do estudo de "
               "recupera\u00e7\u00e3o. O analito aparece pela f\u00f3rmula \u2014 "
               "<b>NO\u2082\u207b</b> \u2014 e n\u00e3o por sigla."))
    s.append(callout("atencao",
                     "O nome do grupo tem de ser <b>id\u00eantico</b> em todas as linhas e no "
                     "campo Grupo do controle: uma letra diferente e a linha \u00e9 ignorada no "
                     "c\u00e1lculo. O c\u00f3digo da corrida tamb\u00e9m \u00e9 gerado automaticamente da data + analista: outro dia ou outra curva geram código novo."))
    s.append(P("<b>Corrida automática (sempre ativa):</b> o código da coluna Corrida é gerado "
               "pelo aplicativo da <b>Data</b> e do <b>Analista</b>, no padrão "
               "<b>ANA_dia+mês+ano NO2- iniciais</b> — 5 de janeiro de 2026 com Carlos Eduardo → "
               "<b>ANA_05JAN26 NO2- CE</b>. O mês sai em três letras (JAN, FEV, MAI, DEZ…), as "
               "iniciais vêm de todas as palavras do nome e <i>Eduardo (CE)</i> força a sigla do "
               "apelido. O campo é somente leitura: duas sessões no mesmo dia, com o mesmo analista "
               "e a mesma preparação recebem os sufixos <b>s2</b>, <b>s3</b>…, e códigos digitados "
               "manualmente (importações antigas ou identificação própria do laboratório) são "
               "preservados."))
    s.append(Paragraph("Como o sIP \u00e9 calculado", S["H2"]))
    s += bullets([
        "<b>Uma observa\u00e7\u00e3o por corrida:</b> usa-se o desvio-padr\u00e3o amostral s dos "
        "resultados independentes.",
        "<b>R\u00e9plicas balanceadas (m por corrida):</b> usa-se ANOVA de efeitos aleat\u00f3rios, "
        "separando a vari\u00e2ncia dentro e entre corridas.",
        "<b>R\u00e9plicas desbalanceadas:</b> gera erro \u2014 o componente de vari\u00e2ncia "
        "precisa ser avaliado fora da ferramenta.",
        "S\u00e3o necess\u00e1rias <b>pelo menos duas corridas independentes</b>.",
    ])
    s.append(formula([
        "s<sub>IP</sub>: 1 obs/corrida \u2192 s amostral   |   r\u00e9plicas balanceadas (m):",
        "s<sub>IP</sub> = \u221a[ MS<sub>dentro</sub> + max(0, (MS<sub>entre</sub> \u2212 MS<sub>dentro</sub>)/m) ]",
        "RSD = 100 \u00b7 s<sub>IP</sub> / |m\u00e9dia|        u<sub>precis\u00e3o</sub>(y) = |y| "
        "\u00b7 s<sub>IP</sub> / |m\u00e9dia|",
    ]))
    s.append(Paragraph("O que a ferramenta avisa (sem bloquear)", S["H2"]))
    s.append(table(["Aviso", "Quando aparece", "O que fazer"],
                   [["Hist\u00f3rico curto", "Poucos resultados no grupo",
                     "Ampliar a s\u00e9rie; n\u00e3o \u00e9 m\u00ednimo prescrito pela ISO 17025"],
                    ["Um \u00fanico dia", "Todos os resultados na mesma data",
                     "Incluir dias diferentes para captar a varia\u00e7\u00e3o entre dias"],
                    ["Dados incompletos", "Falta data, corrida, analista, equipamento, lote ou "
                     "r\u00e9plica", "Completar a linha: qualquer campo faltante invalida o grupo"],
                    ["R\u00e9plica duplicada", "Mesma data + corrida + r\u00e9plica repetidas",
                     "Corrigir a identifica\u00e7\u00e3o da r\u00e9plica"]],
                   [CW * 0.20, CW * 0.40, CW * 0.40]))
    s.append(Spacer(1, 4))
    s.append(callout("ok",
                     "Deixe a varia\u00e7\u00e3o acontecer: um hist\u00f3rico com v\u00e1rios analistas, "
                     "equipamentos e dias representa melhor a precis\u00e3o intermedi\u00e1ria real "
                     "do laborat\u00f3rio."))
    s.append(PageBreak())
    return s


# ================================================================ 7. ETAPA 04
def ch7():
    s = [Paragraph("7. Etapa 04 \u00b7 Check independente e recupera\u00e7\u00e3o", S["H1"])]
    s.append(P("O check \u00e9 um material de valor conhecido e <b>origem independente</b> do "
               "padr\u00e3o de calibra\u00e7\u00e3o. A diferen\u00e7a entre o valor medido e o "
               "designado revela o <b>vi\u00e9s</b>; a incerteza do check entra na conta do "
               "vi\u00e9s. \u00c9 a abordagem recomendada pelo Nordtest."))
    s += fig_n("fig06_vies_check.png",
               "Vi\u00e9s do exemplo: a m\u00e9dia do check (0,796 mg/L) fica abaixo do valor "
               "designado (0,800 mg/L), resultando em b = \u22120,5%.")
    s.append(Paragraph("Campos desta aba", S["H2"]))
    s.append(table(["Campo", "O que registrar", "Exemplo"],
                   [["Fonte do check (v\u00ednculo)", "Linha de certificado da aba 02 \u2014 "
                     "ou digita\u00e7\u00e3o manual", "CRM-NO\u2082\u207b-2026-014"],
                    ["Valor designado do check", "Concentra\u00e7\u00e3o de refer\u00eancia (C<sub>ref</sub>)",
                     "0,800 mg/L"],
                    ["U do check na concentra\u00e7\u00e3o de uso", "Incerteza expandida do "
                     "certificado do check", "0,0048 mg/L"],
                    ["k do check", "Fator de abrang\u00eancia do check", "2"],
                    ["Certificado / lote do check", "Identifica\u00e7\u00e3o e origem independente",
                     "CHECK-NO\u2082\u207b-2026-019"],
                    ["Validade do check", "Prazo do material", "2027-03-01"],
                    ["Resultados do check", "Um valor por linha (meas. do check)",
                     "10 resultados \u2192 m\u00e9dia 0,796"],
                    ["Recupera\u00e7\u00e3o (fortifica\u00e7\u00e3o)", "Percentuais de recupera\u00e7\u00e3o, "
                     "um por linha", "ex.: 98,0; 98,5; 99,0..."]],
                   [CW * 0.34, CW * 0.40, CW * 0.26]))
    s.append(Paragraph("Fonte do check: v\u00ednculo com a aba 02", S["H2"]))
    s.append(P("O valor designado, o U, o k, o certificado e a validade do check j\u00e1 "
               "existem na aba 02. Para n\u00e3o digitar duas vezes \u2014 e n\u00e3o correr o "
               "risco de os dois lugares divergirem \u2014 escolha a linha no campo "
               "<b>Fonte do check</b>: os campos passam a ser <b>lidos da aba 02</b> e se "
               "atualizam sozinhos quando o certificado muda."))
    s.append(table(["Distribui\u00e7\u00e3o na aba 02", "O que o v\u00ednculo grava",
                    "Equivale a"],
                   [["Normal (U/k)", "U = U do certificado; k = k", "u = U / k"],
                    ["Retangular (\u00b1a)", "U = a; k = \u221a3", "u = a / \u221a3"],
                    ["Resolu\u00e7\u00e3o (r)", "U = r; k = \u221a12", "u = r / \u221a12"]],
                   [CW * 0.32, CW * 0.40, CW * 0.28]))
    s += bullets([
        "<b>V\u00ednculo vivo:</b> editar o certificado na aba 02 recalcula o vi\u00e9s \u2014 "
        "nada \u00e9 copiado \u00e0 m\u00e3o.",
        "<b>Copiar valores para edi\u00e7\u00e3o:</b> leva os valores derivados para os "
        "campos edit\u00e1veis e desfaz o v\u00ednculo (busca pontual).",
        "<b>Preencher leituras do grupo (aba 03):</b> copia uma leitura por linha do grupo "
        "selecionado, mostrando antes o n\u00famero de leituras e a m\u00e9dia.",
        "<b>Sem dupla contagem:</b> a linha vinculada \u00e9 marcada como \u201cJ\u00e1 "
        "incorporada ao estudo\u201d e n\u00e3o entra novamente no or\u00e7amento tipo B.",
        "<b>Unidades:</b> g/L \u00e9 convertido para mg/L na pr\u00e9via; unidade relativa "
        "(%) ou base nitrog\u00eanio (N) <b>bloqueiam</b> o v\u00ednculo com mensagem "
        "explicando o motivo.",
        "Se a linha vinculada for removida, o c\u00e1lculo para com erro expl\u00edcito "
        "\u2014 o problema nunca fica escondido.",
    ])
    s.append(Paragraph("O c\u00e1lculo do vi\u00e9s", S["H2"]))
    s.append(formula([
        "b = (x\u0304<sub>check</sub> \u2212 C<sub>ref</sub>) / C<sub>ref</sub>",
        "u<sub>b,rel</sub> = \u221a[ b\u00b2 + ( s<sub>check</sub> / (\u221an \u00b7 C<sub>ref</sub>) )\u00b2 "
        "+ ( U<sub>ref</sub> / (k<sub>ref</sub> \u00b7 C<sub>ref</sub>) )\u00b2 ]",
        "No exemplo:  b = \u22120,005 \u2192 \u22120,5%   ;   u<sub>b,rel</sub> = 0,683%",
    ]))
    s.append(Paragraph("As duas confirmações obrigatórias", S["H2"]))
    s.append(P("São duas verificações: uma caixa de marcar e um campo identificado. Sem as duas o "
               "cálculo fica bloqueado."))
    s.append(table(["Onde", "O que você confirma", "Mensagem se faltar"],
                   [["Aba 03 — Controle de Qualidade",
                     "estabilidade/comparabilidade do controle no período e origem independente do "
                     "check (caixa única “Premissas confirmadas”; desmarcar exige a justificativa "
                     "técnica do desvio — com ela o cálculo é liberado e o desvio sai como aviso "
                     "na memória de cálculo)",
                     "Confirme as premissas do controle (comparabilidade/estabilidade do período e "
                     "origem independente do check) ou registre a justificativa técnica do desvio."],
                    ["Aba 03 — Controle de Qualidade",
                     "identificação do certificado do check (campo, não caixa)",
                     "Identifique o certificado do check."]],
                   [CW * 0.22, CW * 0.50, CW * 0.28]))
    s.append(Paragraph("Fortifica\u00e7\u00e3o: o que \u00e9 e quando ela entra", S["H2"]))
    s.append(P("Fortificar (\u201cspike\u201d) \u00e9 <b>adicionar uma quantidade conhecida do "
               "analito \u00e0 amostra</b> e medir de novo. Se voc\u00ea adiciona 1,00 mg/L de "
               "nitrito a 50 mL de amostra e mede um aumento de 0,985 mg/L, a recupera\u00e7\u00e3o "
               "foi <b>98,5%</b>: a matriz devolveu 98,5% do que foi adicionado e reteve 1,5%. "
               "A recupera\u00e7\u00e3o serve para medir o <b>efeito de matriz</b> \u2014 aquilo "
               "que o certificado em \u00e1gua pura n\u00e3o mostra."))
    s.append(callout("dica",
                     "<b>N\u00e3o faz fortifica\u00e7\u00e3o no seu laborat\u00f3rio?</b> Este "
                     "bloco inteiro \u00e9 <b>opcional</b>. Deixe os campos de recupera\u00e7\u00e3o "
                     "em branco, mantenha o <i>Incluir efeito residual de matriz</i> desmarcado e "
                     "preencha <b>somente</b> a parte do check independente. O c\u00e1lculo "
                     "continua v\u00e1lido \u2014 a contribui\u00e7\u00e3o de matriz simplesmente "
                     "<b>n\u00e3o existe</b> no or\u00e7amento.",
                     title="VERDADE PR\u00c1TICA"))
    s.append(P("O que muda no resultado, usando os dados do exemplo:"))
    s.append(table(["Or\u00e7amento do exemplo", "Com recupera\u00e7\u00e3o (como no guia)",
                    "Sem recupera\u00e7\u00e3o (o seu caso)"],
                   [["Precis\u00e3o intermedi\u00e1ria", "0,02110 mg/L \u00b7 66,1%",
                     "0,02110 mg/L \u00b7 77,4%"],
                    ["Recupera\u00e7\u00e3o residual de matriz", "0,01396 mg/L \u00b7 28,9%",
                     "\u2014 n\u00e3o entra"],
                    ["Vi\u00e9s do check independente", "0,00581 mg/L \u00b7 5,0%",
                     "0,00581 mg/L \u00b7 7,0%"],
                    ["u<sub>c</sub>", "0,02596 mg/L", "0,02189 mg/L"],
                    ["<b>U = 2 \u00b7 u<sub>c</sub></b>", "<b>0,052 mg/L</b>",
                     "<b>0,044 mg/L</b>"]],
                   [CW * 0.40, CW * 0.30, CW * 0.30], mono_cols=(1, 2)))
    s.append(P("A diferen\u00e7a n\u00e3o \u00e9 um erro: \u00e9 a informa\u00e7\u00e3o que voc\u00ea "
               "tem. Sem o estudo de fortifica\u00e7\u00e3o, o <b>efeito de matriz fica fora do "
               "or\u00e7amento</b> e o U fica menor. O caminho correto \u00e9 declarar isso na "
               "mem\u00f3ria de c\u00e1lculo \u2014 por exemplo: \u201cestudo de recupera\u00e7\u00e3o "
               "por fortifica\u00e7\u00e3o n\u00e3o realizado; efeito de matriz n\u00e3o avaliado "
               "separadamente\u201d \u2014 e registrar que o vi\u00e9s medido com o check cobre a "
               "escala da curva e o preparo de rotina."))
    s.append(callout("atencao",
                     "Omitir a recupera\u00e7\u00e3o <b>sem declarar a limita\u00e7\u00e3o</b> "
                     "\u00e9 o que n\u00e3o se deve fazer: o resultado parecer\u00e1 mais exato do "
                     "que o laborat\u00f3rio consegue demonstrar. A fortifica\u00e7\u00e3o passa a "
                     "ser recomendada quando a matriz das amostras \u00e9 agressiva (efluente, "
                     "turbidez alta, sulfeto, cloro residual) ou quando a valida\u00e7\u00e3o do "
                     "m\u00e9todo j\u00e1 exige recupera\u00e7\u00e3o."))
    s.append(Paragraph("Recupera\u00e7\u00e3o residual de matriz", S["H2"]))
    s.append(P("A recupera\u00e7\u00e3o s\u00f3 entra no or\u00e7amento como <b>efeito residual de "
               "matriz</b>, quando justificada e independente. \u00c9 preciso informar a "
               "incerteza da fortifica\u00e7\u00e3o e sua origem. A dispers\u00e3o da recupera\u00e7\u00e3o "
               "n\u00e3o deve ser somada novamente \u00e0 precis\u00e3o."))
    s.append(formula([
        "u<sub>R,rel</sub> = \u221a[ (R\u0304/100 \u2212 1)\u00b2 + ( s<sub>R</sub> / (100\u221an) )\u00b2 "
        "+ u<sub>fort,rel</sub>\u00b2 ]",
        "No exemplo:  R\u0304 = 98,5%  \u2192  u<sub>R,rel</sub> = 1,643%",
    ]))
    s.append(callout("erro",
                     "A recupera\u00e7\u00e3o s\u00f3 pode ser adicionada como <b>efeito residual</b> e "
                     "precisa de justificativa. Sem isso, a ferramenta bloqueia com mensagem de "
                     "dupla contagem e exige a origem da incerteza da fortifica\u00e7\u00e3o."))
    s.append(callout("dica",
                     "Quantas leituras do check: a ferramenta exige <b>duas</b> (abaixo "
                     "disso \u00e9 erro) e avisa quando h\u00e1 <b>menos de cinco</b>. A meta "
                     "pr\u00e1tica \u00e9 <b>6 a 10</b> leituras independentes, espalhadas em "
                     "dias e condi\u00e7\u00f5es diferentes. Uma leitura por m\u00eas \u00e9 "
                     "v\u00e1lida: o aviso desaparece a partir da quinta."))
    s.append(PageBreak())
    return s


# ================================================================ 8. ETAPA 05
def ch8():
    s = [Paragraph("8. Etapa 05 \u00b7 Or\u00e7amento de incerteza", S["H1"])]
    s.append(P("O or\u00e7amento \u00e9 o cora\u00e7\u00e3o do c\u00e1lculo: ele re\u00fane todas as "
               "contribui\u00e7\u00f5es e mostra <b>quem domina</b> o resultado. Esta aba \u00e9 "
               "somente leitura \u2014 voc\u00ea n\u00e3o digita aqui, apenas confere."))
    s.append(Paragraph("Como ler cada coluna", S["H2"]))
    s.append(table(["Coluna", "Significado", "Como interpretar"],
                   [["Fonte / tipo", "Origem da contribui\u00e7\u00e3o e sua natureza "
                     "(tipo A ou A/B)", "O nome vem das abas anteriores"],
                    ["Valor de entrada", "O dado usado no c\u00e1lculo", "Confira unidade e ordem "
                     "de grandeza"],
                    ["Distribui\u00e7\u00e3o / divisor", "Como a entrada foi convertida",
                     "Normal, estat\u00edstica, vi\u00e9s + estat\u00edstica..."],
                    ["u(x)", "Incerteza-padr\u00e3o da fonte", "Sempre maior que zero e finita"],
                    ["c\u1d62", "Coeficiente de sensibilidade", "Quanto o resultado varia por "
                     "unidade de x"],
                    ["|c\u1d62 u(x)| mg/L", "Contribui\u00e7\u00e3o efetiva ao resultado",
                     "Estas s\u00e3o as barras compar\u00e1veis"],
                    ["Participa\u00e7\u00e3o", "Fra\u00e7\u00e3o da <b>vari\u00e2ncia</b> total",
                     "Soma 100%; n\u00e3o \u00e9 fra\u00e7\u00e3o linear de U"]],
                   [CW * 0.22, CW * 0.40, CW * 0.38]))
    s += fig_n("fig07_orcamento_barras.png",
               "Or\u00e7amento do exemplo: a precis\u00e3o intermedi\u00e1ria responde por 66% da "
               "vari\u00e2ncia, a recupera\u00e7\u00e3o residual por 29% e o vi\u00e9s por 5%.",
               max_h=7.2 * cm)
    s.append(Paragraph("A regra de ouro da melhoria", S["H2"]))
    s.append(P("Para reduzir a incerteza do resultado, ataque a fonte que <b>domina</b> a "
               "participa\u00e7\u00e3o. Reduzir uma fonte que j\u00e1 \u00e9 pequena quase n\u00e3o muda U, "
               "porque as contribui\u00e7\u00f5es se combinam em quadratura."))
    s += bullets([
        "Se a precis\u00e3o domina: padronize a execu\u00e7\u00e3o, reveja a prepara\u00e7\u00e3o e o "
        "controle do material.",
        "Se a recupera\u00e7\u00e3o/vi\u00e9s domina: revise a calibra\u00e7\u00e3o, o padr\u00e3o e a "
        "matriz de refer\u00eancia.",
        "Se um certificado domina: ele \u00e9 o gargalo \u2014 considere um padr\u00e3o ou "
        "instrumento de maior exatid\u00e3o.",
    ])
    s.append(callout("nota",
                     "As contribui\u00e7\u00f5es s\u00e3o combinadas por "
                     "u<sub>c</sub> = \u221a\u03a3(c\u1d62\u00b7u)\u00b2. Uma fonte com metade da "
                     "contribui\u00e7\u00e3o da dominante pesa apenas 0,25 da vari\u00e2ncia dela."))
    s.append(callout("atencao",
                     "Se aparecer <b>FD \u2260 1</b>, verifique se a dilui\u00e7\u00e3o adicional "
                     "est\u00e1 coberta pelo estudo ou se precisa entrar como contribui\u00e7\u00e3o "
                     "independente."))
    s.append(PageBreak())
    return s


# ================================================================ 9. ETAPA 06
def ch9():
    s = [Paragraph("9. Etapa 06 \u00b7 Resultado e regra de decis\u00e3o", S["H1"])]
    s.append(P("O painel de resultado expressa <b>y \u00b1 U</b> na unidade do ensaio e, quando "
               "houver limite de conformidade, aplica a regra declarada. O fator k e o modo de "
               "decis\u00e3o s\u00e3o escolhas suas."))
    s.append(Paragraph("Campos desta aba", S["H2"]))
    s.append(table(["Campo", "O que \u00e9", "Exemplo"],
                   [["Fator k", "Fator de abrang\u00eancia declarado pelo usu\u00e1rio", "2"],
                    ["Modo de decis\u00e3o", "Sem declara\u00e7\u00e3o / limite superior (L)",
                     "Sem declara\u00e7\u00e3o de conformidade"],
                    ["Limite superior L", "Valor m\u00e1ximo admiss\u00edvel (se houver)",
                     "n\u00e3o informado no exemplo"],
                    ["Acordo / base da regra", "Documento que fundamenta a regra de decis\u00e3o",
                     "obrigat\u00f3rio quando h\u00e1 limite L"]],
                   [CW * 0.26, CW * 0.46, CW * 0.28]))
    s += fig_n("fig08_resultado_bandas.png",
               "Os tr\u00eas desfechos poss\u00edveis da regra y + U \u2264 L, com o exemplo "
               "y = 0,850 e U = 0,052.")
    s.append(Paragraph("As tr\u00eas conclus\u00f5es poss\u00edveis", S["H2"]))
    s.append(table(["Condi\u00e7\u00e3o", "Mensagem da ferramenta", "Leitura"],
                   [["y + U \u2264 L", "Conforme pela regra y + U \u2264 L.",
                     "Todo o intervalo est\u00e1 abaixo do limite"],
                    ["y \u2212 U > L", "N\u00e3o conforme: todo o intervalo est\u00e1 acima de L.",
                     "Nenhuma incerteza salva o resultado"],
                    ["Caso contr\u00e1rio", "Conformidade n\u00e3o demonstrada: o intervalo "
                     "sobrep\u00f5e o limite.", "Decis\u00e3o depende do risco acordado"]],
                   [CW * 0.20, CW * 0.44, CW * 0.36]))
    s.append(Spacer(1, 5))
    s.append(Paragraph("Arredondamento do resultado", S["H2"]))
    s.append(P("A ferramenta arredonda U para um n\u00famero de decimais coerente com sua "
               "magnitude e apresenta y com o mesmo n\u00famero de casas. No exemplo, "
               "U = 0,05192 \u2192 0,052, e o resultado aparece como "
               "<b>0,850 \u00b1 0,052 mg/L de NO\u2082\u207b</b>."))
    s.append(callout("atencao",
                     "Ao informar um limite L, o texto de <b>acordo / base da regra de "
                     "decis\u00e3o</b> passa a ser obrigat\u00f3rio \u2014 a ferramenta exige a base "
                     "documental antes de concluir conformidade."))
    s.append(callout("ok",
                     "Registre no pr\u00f3prio estudo quem definiu a regra de decis\u00e3o e por "
                     "qu\u00ea. Isso torna a mem\u00f3ria de c\u00e1lculo audit\u00e1vel, e n\u00e3o apenas "
                     "aritm\u00e9tica."))
    s.append(PageBreak())
    return s


# ================================================================ 10. EXEMPLO
def ch10():
    s = [Paragraph("10. Exemplo resolvido de ponta a ponta", S["H1"])]
    s.append(P("Este cap\u00edtulo percorre o <b>estudo fict\u00edcio</b> que acompanha a "
               "calculadora: nitrito em \u00e1gua, controle est\u00e1vel, sem dilui\u00e7\u00e3o. "
               "Acompanhe o caminho dos dados entre as abas e confira as contas."))
    s += fig_n("fig09_fluxo_dados.png",
               "Do hist\u00f3rico \u00e0 decis\u00e3o: o que cada aba entrega para a seguinte, e as "
               "quatro vias que alimentam o or\u00e7amento.")
    s.append(Paragraph("Dados de entrada, consolidados", S["H2"]))
    s.append(table(["Aba", "Dado", "Valor do exemplo"],
                   [["01", "C<sub>leitura</sub> \u00b7 FD \u00b7 faixa",
                     "0,850 mg/L \u00b7 1 \u00b7 0,05\u20132 mg/L"],
                    ["02", "Padr\u00e3o de nitrito (U, k, distribui\u00e7\u00e3o)",
                     "1,0 mg/L, k = 2, normal \u2192 0,5 mg/L"],
                    ["02", "Bal\u00e3o 100 mL \u00b7 pipetador 10 mL",
                     "\u00b10,2 mL \u00b7 \u00b10,05 mL, k = 2 \u2192 0,1 / 0,025 mL"],
                    ["02", "Espectrofot\u00f4metro (abs)",
                     "\u00b10,002 abs, k = 2 \u2192 0,001 abs"],
                    ["03", "Hist\u00f3rico do controle",
                     "0,846 mg/L m\u00e9dia \u00b7 s<sub>IP</sub> = 0,021 mg/L \u00b7 RSD = 2,48%"],
                    ["04", "Check independente",
                     "C<sub>ref</sub> = 0,800 mg/L \u00b7 U = 0,0048 \u00b7 k = 2 \u00b7 "
                     "x\u0304 = 0,796"],
                    ["04", "Recupera\u00e7\u00e3o (fortifica\u00e7\u00e3o)",
                     "R\u0304 = 98,5% \u00b7 s = 1,9% \u00b7 n = 10 \u00b7 u<sub>fort</sub> = 0,3%"],
                    ["06", "Regra de decis\u00e3o", "sem limite L \u00b7 k declarado = 2"]],
                   [CW * 0.09, CW * 0.42, CW * 0.49], mono_cols=(2,)))
    s.append(Paragraph("O que a ferramenta faz com esses dados", S["H2"]))
    s += bullets([
        "<b>Padroniza</b> cada entrada tipo B (u(x) = U/k, a/\u221a3 ou r/\u221a12).",
        "<b>Calcula</b> o s<sub>IP</sub> do hist\u00f3rico e o converte em contribui\u00e7\u00e3o "
        "relativa ao resultado.",
        "<b>Estima</b> o vi\u00e9s do check e a recupera\u00e7\u00e3o residual.",
        "<b>Combina</b> tudo em quadratura no or\u00e7amento e expande por k = 2.",
    ])
    s.append(Paragraph("Contas do exemplo, passo a passo", S["H2"]))
    s.append(table(["Contribui\u00e7\u00e3o", "C\u00e1lculo", "Resultado", "Participa\u00e7\u00e3o"],
                   [["Precis\u00e3o intermedi\u00e1ria",
                     "u = 0,850 \u00b7 0,021 / 0,846", "0,02110 mg/L", "66,1%"],
                    ["Recupera\u00e7\u00e3o residual",
                     "\u221a[(0,985\u22121)\u00b2 + (1,9/(100\u221a10))\u00b2 + 0,003\u00b2]",
                     "0,01643 \u00b7 0,850 = 0,01396 mg/L", "28,9%"],
                    ["Vi\u00e9s do check",
                     "\u221a[(0,005)\u00b2 + (s/(\u221an\u00b7C<sub>ref</sub>))\u00b2 + (U/(k\u00b7C<sub>ref</sub>))\u00b2]",
                     "0,00683 \u00b7 0,850 = 0,00581 mg/L", "5,0%"],
                    ["Incerteza combinada u<sub>c</sub>",
                     "\u221a(0,02110\u00b2 + 0,01396\u00b2 + 0,00581\u00b2)", "0,02596 mg/L",
                     "100%"],
                    ["Incerteza expandida U",
                     "2 \u00b7 0,02596", "<b>0,05192 mg/L</b>", "\u2014"]],
                   [CW * 0.25, CW * 0.38, CW * 0.22, CW * 0.15], mono_cols=(2, 3)))
    # CH10_PART2
    s.append(Paragraph("Resultado e leitura final", S["H2"]))
    s.append(formula([
        "u<sub>c</sub>(y) = 0,02596 mg/L      U = 2 \u00b7 u<sub>c</sub> = 0,05192 mg/L",
        "y \u00b1 U = 0,850 \u00b1 0,052 mg/L de NO\u2082\u207b      (k = 2, ~95%)",
        "Sem limite L: nenhuma declara\u00e7\u00e3o de conformidade \u00e9 emitida.",
    ]))
    s += fig_n("memoria_orcamento_p5.png",
               "Bloco 5 da mem\u00f3ria de c\u00e1lculo: fonte, valor de "
               "entrada, distribui\u00e7\u00e3o/divisor, u(x), coeficiente de "
               "sensibilidade e participa\u00e7\u00e3o.", max_h=8.6 * cm)
    s += fig_n("memoria_resultado_p1.png",
               "Fechamento do resultado: incerteza combinada, fator k declarado e texto de "
               "decis\u00e3o.", max_h=7.2 * cm)
    s.append(Paragraph("Confer\u00eancia em oito pontos", S["H2"]))
    s.append(table(["#", "O que conferir", "Crit\u00e9rio de aceite"],
                   [["1", "C<sub>leitura</sub> dentro da faixa de trabalho", "0,850 dentro de 0,05\u20132 mg/L"],
                    ["2", "Unidade do resultado", "mg/L de NO\u2082\u207b em todas as abas"],
                    ["3", "Certificados e validade", "Todos com lote/prazo informados"],
                    ["4", "Tratamentos", "Nenhuma dupla contagem; justificativa preenchida"],
                    ["5", "Hist\u00f3rico do controle", ">= 2 corridas independentes, "
                     "campos completos"],
                    ["6", "Check independente", ">= 5 medi\u00e7\u00f5es (sen\u00e3o, aviso)"],
                    ["7", "Recupera\u00e7\u00e3o (se houver fortifica\u00e7\u00e3o)",
                     "Somente como efeito residual, com origem; sem fortifica\u00e7\u00e3o, "
                     "deixar em branco e declarar a limita\u00e7\u00e3o"],
                    ["8", "Regra de decis\u00e3o", "Limite e base documental coerentes"]],
                   [CW * 0.05, CW * 0.45, CW * 0.50]))
    s.append(callout("ok",
                     "Reproduza estas contas com os seus pr\u00f3prios dados e compare com a "
                     "ferramenta: enquanto os valores baterem, voc\u00ea est\u00e1 preenchendo "
                     "corretamente e j\u00e1 sabe onde est\u00e1 a maior contribui\u00e7\u00e3o."))
    s.append(PageBreak())
    return s





# ================================================================ APÊNDICES
def ch_appendix():
    s = [Paragraph("Ap\u00eandices \u00b7 checklists e refer\u00eancias r\u00e1pidas", S["H1"])]
    s.append(Paragraph("A. Checklist de preenchimento (todas as abas)", S["H2"]))
    s.append(table(["Aba", "Antes de avan\u00e7ar, confirme que..."],
                   [["01 \u00b7 Identifica\u00e7\u00e3o",
                     "Estudo, m\u00e9todo, matriz, faixa, C<sub>leitura</sub>, FD, respons\u00e1vel, "
                     "data e vers\u00e3o est\u00e3o preenchidos; a leitura est\u00e1 na faixa."],
                    ["02 \u00b7 Padr\u00f5es e equipamentos",
                     "Cada fonte tem certificado, validade, unidade, U/\u00b1a/r, k, "
                     "distribui\u00e7\u00e3o, tratamento e (quando inclu\u00edda) justificativa."],
                    ["03 \u00b7 Precis\u00e3o",
                     "Grupo com >= 2 corridas independentes; data, corrida, analista, "
                     "equipamento, lote e r\u00e9plica completos."],
                    ["04 \u00b7 Check e recupera\u00e7\u00e3o",
                     "C<sub>ref</sub>, U e k do check; >= 5 medi\u00e7\u00f5es; as tr\u00eas "
                     "confirma\u00e7\u00f5es marcadas; recupera\u00e7\u00e3o s\u00f3 como residual."],
                    ["05 \u00b7 Or\u00e7amento",
                     "Nenhuma contribui\u00e7\u00e3o zerada por engano; participa\u00e7\u00e3o soma "
                     "100%; voc\u00ea sabe qual fonte domina."],
                    ["06 \u00b7 Resultado",
                     "k coerente com a pol\u00edtica; limite L e base documental preenchidos se "
                     "houver declara\u00e7\u00e3o de conformidade."]],
                   [CW * 0.26, CW * 0.74], pad=4))
    s.append(Spacer(1, 4))
    s.append(Paragraph("B. Gloss\u00e1rio m\u00ednimo", S["H2"]))
    s.append(table(["Termo", "Defini\u00e7\u00e3o curta"],
                   [["Tipo A", "Contribui\u00e7\u00e3o avaliada por estat\u00edstica de resultados "
                     "repetidos (ex.: precis\u00e3o)."],
                    ["Tipo B", "Contribui\u00e7\u00e3o avaliada por certificado, especifica\u00e7\u00e3o "
                     "ou conhecimento t\u00e9cnico (ex.: padr\u00e3o, vidraria)."],
                    ["u(x)", "Incerteza-padr\u00e3o da fonte, na unidade da fonte."],
                    ["c\u1d62", "Coeficiente de sensibilidade: quanto y varia por unidade de x."],
                    ["u<sub>c</sub>(y)", "Incerteza combinada do resultado."],
                    ["U", "Incerteza expandida: U = k \u00b7 u<sub>c</sub>."],
                    ["k", "Fator de abrang\u00eancia (2 \u2248 95% em distribui\u00e7\u00e3o normal)."],
                    ["s<sub>IP</sub>", "Desvio-padr\u00e3o da precis\u00e3o intermedi\u00e1ria."],
                    ["Vi\u00e9s (b)", "Desvio sistem\u00e1tico relativo revelado pelo check."],
                    ["FD", "Fator de dilui\u00e7\u00e3o aplicado \u00e0 amostra."]],
                   [CW * 0.18, CW * 0.82], pad=4))
    s.append(Spacer(1, 4))
    s.append(Paragraph("C. Refer\u00eancias usadas na mem\u00f3ria de c\u00e1lculo", S["H2"]))
    s += bullets([
        "<b>ISO/IEC 17025</b> \u2014 itens 7.6 (avalia\u00e7\u00e3o da incerteza), 7.7 "
        "(garantia da validade) e 7.8 (relato de conformidade e regra de decis\u00e3o).",
        "<b>Guia Eurachem/CITAC</b> \u2014 quantifica\u00e7\u00e3o da incerteza em medi\u00e7\u00f5es "
        "anal\u00edticas (or\u00e7amento, tipo A/tipo B, sensibilidade).",
        "<b>Abordagem Nordtest (TR 537)</b> \u2014 vi\u00e9s e precis\u00e3o intermedi\u00e1ria a "
        "partir de material de controle e check independente.",
        "<b>GUM / JCGM 100</b> \u2014 propaga\u00e7\u00e3o de incertezas e fator de abrang\u00eancia.",
    ])
    s.append(Spacer(1, 4))
    s.append(Paragraph("D. Fechamento e arquivamento do estudo", S["H2"]))
    s += bullets([
        "Exporte o <b>JSON</b> do estudo: \u00e9 ele que guarda o formul\u00e1rio completo "
        "para retomar o trabalho depois.",
        "Anexe os <b>CSV</b> (mensal e or\u00e7amento) \u00e0 mem\u00f3ria de c\u00e1lculo "
        "assinada \u2014 eles mostram de onde vem cada contribui\u00e7\u00e3o.",
        "Arquive a <b>mem\u00f3ria (PDF)</b> junto dos certificados citados (padr\u00e3o, check, "
        "vidraria) e do hist\u00f3rico de controle usado.",
        "Registre a <b>data de revis\u00e3o</b>: mudou padr\u00e3o, lote do controle, analista "
        "ou equipamento, refa\u00e7a a avalia\u00e7\u00e3o.",
    ])
    s.append(callout("ok",
                     "Na pr\u00f3xima revis\u00e3o, comece pela aba 05: se a fonte que domina "
                     "o or\u00e7amento mudou, algo mudou no processo \u2014 e a mem\u00f3ria de "
                     "c\u00e1lculo precisa ser atualizada."))

    s.append(callout("nota",
                     "Este guia \u00e9 material de treinamento: ele explica a ferramenta, mas a "
                     "responsabilidade t\u00e9cnica pela mem\u00f3ria de c\u00e1lculo \u2014 escolha das "
                     "distribui\u00e7\u00f5es, tratamentos e regra de decis\u00e3o \u2014 \u00e9 sempre do "
                     "laborat\u00f3rio."))
    return s


# ================================================================ MONTAGEM
# Espaco minimo (cm) que precisa sobrar na pagina para o capitulo comecar ali.
# Se sobrar menos que isso, o capitulo abre em pagina nova; se sobrar mais, ele
# aproveita o espaco e o guia flui sem paginas quase vazias.
MIN_SPACE = {
    "ch1": 5.4, "ch2": 5.4, "ch3": 5.4, "ch4": 5.4, "ch5": 5.4, "ch6": 5.4,
    "ch7": 5.4, "ch8": 5.4, "ch9": 5.4, "ch10": 5.4, "ch_appendix": 5.4,
}


def build_story():
    story = []
    story += ch_cover()
    for fn in (ch_toc, ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8, ch9, ch10, ch_appendix):
        blocks = fn()
        while blocks and isinstance(blocks[-1], PageBreak):
            blocks.pop()   # o corte entre secoes passa a ser condicional
        story.append(CondPageBreak(MIN_SPACE.get(fn.__name__, 10) * cm))
        story += blocks
    return story


def main():
    doc = make_doc()
    doc.multiBuild(build_story())
    print("PDF gerado:", OUT)


if __name__ == "__main__":
    main()
