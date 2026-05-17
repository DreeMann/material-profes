---
name: agregar-producto
description: Guía el proceso completo de agregar un nuevo material educativo al catálogo de profvanessa.cl — copia assets, genera el objeto JS y hace commit+push.
---

# Agregar producto a profvanessa.cl

Sigue este flujo exacto para agregar un nuevo material al catálogo:

## 1. Recopilar información del producto

Pregunta al usuario, uno por uno si no los dio todos de entrada:

- **Categoría**: presentaciones | fichas | tableros | guias | pruebas | flashcards
- **Nombre completo** del producto (ej: "Acto 1: Reparto equitativo de entradas")
- **Descripción corta** (nivel, páginas, asignatura — ej: "4°-5° Básico · 25 páginas · Matemática")
- **Detalle largo** (2-3 frases describiendo qué aprende el alumno y qué incluye)
- **Precio en CLP** sin puntos (ej: 5990) — o "gratis" si es gratuito
- **Link de Hotmart** (ej: https://pay.hotmart.com/XXXXXXX)
- **Ruta Windows de los assets** (ej: C:\Users\israe\Downloads\NombreCarpeta)
- **¿Tiene video de YouTube?** (opcional — URL completa)
- **¿Es pack con thumbnailStack?** (opcional — si agrupa varios productos)

## 2. Listar y verificar los assets disponibles

```bash
ls -la "/mnt/c/Users/israe/Downloads/<NombreCarpeta>/"
```

Identifica:
- Archivo de **portada** (PNG principal del producto)
- **Previews** (screenshots de páginas internas — mínimo 3, máximo 6, la última se difumina con candado)
- **PDF** del material (si existe y debe ser descargable)

## 3. Definir la convención de nombres

El patrón es: `<categoria>-<slug>-portada.png`, `<categoria>-<slug>-prev1.png`, etc.

Ejemplos reales del proyecto:
- `acto-1-portada.png`, `acto-1-prev1.png` ... `acto-1-prev4.png`, `acto-1.pdf`
- `tablero-potencias-portada.png`, `tablero-potencias-preview.png`
- `matematica-2-basico-portada.png`

## 4. Copiar y renombrar los assets

Determina la carpeta destino según categoría:
- presentaciones → `materiales/presentaciones/<slug>/`
- fichas → `materiales/fichas/<slug>/`
- tableros → `materiales/tableros/<slug>/`
- guias → `materiales/guias/<slug>/`

Crea la carpeta si no existe y copia los archivos con los nombres correctos.

## 5. Generar el objeto JS

Inserta en el array `productos` de la categoría correcta dentro de `categorias` en `index.html`.

Estructura base:
```js
{
  nombre: '<nombre>',
  descripcion: '<descripción corta>',
  detalle: '<detalle largo>',
  precio: '<precio>',           // null si es gratis
  formato: 'slide',             // solo para presentaciones/diapositivas
  thumbnail: 'materiales/<cat>/<slug>/<slug>-portada.png',
  previews: [
    'materiales/<cat>/<slug>/<slug>-prev1.png',
    'materiales/<cat>/<slug>/<slug>-prev2.png',
    'materiales/<cat>/<slug>/<slug>-prev3.png',
    'materiales/<cat>/<slug>/<slug>-prev4.png'   // esta se difumina con candado
  ],
  link: '<link hotmart>',
  videoYoutube: '<url>'         // omitir si no hay video
}
```

Si es pack con descuento, agregar también:
```js
  precioOriginal: '<precio sin descuento>',
  etiquetaDestacado: 'PACK · AHORRA $<diferencia>',
  destacado: true,
  thumbnailStack: ['portada1.png', 'portada2.png', 'portada3.png']
```

## 6. Verificar assets referenciados

Después de editar index.html, confirma que todos los paths existen en disco.

## 7. Commit y push

Mensaje de commit descriptivo:
```
Agregar <nombre del producto> a <categoría>
```

Incluir todos los archivos nuevos de assets + index.html en el commit.

## Notas del proyecto

- Formato de slides (Canva/PowerPoint) → siempre `formato: 'slide'` (aspect-ratio 16:9)
- Documentos impresos (fichas, guías) → sin `formato` (aspect-ratio 8.5:11 por defecto)
- La **última preview siempre se difumina** con candado — elegir una página de ejercicios o contenido valioso
- El archivo `Divisiones 3  .pdf` tiene **dos espacios** antes de `.pdf` — siempre verificar nombres con `ls`
- GitHub Pages tarda ~1 minuto en publicar después del push
