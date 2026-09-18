# -*- coding: utf-8 -*-
"""Gera o guia em um PDF temporario (para conferir layout quando o arquivo final
esta aberto no leitor de PDF). Uso: python guia_calculadora/_preview.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_guia as b

b.OUT = os.path.join(b.HERE, "preview_guia.pdf")
b.main()
print("preview:", b.OUT)
