import os, fitz
doc = fitz.open(r'f:\Transcricoes_Consolidadas\guia_calculadora\tmp\memoria_exemplo.pdf')
out = r'f:\Transcricoes_Consolidadas\guia_calculadora\tmp'
for i in range(doc.page_count):
    pix = doc[i].get_pixmap(dpi=110)
    p = os.path.join(out, f'memoria_p{i+1}.png')
    pix.save(p)
    txt = doc[i].get_text()[:160].replace('\n', ' | ')
    print(i + 1, '->', txt)
doc.close()

