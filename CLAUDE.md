# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Proyecto

Sitio web estático de materiales educativos de la profesora Vanessa, publicado en profvanessa.cl via GitHub Pages. No hay framework, build system ni dependencias: todo es HTML/CSS/JS en un único archivo `index.html`.

## Comandos

```bash
# Servidor local de desarrollo
python3 -m http.server 8000       # → http://localhost:8000

# Verificar que todos los assets referenciados en index.html existen en disco
python3 .claude/check-assets.py

# Deploy — un push a main publica en ~1 minuto via GitHub Pages
git push
```

No hay linter, tests ni build. El hook `PostToolUse` corre `check-assets.py` automáticamente después de cada Edit/Write al `index.html`.

## Arquitectura

### `index.html` (todo el sitio, ~2100 líneas)

El archivo tiene 3 secciones bien delimitadas:

1. **`<style>`** — Todo el CSS inline. Variables de color en `:root`. Tipografía: Playfair Display (títulos) + Nunito (cuerpo), ambas de Google Fonts.

2. **HTML** — Secciones en orden: `nav`, `#inicio` (hero), `#recursos` (cards de categorías), `#about`, `#videos` (YouTube embeds), `#contacto`, `footer`. Más 4 overlays: modal de productos, lightbox de preview, video overlay, formulario de testimonio.

3. **`<script>`** — Toda la lógica inline. El objeto clave es `categorias` (hacia el final del script), que contiene todos los productos del catálogo.

### Objeto `categorias`

```js
const categorias = {
  guias: { icono, titulo, subtitulo, productos: [] },
  presentaciones: { ..., productos: [ { nombre, descripcion, detalle, precio, formato, thumbnail, previews, link, videoYoutube?, destacado?, thumbnailStack?, precioOriginal?, etiquetaDestacado? } ] },
  pruebas: { ... },
  tableros: { ... },
  fichas: { ... },
  flashcards: { ... }
};
```

Para agregar o modificar un producto, **siempre editar este objeto**. Los modales se renderizan dinámicamente desde él con `renderProducto()`.

### Hero dinámico

`popularHero()` se ejecuta al cargar y busca el producto con mayor precio en todas las categorías (priorizando `destacado: true` en empates) para mostrarlo en el mockup hero. Al hacer click abre el modal de la categoría y hace scroll al producto con resaltado dorado.

### Funciones JS clave

| Función | Qué hace |
|---|---|
| `abrirModal(id, pushUrl, scrollToIdx)` | Abre el modal de una categoría, opcionalmente hace scroll a un producto |
| `renderProducto(cat, catId, idx, p)` | Genera el HTML de un producto para el modal |
| `encontrarProductoMasCaro()` | Recorre `categorias` y devuelve el producto más caro |
| `abrirPreview(catId, prodIdx)` | Abre el lightbox con las imágenes de preview |
| `abrirVideo(youtubeUrl)` | Abre el overlay de video YouTube |

### Assets

```
materiales/
  presentaciones/<slug>/   ← PNGs de portada y previews, PDFs
  fichas/<slug>/
  tableros/<slug>/
  guias/<slug>/
img/
  vanessa.jpg              ← foto de perfil
  canva-page1.png
```

Convención de nombres: `<slug>-portada.png`, `<slug>-prev1.png`, `<slug>-prev2.png`, ... La última preview siempre se difumina con candado (CSS automático).

## Convenciones importantes

- **Precios**: string con punto como separador de miles (`'13.990'`). La función `encontrarProductoMasCaro()` hace `replace(/\./g, '')` antes de parsear.
- **Formato slide**: agregar `formato: 'slide'` solo en presentaciones Canva/PPT (aplica aspect-ratio 16:9 al thumbnail). Fichas y tableros no llevan `formato`.
- **Packs**: requieren `destacado: true`, `thumbnailStack: [...]`, `precioOriginal`, `etiquetaDestacado`.
- **Categorías vacías**: dejar `productos: []` — el modal muestra "¡Próximamente!" automáticamente.
- **Deploy**: GitHub Pages. Un `git push` a `main` publica en ~1 minuto.

## Skill disponible

Usar `/agregar-producto` para guiar el proceso completo de agregar un material nuevo: recopila info, copia assets desde Windows (`/mnt/c/...`), genera el objeto JS y hace commit+push.
