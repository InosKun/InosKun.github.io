# Tinyearss — GitHub Pages

Código completo del diseño actual del portfolio de Martín Mora, preparado para el repositorio `InosKun/InosKun.github.io` y el dominio `tinyearss.com`.

Las seis páginas, las imágenes, las tipografías, los vídeos, los fondos con grano, los recursos decorativos y las interacciones están incluidos. El reparto actualizado de Heartquarters es la portada tanto de Home como de Portfolio; la nueva lámina de props también está incluida.

**Para publicarlo, abre primero [SUBIR-A-GITHUB.md](SUBIR-A-GITHUB.md).** La carpeta que debes copiar al repositorio es la que contiene este README, `index.html`, `CNAME` y `assets/`.

## Estructura

| Archivo o carpeta | Contenido |
| --- | --- |
| `index.html` | Landing con estrellas, vídeo de fondo, portfolio y demo reel |
| `portfolio/index.html` | Heartquarters → Lúcido → ATypical Office y sus galerías |
| `sketches/index.html` | Las 16 ilustraciones y su ampliación |
| `reel/index.html` | Demo reel con sonido y controles |
| `about/index.html` | Presentación y notas siempre visibles |
| `contact/index.html` | Contacto, copia del correo y formulario que abre un borrador |
| `style.css` | Diseño completo, paleta, animaciones y ajustes para móvil |
| `main.js` | Menú, galerías, zoom, movimiento y formulario |
| `site-config.js` | Rutas de vídeos y datos usados por el reproductor y el formulario |
| `assets/` | Recursos locales completos y optimizados |
| `pages/` | Compatibilidad con las cuatro direcciones de la web anterior |
| `404.html` | Página para direcciones inexistentes |
| `CNAME` | Dominio existente: `tinyearss.com` |
| `.nojekyll` | Publicación directa de los archivos estáticos |
| `scripts/` | Plantilla compartida y comprobación opcional del código |

## Cómo editar

El HTML, el CSS y el JavaScript ya están preparados para publicarse. No hay que instalar paquetes ni ejecutar un proceso de compilación para subir esta versión.

- **Diseño y colores:** edita `style.css`. La paleta está en `:root`; los ajustes para pantallas pequeñas están al final.
- **Contenido de una página:** puedes editar su `index.html` directamente.
- **Cabecera, footer, textos y proyectos de forma unificada:** edita `scripts/build-pages.py` y regenera las páginas con el comando de abajo. Esta opción sustituye los HTML generados; conserva tus cambios en la plantilla si eliges este método.
- **Vídeos y correo del formulario:** revisa `site-config.js`. Los textos y enlaces visibles de contacto también están en la plantilla o en los HTML.
- **Imágenes:** los nombres de los archivos están en la plantilla; usa recursos con el mismo formato y proporciones si sustituyes un archivo existente. Las láminas completas de Heartquarters tienen 1920 × 1080 px y sus miniaturas, 960 × 540 px.
- **Dominio:** el generador obtiene la dirección pública de `CNAME` para los metadatos y el sitemap.

Comandos opcionales con Python 3.9 o posterior, ejecutados desde esta carpeta:

```bash
python scripts/build-pages.py
python scripts/check-site.py
```

Para revisar el sitio en tu ordenador con Python:

```bash
python -m http.server 8000
```

Después abre `http://localhost:8000/`. En Windows puedes utilizar `py` en lugar de `python`.

## Compatibilidad con la web anterior

| Dirección anterior | Página nueva |
| --- | --- |
| `/pages/nosotros.html` | `/portfolio/` |
| `/pages/hospital.html` | `/sketches/` |
| `/pages/donar.html` | `/about/` |
| `/pages/actividades.html` | `/contact/` |

Las antiguas anclas `#Atypical` y `#Lucido` llevan a sus proyectos actuales. `#Plaga` lleva a Heartquarters, que sustituye aquel proyecto.

La copia se aplica sobre el repositorio existente. Sus carpetas anteriores de imágenes, CSS y JavaScript pueden permanecer: las nuevas páginas usan las rutas propias incluidas en este paquete. El dominio conserva el mismo `CNAME`.

La revisión se ha realizado sobre el commit público `c9d7707538fc7f0bde28132d76ab36bdeba179be`, que coincide con el ZIP facilitado. Los datos de referencia están en `scripts/migration-baseline.json`.

## Qué se comprueba

`scripts/check-site.py` revisa archivos, rutas y mayúsculas, enlaces internos, anclas, imágenes, etiquetas accesibles, tamaños de subida, CNAME y sitemap. El CSS, el JavaScript de interacción y los recursos gráficos proceden de la versión actual del diseño. Todos los recursos usados por las páginas se sirven desde el propio repositorio.
