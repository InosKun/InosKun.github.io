"""Validate the portable static site before uploading to GitHub Pages.

Usage: python scripts/check-site.py
Uses only Python's standard library; it never changes files or contacts GitHub.
"""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MAIN_PAGES = ['index.html', 'portfolio/index.html', 'sketches/index.html',
              'reel/index.html', 'about/index.html', 'contact/index.html']
failures = []


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids = set()
        self.references = []
        self.attributes = []
        self.h1_count = 0
        self.lang = None
        self.title_found = False

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        self.attributes.append((tag, data))
        if tag == 'html': self.lang = data.get('lang')
        if tag == 'title': self.title_found = True
        if tag == 'h1': self.h1_count += 1
        if data.get('id'):
            if data['id'] in self.ids:
                failures.append(f'{self.path}: duplicate ID {data["id"]}')
            self.ids.add(data['id'])
        if tag == 'img' and 'alt' not in data:
            failures.append(f'{self.path}: missing image alt')
        for key in ('src', 'href', 'data-image', 'poster'):
            if data.get(key): self.references.append(data[key])
        if tag == 'button' and data.get('type') not in ('button', 'submit'):
            failures.append(f'{self.path}: button without explicit type')
        if tag == 'meta' and data.get('http-equiv', '').lower() == 'refresh':
            match = re.search(r'url=(.+)', data.get('content', ''), re.I)
            if match: self.references.append(match.group(1))


domain = (ROOT / 'CNAME').read_text(encoding='utf-8').strip()
if not re.fullmatch(r'[A-Za-z0-9.-]+', domain) or '.' not in domain:
    failures.append('CNAME must contain one domain name, without https:// or a path')
origin = 'https://' + domain
migration = json.loads((ROOT / 'scripts/migration-baseline.json').read_text(encoding='utf-8'))
required = MAIN_PAGES + list(migration['legacy_routes']) + ['404.html']
for name in required:
    if not (ROOT / name).is_file(): failures.append(f'Missing page: {name}')
if not (ROOT / '.nojekyll').is_file(): failures.append('Missing .nojekyll')

pages = {}
for name in required:
    path = ROOT / name
    if not path.is_file(): continue
    parser = Page(name)
    parser.feed(path.read_text(encoding='utf-8'))
    pages[path] = parser
    if parser.h1_count != 1:
        failures.append(f'{name}: expected one h1, got {parser.h1_count}')
    if parser.lang != 'en': failures.append(f'{name}: incorrect page language')
    if not parser.title_found: failures.append(f'{name}: missing title')
    for tag, data in parser.attributes:
        for attr in ('aria-controls', 'aria-labelledby'):
            for target in data.get(attr, '').split():
                if target not in parser.ids:
                    failures.append(f'{name}: broken {attr}={target}')
        if tag == 'label' and data.get('for') not in parser.ids and 'for' in data:
            failures.append(f'{name}: broken form label')
        if name in MAIN_PAGES and tag == 'link' and data.get('rel') == 'canonical':
            route = '/' if name == 'index.html' else '/' + name.removesuffix('index.html')
            if data.get('href') != origin + route:
                failures.append(f'{name}: incorrect canonical URL')

for path, parser in pages.items():
    for reference in parser.references:
        url = urlsplit(reference)
        if url.scheme or url.netloc: continue
        target = ROOT / unquote(url.path.lstrip('/')) if url.path.startswith('/') else path.parent / unquote(url.path)
        if not url.path: target = path
        if target.is_dir(): target = target / 'index.html'
        if not target.is_file():
            failures.append(f'{parser.path}: missing resource {reference}')
        if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            failures.append(f'{parser.path}: missing anchor {reference}')

css = (ROOT / 'style.css').read_text(encoding='utf-8')
for resource in re.findall(r"""url\(['"]?(/[^\)'"\s]+)""", css):
    if not (ROOT / resource.lstrip('/')).is_file():
        failures.append(f'CSS: missing resource {resource}')
if css.count('{') != css.count('}'): failures.append('CSS: unbalanced blocks')
if '[hidden]{display:none!important}' not in css:
    failures.append('Missing strict hidden-state rule')

assets = [p for p in (ROOT / 'assets').rglob('*') if p.is_file()]
for path in assets:
    if path.stat().st_size > 25 * 1024 * 1024:
        failures.append(f'{path.relative_to(ROOT)}: larger than the 25 MiB browser-upload limit')
    with path.open('rb') as handle:
        if handle.read(80).startswith(b'version https://git-lfs.github.com/spec/v1'):
            failures.append(f'{path.relative_to(ROOT)}: Git LFS pointer instead of the actual asset')

for path in list(pages) + [ROOT / p for p in ['style.css', 'main.js', 'site-config.js', 'robots.txt', 'sitemap.xml']]:
    text = path.read_text(encoding='utf-8')
    if re.search(r'https?://[^\s"\'<>]*(?:chatgpt\.site|oaiusercontent\.com)', text):
        failures.append(f'{path.relative_to(ROOT)}: non-portable hosting URL')

tree = ET.parse(ROOT / 'sitemap.xml')
locations = [node.text for node in tree.findall('.//{*}loc')]
expected = [origin + ('/' if p == 'index.html' else '/' + p.removesuffix('index.html')) for p in MAIN_PAGES]
if set(locations) != set(expected): failures.append('Sitemap must list the six main routes at the CNAME domain')
if origin + '/sitemap.xml' not in (ROOT / 'robots.txt').read_text(encoding='utf-8'):
    failures.append('robots.txt points to the wrong sitemap')

if failures:
    print('\n'.join(failures))
    raise SystemExit(1)
groups = Counter(data['data-gallery'] for page in pages.values() for _, data in page.attributes if 'data-gallery' in data)
print(f'OK: {len(MAIN_PAGES)} main pages, {len(migration["legacy_routes"])} legacy routes, 404, {len(assets)} assets.')
print('Verified: local paths and case, anchors, ARIA, labels, CNAME, sitemap, upload sizes and real asset files.')
print('Gallery entries: ' + ', '.join(f'{name}={count}' for name, count in sorted(groups.items())))
