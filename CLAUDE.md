# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Proyecto

Sitio web estático de materiales educativos de la profesora Vanessa, publicado en **profvanessa.cl vía Netlify**. No hay framework ni build system: HTML/CSS/JS plano. Los productos del catálogo viven en JSONs sueltos en `_data/categorias/` que se cargan dinámicamente vía `fetch`, y Vanessa puede editarlos sin tocar código desde **profvanessa.cl/admin** (Decap CMS + Netlify Identity + Git Gateway).

## Comandos

```bash
# Servidor local de desarrollo
python3 -m http.server 8000       # → http://localhost:8000

# Verificar que todos los assets referenciados existan en disco
# (escanea index.html + _data/categorias/*.json)
python3 .claude/check-assets.py

# Deploy — un push a main publica en Netlify en ~1 minuto
git push
```

No hay linter, tests ni build. El hook `PostToolUse` corre `check-assets.py` automáticamente después de cada Edit/Write a `index.html` o a los JSON de categorías.

## Arquitectura

### Estructura de datos: `_data/categorias/*.json`

Un archivo JSON por categoría. Cada archivo contiene metadata + array de productos:

```json
{
  "id": "presentaciones",
  "orden": 2,
  "icono": "🎨",
  "titulo": "Presentaciones",
  "subtitulo": "Diapositivas en Canva y PowerPoint listas para usar",
  "productos": [
    {
      "nombre": "...",
      "descripcion": "...",
      "detalle": "...",
      "precio": "5.990",
      "formato": "slide",
      "thumbnail": "materiales/<cat>/<slug>/portada.png",
      "previews": [
        { "src": "materiales/<cat>/<slug>/prev1.png" },
        { "src": "materiales/<cat>/<slug>/prev2.png" }
      ],
      "link": "https://pay.hotmart.com/...",
      "videoYoutube": "https://www.youtube.com/watch?v=..."
    }
  ]
}
```

Campos opcionales por producto: `formato` ("slide" para Canva/PPT), `videoYoutube`, `destacado`, `thumbnailStack` (packs), `precioOriginal`, `etiquetaDestacado`.

**Importante**: `previews` y `thumbnailStack` deben ser **listas de objetos `{src: "..."}`** (no strings sueltos). Es el formato que Decap CMS produce con `widget: list` + `field: {widget: image}`. La función `cargarCategorias()` en `index.html` los aplana a `[string]` en memoria, así el resto del código no lo nota.

### `index.html` (~2100 líneas)

Tres secciones:

1. **`<style>`** — CSS inline. Variables en `:root`. Tipografías: Playfair Display + Nunito.
2. **HTML** — `nav`, `#inicio` (hero), `#recursos` (cards), `#about`, `#videos`, `#contacto`, `footer`. + 4 overlays: modal de productos, lightbox preview, video, formulario.
3. **`<script>`** — Toda la lógica. Al cargar la página, `cargarCategorias()` hace fetch en paralelo de los 6 JSONs y arma el objeto `categorias`. Después corre `popularHero()` y abre el modal si el URL tiene hash.

### Funciones JS clave

| Función | Qué hace |
|---|---|
| `cargarCategorias()` | Fetch paralelo de `_data/categorias/*.json` y arma el objeto `categorias` en memoria |
| `abrirModal(id, pushUrl, scrollToIdx)` | Abre el modal de una categoría |
| `renderProducto(cat, catId, idx, p)` | Genera el HTML de un producto |
| `encontrarProductoMasCaro()` | Recorre `categorias` y devuelve el producto más caro (para el hero) |
| `popularHero()` | Coloca el producto más caro en el mockup hero (al cargar) |
| `abrirPreview(catId, prodIdx)` | Lightbox de imágenes preview |
| `abrirVideo(youtubeUrl)` | Overlay de video YouTube |
| `filtrarProductos()` | Filtra el listado del modal por texto/grado |

### Assets

```
materiales/
  presentaciones/<slug>/   ← PNGs de portada y previews
  fichas/<slug>/
  tableros/<slug>/
  guias/<slug>/
img/
  vanessa.jpg              ← foto de perfil
```

Convención de nombres: `<slug>-portada.png`, `<slug>-prev1.png`, ... La última preview se difumina con candado (CSS automático).

### Admin / CMS

- `/admin/index.html` — bootstrap de Decap CMS desde unpkg
- `/admin/config.yml` — define backend (`git-gateway`), media_folder y colecciones
- Una colección de tipo "Files", con un archivo por categoría → cada uno con sus `productos` como list widget (drag-and-drop para reordenar)
- Auth vía Netlify Identity (invitación por email)

## Convenciones importantes

- **Precios**: string con punto como separador de miles (`"13.990"`). `null` si es gratis.
- **Formato slide**: agregar `"formato": "slide"` solo en Canva/PPT (aspect-ratio 16:9). Fichas y tableros no llevan `formato`.
- **Packs**: requieren `"destacado": true`, `"thumbnailStack": [{src: ...}]`, `"precioOriginal"`, `"etiquetaDestacado"`.
- **Categorías vacías**: dejar `"productos": []` — el modal muestra "¡Próximamente!" automáticamente.
- **Deploy**: Netlify. Un `git push` a `main` publica en ~1 minuto.

## Skill disponible

Usar `/agregar-producto` para agregar un material nuevo desde código: recopila info, copia assets desde Windows (`/mnt/c/...`), inserta el objeto al JSON de la categoría y hace commit+push.

Alternativa sin código: Vanessa puede agregar productos sola desde **profvanessa.cl/admin**.
