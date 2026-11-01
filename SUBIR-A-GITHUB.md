# Publicar el nuevo Tinyearss en tu repositorio

El paquete contiene la web completa, lista para `InosKun/InosKun.github.io`. Conserva `tinyearss.com`. El paso que actualiza la web pública será incorporar los archivos nuevos a la rama que publica GitHub Pages.

## 1. Descomprimir

Extrae `Tinyearss-GitHub-Pages.zip`. Localiza la carpeta que contiene `index.html`, `CNAME`, `style.css`, `main.js` y `assets/`. Ese es el contenido que debe quedar en la raíz del repositorio.

## 2. Subir con GitHub Desktop — recomendado

Esta opción permite revisar todos los cambios y subirlos juntos.

1. Abre [GitHub Desktop](https://desktop.github.com/) e inicia sesión en tu cuenta de GitHub.
2. En **File → Clone repository → URL**, introduce `https://github.com/InosKun/InosKun.github.io.git` y elige una carpeta de tu ordenador.
3. Usa **Fetch origin** y, si aparece, **Pull origin** para trabajar sobre la versión más reciente.
4. En **Current Branch → New Branch**, crea una rama llamada `tinyearss-nuevo` a partir de `main`.
5. Copia dentro de la carpeta clonada **el contenido de la carpeta del paso 1**, conservando su estructura y aceptando la sustitución de los archivos coincidentes. `index.html` y `CNAME` deben quedar al primer nivel. Mantén la carpeta `.git` que creó GitHub Desktop.
6. En **Changes**, revisa la lista. Las páginas antiguas cambian por redirecciones; se añaden los archivos del nuevo diseño y sus recursos. `CNAME` mantiene `tinyearss.com`.
7. Escribe un resumen, por ejemplo «Actualiza Tinyearss con el nuevo diseño», y crea el commit en `tinyearss-nuevo`.
8. Usa **Publish branch** o **Push origin**, según el estado que muestre Desktop.
9. Abre una pull request de `tinyearss-nuevo` a `main`. Cuando estén incluidos todos los archivos y hayas revisado el cambio, fusiónala. La versión anterior sigue disponible en el historial de Git.

Si quieres comprobar la web local antes de ese último paso y tienes Python, abre una terminal en la carpeta clonada y ejecuta `py -m http.server 8000` en Windows, o `python3 -m http.server 8000` en macOS/Linux. Visita `http://localhost:8000/`.

Documentación oficial: [clonar](https://docs.github.com/en/desktop/adding-and-cloning-repositories/cloning-and-forking-repositories-from-github-desktop), [ramas](https://docs.github.com/en/desktop/making-changes-in-a-branch/managing-branches-in-github-desktop) y [revisar y crear commits](https://docs.github.com/en/desktop/making-changes-in-a-branch/committing-and-reviewing-changes-to-your-project-in-github-desktop).

## 3. Comprobar GitHub Pages

En el repositorio, entra en **Settings → Pages** y comprueba:

| Ajuste | Valor previsto para esta copia |
| --- | --- |
| Source | Deploy from a branch |
| Branch | `main` |
| Folder | `/(root)` |
| Custom domain | `tinyearss.com` |
| HTTPS | Enforce HTTPS, cuando esté disponible |

Si estos valores ya son los de tu web actual, se conservan. El `CNAME` incluido contiene tu mismo dominio. Los metadatos, el sitemap y las rutas del paquete apuntan a él.

Después del despliegue, abre `https://tinyearss.com` y actualiza la página. En **Actions** puedes consultar el resultado de la publicación. La documentación indica que los cambios pueden tardar hasta unos diez minutos en aparecer.

Fuentes: [publicación desde una rama](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site), [dominio propio](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) y [publicación](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

## Alternativa: subir desde la web de GitHub

Trabaja en una rama nueva y utiliza **Add file → Upload files**. Sube el contenido descomprimido del paquete conservando las rutas. En la carpeta `assets/`, añade los archivos en tandas de hasta 100; completa todas las tandas antes de fusionar la rama con `main`.

El paquete cumple el límite de 25 MiB por archivo del cargador web. El ZIP es el contenedor para descargar el código: GitHub Pages publica los archivos extraídos.

Fuente: [subida de archivos a un repositorio](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).

## Revisión después de publicar

- Home muestra el reparto de Heartquarters como portada y reproduce el vídeo de fondo con su control de pausa.
- Portfolio conserva Heartquarters → Lúcido → ATypical Office, las imágenes ampliables y las dos láminas actualizadas.
- El demo reel conserva sus controles y sonido.
- Sketches muestra las 16 ilustraciones; About mantiene las notas visibles.
- Contact copia la dirección y prepara el borrador de correo.
- Las cuatro direcciones antiguas de `pages/` llevan a sus equivalentes nuevos.
- La navegación y los recursos se ajustan al ancho de móvil.

Esta copia está preparada para la raíz del repositorio de usuario y para tu dominio. Si en el futuro la trasladas a un repositorio de proyecto con una ruta adicional, como `usuario.github.io/otro-proyecto/`, habrá que adaptar las rutas que empiezan por `/`.
