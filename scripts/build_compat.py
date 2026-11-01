"""Static GitHub Pages compatibility files; no server-side code is required."""
from html import escape
from pathlib import Path
import json
import re


def write_compatibility_pages(root: Path, origin: str) -> None:
    migration = json.loads((root / 'scripts/migration-baseline.json').read_text(encoding='utf-8'))
    aliases = {'atypical': 'atypical', 'lucido': 'lucido', 'plaga': 'heartquarters'}
    for old_path, new_path in migration['legacy_routes'].items():
        label = new_path.strip('/').title()
        fragment_aliases = aliases if new_path == '/portfolio/' else {}
        html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(label)} · Tinyearss</title>
<link rel="canonical" href="{escape(origin + new_path, quote=True)}">
<meta http-equiv="refresh" content="0;url={escape(new_path, quote=True)}">
<script>
(() => {{
  const target = new URL({json.dumps(new_path)}, window.location.href);
  const aliases = {json.dumps(fragment_aliases)};
  let fragment = window.location.hash.slice(1);
  try {{ fragment = decodeURIComponent(fragment); }} catch (_) {{}}
  target.search = window.location.search;
  target.hash = aliases[fragment.toLowerCase()] || fragment;
  window.location.replace(target.href);
}})();
</script>
<style>body{{margin:60px auto;padding:0 24px;max-width:620px;background:#fff5e7;color:#301c3b;font-family:Arial,sans-serif;line-height:1.6}}a{{color:inherit}}</style>
</head>
<body><main><h1>{escape(label)}</h1><p><a href="{escape(new_path, quote=True)}">Continue to {escape(label)} →</a></p></main></body>
</html>
'''
        destination = root / old_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(html, encoding='utf-8')

    # Reuse the exact shared header, navigation and footer of the main site.
    html = (root / 'index.html').read_text(encoding='utf-8')
    html = re.sub(r'<title>.*?</title>', '<title>Page not found · Tinyearss</title>', html, count=1)
    html = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="Find your way back to the characters, stories and sketches of Tinyearss.">', html, count=1)
    html = re.sub(r'<meta property="og:[^"]+"[^>]*>', '', html)
    html = html.replace('<body class="dark" data-page="home">', '<body class="" data-page="not-found">')
    html = html.replace('<meta name="theme-color" content="#23172e">', '<meta name="theme-color" content="#fff5e7">')
    html = html.replace('</head>', '<meta name="robots" content="noindex,follow">\n</head>')
    main = '''<main id="main"><section class="section" style="padding-top:150px"><div class="container">
<p class="eyebrow">404 / A LITTLE DETOUR</p>
<h1 style="font-size:clamp(58px,11vw,120px);margin:28px 0">Lost in orbit.</h1>
<p>This little corner has moved. Let's get you back to the characters.</p>
<div class="action-row" style="margin:32px 0"><a class="pill fill" href="/">Back to Home ↗</a><a class="pill" href="/portfolio/">Explore the portfolio ↗</a></div>
<img src="/assets/estrella3-thumb.webp" alt="" aria-hidden="true" style="width:90px;height:auto;transform:rotate(12deg)">
</div></section></main>'''
    html = re.sub(r'<main id="main">.*?</main>', lambda _: main, html, count=1, flags=re.S)
    (root / '404.html').write_text(html, encoding='utf-8')
