#!/usr/bin/env python3
"""Verifica que todos los assets referenciados en index.html existan en disco."""
import re, os, sys

try:
    html = open('index.html', encoding='utf-8').read()
except FileNotFoundError:
    sys.exit(0)

paths = set()
paths |= set(re.findall(r"url\('(materiales/[^']+\.(?:png|jpg|jpeg|pdf|webp))'\)", html, re.I))
paths |= set(re.findall(r"'(materiales/[^']+\.(?:png|jpg|jpeg|pdf|webp))'", html, re.I))

missing = [p for p in sorted(paths) if not os.path.exists(p)]

if missing:
    print('\n⚠️  Assets no encontrados en disco (rutas rotas):')
    for p in missing:
        print('   ✗ ' + p)
    print()
else:
    print(f'✓ {len(paths)} assets verificados — todas las rutas OK')
