---
name: agregar-producto
description: Guía el proceso completo de agregar un nuevo material educativo al catálogo de profvanessa.cl — copia assets, agrega el producto al JSON de la categoría y hace commit+push.
---

# Agregar producto a profvanessa.cl

> Vanessa también puede agregar productos sola desde **profvanessa.cl/admin** (Decap CMS). Este skill es para cuando Israel/Claude lo agrega directo por código.

## 1. Recopilar información del producto

Pregunta al usuario uno por uno si no los dio todos de entrada:

- **Categoría**: `guias` | `presentaciones` | `pruebas` | `tableros` | `fichas` | `flashcards`
- **Nombre completo** (ej: "Acto 1: Reparto equitativo de entradas")
- **Descripción corta** (nivel, páginas, asignatura — ej: "4°-5° Básico · 25 páginas · Matemática")
- **Detalle largo** (2-3 frases describiendo qué aprende el alumno y qué incluye)
- **Precio en CLP** sin puntos (ej: 5990) — o `null` si es gratis
- **Link de Hotmart** (ej: https://pay.hotmart.com/XXXXXXX)
- **Ruta Windows de los assets** (ej: `C:\Users\israe\Downloads\NombreCarpeta`)
- **¿Tiene video de YouTube?** (opcional — URL completa)
- **¿Es pack con thumbnailStack?** (opcional — si agrupa varios productos)

## 2. Listar y verificar los assets disponibles

```bash
ls -la "/mnt/c/Users/israe/Downloads/<NombreCarpeta>/"
```

Identifica:
- Archivo de **portada** (PNG/JPG principal)
- **Previews** (screenshots — mínimo 3, máximo 6; la última se difumina con candado)

## 3. Convención de nombres

`<slug>-portada.png`, `<slug>-prev1.png`, ..., `<slug>-prevN.png`

## 4. Copiar y renombrar los assets

Carpeta destino según categoría:
- presentaciones → `materiales/presentaciones/<slug>/`
- fichas → `materiales/fichas/<slug>/`
- tableros → `materiales/tableros/<slug>/`
- guias → `materiales/guias/<slug>/`
- pruebas → `materiales/pruebas/<slug>/`
- flashcards → `materiales/flashcards/<slug>/`

## 5. Agregar el producto al JSON de la categoría

Abre `_data/categorias/<categoria>.json` y agrega un objeto al array `productos`. Cada categoría es **un único archivo JSON** con metadata + array de productos.

Estructura base de un producto:
```json
{
  "nombre": "<nombre>",
  "descripcion": "<descripción corta>",
  "detalle": "<detalle largo>",
  "precio": "<precio con punto como miles, o null si es gratis>",
  "formato": "slide",
  "thumbnail": "materiales/<cat>/<slug>/<slug>-portada.png",
  "previews": [
    { "src": "materiales/<cat>/<slug>/<slug>-prev1.png" },
    { "src": "materiales/<cat>/<slug>/<slug>-prev2.png" },
    { "src": "materiales/<cat>/<slug>/<slug>-prev3.png" },
    { "src": "materiales/<cat>/<slug>/<slug>-prev4.png" }
  ],
  "link": "<link hotmart>",
  "videoYoutube": "<url>"
}
```

**Importante**:
- `previews` y `thumbnailStack` van como `[{src: "..."}]` (objetos), NO como array de strings. Decap CMS requiere ese formato y `cargarCategorias()` en `index.html` lo aplana en memoria.
- `formato: "slide"` solo en presentaciones Canva/PowerPoint (aspect-ratio 16:9). Omitir para fichas/tableros.
- Si es **pack con descuento**, agregar también:
  ```json
  "precioOriginal": "<precio sin descuento>",
  "etiquetaDestacado": "PACK · AHORRA $<diferencia>",
  "destacado": true,
  "thumbnailStack": [
    { "src": "materiales/<cat>/<slug>/portada1.png" },
    { "src": "materiales/<cat>/<slug>/portada2.png" }
  ]
  ```

## 6. Verificar assets referenciados

```bash
python3 .claude/check-assets.py
```

Escanea `index.html` + todos los `_data/categorias/*.json`. Falla si algún path no existe en disco.

## 7. Commit y push

```
Agregar <nombre del producto> a <categoría>
```

Incluir los assets nuevos + el JSON modificado.

## Notas del proyecto

- Hosting: **Netlify** (CDN + SSL automático). Un `git push` a `main` despliega en ~1 min.
- Formato de slides (Canva/PowerPoint) → siempre `formato: "slide"` (aspect-ratio 16:9)
- Documentos impresos (fichas, guías) → sin `formato`
- La **última preview siempre se difumina** con candado — elegir página con contenido valioso
- Convención de precios: punto como separador de miles (`"3.990"`)
