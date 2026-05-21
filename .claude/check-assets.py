#!/usr/bin/env python3
"""Verifica que todos los assets referenciados en index.html y _data/categorias/*.json existan en disco."""
import re, os, sys, glob

paths = set()

if os.path.exists('index.html'):
    html = open('index.html', encoding='utf-8').read()
    paths |= set(re.findall(r"url\('(materiales/[^']+\.(?:png|jpg|jpeg|pdf|webp))'\)", html, re.I))
    paths |= set(re.findall(r"'(materiales/[^']+\.(?:png|jpg|jpeg|pdf|webp))'", html, re.I))

for jf in glob.glob('_data/categorias/*.json'):
    text = open(jf, encoding='utf-8').read()
    paths |= set(re.findall(r'"(materiales/[^"]+\.(?:png|jpg|jpeg|pdf|webp))"', text, re.I))

missing = [p for p in sorted(paths) if not os.path.exists(p)]

if missing:
    print('\n⚠️  Assets no encontrados en disco (rutas rotas):')
    for p in missing:
        print('   ✗ ' + p)
    print()
else:
    print(f'✓ {len(paths)} assets verificados — todas las rutas OK')
