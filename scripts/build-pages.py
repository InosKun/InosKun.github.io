from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT
DOODLES = json.loads((ROOT / 'scripts/doodle-assets.json').read_text())
ORIGIN = 'https://' + (ROOT / 'CNAME').read_text(encoding='utf-8').strip()
NAV = [('Home', '/'), ('Portfolio', '/portfolio/'), ('Sketches', '/sketches/'), ('Demo Reel', '/reel/'), ('About', '/about/'), ('Contact', '/contact/')]
STAR = '<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M20 2 24 15 38 14 27 23 32 37 20 29 8 37 13 23 2 14 16 15Z" fill="currentColor"/></svg>'
PAUSE = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M6 4v12M14 4v12" fill="none" stroke="currentColor" stroke-width="2"/></svg>'

def motion():
    return f'<button class="motion-toggle" type="button" aria-pressed="false">{PAUSE}<span>Pause motion</span></button>'

def socials():
    return '<div class="social-links"><a href="https://www.instagram.com/tiny.earss/" target="_blank" rel="noopener noreferrer">Instagram ↗</a><a href="https://x.com/tiny_earss" target="_blank" rel="noopener noreferrer">X ↗</a></div>'

def img(name, alt='', cls='', thumb=False, eager=False):
    stem = name + ('-thumb' if thumb else '')
    return f'<img src="/assets/{stem}.webp" alt="{escape(alt, quote=True)}" class="{cls}" loading="{"eager" if eager else "lazy"}" decoding="async">'

def doodle(name, cls=''):
    size = DOODLES[name]
    return f'<img src="/assets/doodle-{name}.webp" alt="" aria-hidden="true" class="doodle {cls}" width="{size["width"]}" height="{size["height"]}" loading="lazy" decoding="async" draggable="false">'

def gallery_button(name, caption, group, cls='art-sheet', child='', thumb=False):
    return f'<button type="button" class="{cls}" data-gallery="{group}" data-image="/assets/{name}.webp" data-caption="{escape(caption,quote=True)}" aria-label="Enlarge {escape(caption,quote=True)}">{img(name,caption,thumb=thumb)}{child}</button>'

def shell(page, title, description, content, dark=False):
    nav = ''.join(f'<a href="{path}"'+(' aria-current="page"' if page == label.lower().replace(' ', '-') else '')+f'><small>0{i+1}</small>{label}<i aria-hidden="true">↗</i></a>' for i, (label,path) in enumerate(NAV))
    header_links = ''.join(f'<a href="{path}"'+(' aria-current="page"' if page == label.lower().replace(' ', '-') else '')+f'>{label}</a>' for label,path in [NAV[1],NAV[3],NAV[4]])
    path = next((p for label,p in NAV if label.lower().replace(' ', '-') == page), '/')
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} · Tinyearss</title><meta name="description" content="{escape(description,quote=True)}">
<meta name="theme-color" content="{'#23172e' if dark else '#fff5e7'}">
<meta property="og:title" content="{escape(title,quote=True)} · Tinyearss"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:type" content="website"><meta property="og:image" content="{ORIGIN}/assets/artstation.webp"><meta property="og:url" content="{ORIGIN}{path}">
<link rel="canonical" href="{ORIGIN}{path}"><link rel="icon" href="/assets/logoestrella-thumb.webp" type="image/webp">
<link rel="preload" href="/assets/martinregular.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/style.css">
<script src="/site-config.js" defer></script><script src="/main.js" defer></script>
</head>
<body class="{'dark' if dark else ''}" data-page="{page}">
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><a href="/" class="brand" aria-label="Tinyearss — Home">{img('tinyearss-wordmark','Tinyearss',thumb=True,eager=True)}<span class="brand-label">MARTÍN MORA<small>CHARACTER DESIGN & 2D ANIMATION</small></span></a><nav class="header-links" aria-label="Quick navigation">{header_links}</nav></header>
<button id="menu-toggle" class="menu-button" type="button" aria-expanded="false" aria-controls="site-menu" aria-label="Open navigation menu">{STAR}<span>MENU</span></button>
<div id="site-menu" class="menu-shell" role="dialog" aria-modal="true" aria-label="Site navigation" aria-hidden="true" inert>
<div class="menu-content"><nav class="menu-nav" aria-label="Main navigation">{nav}</nav><div class="menu-side">{img('logoestrella','Tinyearss star with an illustrated eye',thumb=True)}<p class="hand">Pick a little<br>corner of my world.</p><p>Character design. Stories. A little chaos.</p></div><div class="menu-bottom"><a href="mailto:tinyearss8@gmail.com">tinyearss8@gmail.com ↗</a>{socials()}{motion()}</div></div></div>
<main id="main">{content}</main>
<footer class="site-footer"><div class="footer-top"><div><h2>Let's make<br>something stellar.</h2><a class="footer-bottom-link" href="/contact/">Say hello <span aria-hidden="true">↗</span></a></div><a href="/" class="footer-brand" aria-label="Tinyearss — Home">{img('tinyearss-wordmark','Tinyearss',thumb=True)}</a></div><div class="footer-meta"><span>© 2026 Martín Mora · Tinyearss</span>{socials()}<a href="#main">Back to top ↑</a></div></footer>
<dialog id="art-lightbox" class="lightbox" aria-labelledby="lightbox-title"><div class="lightbox-inner"><div class="lightbox-top"><h2 id="lightbox-title">Artwork</h2><button type="button" class="icon-button" id="lightbox-close" aria-label="Close artwork">×</button></div><div class="lightbox-image-wrap"><img id="lightbox-image" alt=""></div><div class="lightbox-controls"><span class="count" id="lightbox-count" aria-live="polite"></span><button class="pill" type="button" id="lightbox-zoom" aria-pressed="false">Zoom in</button><div class="lightbox-arrows"><button type="button" class="icon-button" id="lightbox-prev" aria-label="Previous artwork">←</button><button type="button" class="icon-button" id="lightbox-next" aria-label="Next artwork">→</button></div></div></div></dialog>
<div id="toast" class="toast" role="status" aria-live="polite"></div>
</body></html>'''
    location = DIST if path == '/' else DIST / path.strip('/')
    location.mkdir(exist_ok=True,parents=True)
    (location/'index.html').write_text(html)

def home():
    stars = ''.join(f'<button class="hero-star star-{i}" type="button" aria-label="Make star {i} dance">{img(f"estrella{i}","",thumb=True,eager=True)}</button>' for i in range(1,7))
    strip = ''.join(gallery_button(name,title,'home-sketches','strip-card',f'<span class="hand">{title}</span>',thumb=True) for name,title in [('sketch-isha','Colour overload'),('sketch-stargirl','Star girl'),('sketch-estela','A little sunshine'),('sketch-mujerona','Purple mood'),('sketch-beast','Beast boy')])
    return f'''
<section class="hero" aria-label="Welcome to Tinyearss">
<video class="hero-video" src="/assets/landing-background-v2-720.mp4" poster="/assets/landing-poster-v2.webp" muted loop playsinline preload="none" data-decorative aria-hidden="true" tabindex="-1"></video><div class="orbit-line"></div><div class="orbit-line two"></div>
{stars}<div class="hero-center"><p class="eyebrow">A LITTLE WORLD BY MARTÍN MORA</p><h1 class="hero-wordmark">{img('tinyearss-wordmark','Tinyearss',cls='hero-wordmark-image',eager=True)}</h1><p class="hero-tag">Characters. Stories. A little sparkle.</p><div class="action-row"><a class="pill fill" href="/portfolio/">Explore my work <span aria-hidden="true">↗</span></a><a class="pill" href="/reel/">2D Demo Reel <span aria-hidden="true">↗</span></a></div></div>
<p class="hero-note hand">go on,<br>touch a star :)</p><div class="hero-bottom"><a class="scroll-cue" href="#selected">{img('perfil','',thumb=True,eager=True)}SCROLL TO MEET THE CAST</a><div><a class="preview-label" href="/reel/">2D Animation Demo Reel ↗</a>{motion()}</div></div></section>
<div class="marquee" aria-label="Character design, 2D animation, colour and chaos"><div class="marquee-track" aria-hidden="true"><span>CHARACTER DESIGN <b>✳</b> 2D ANIMATION <b>✳</b> COLOUR & CHAOS <b>✳</b></span><span>CHARACTER DESIGN <b>✳</b> 2D ANIMATION <b>✳</b> COLOUR & CHAOS <b>✳</b></span></div></div>
<section class="section paper-section color-wash" id="selected"><div class="container"><div class="section-heading reveal"><div><h2>Meet<br>the cast.</h2></div>{doodle('cross','heading-doodle doodle-drift')}<p>A few worlds I've been building.<br>Come for the characters, stay for the little details.</p></div>
<div class="selected-feature reveal"><a class="selected-visual" href="/portfolio/#heartquarters" aria-label="Explore Heartquarters"><span class="tape" aria-hidden="true"></span>{img('heartquarters-cast-lineup','Heartquarters character line-up')}</a><div class="selected-copy"><span class="project-number">01 / CHARACTER DESIGN & VISUAL DEVELOPMENT</span><h3>Heartquarters</h3><p>Meet Andrea and Leo through character explorations, playful interactions and the props that bring their world to life.</p><div class="doodle-link-row"><a class="text-link" href="/portfolio/#heartquarters">Step into this world <span class="arrow" aria-hidden="true">↗</span></a>{doodle('loop','link-doodle')}</div></div></div>
<div class="small-picks"><a class="small-pick reveal" href="/portfolio/#lucido"><div class="pick-image">{img('work-15','The colourful cast of Lúcido')}</div><div class="pick-caption"><div><p class="eyebrow">02 / CHARACTER DESIGN PROPOSAL</p><h3>Lúcido</h3></div><span aria-hidden="true">↗</span></div></a><a class="small-pick reveal" href="/portfolio/#atypical"><div class="pick-image">{img('work-6','Character line-up for ATypical Office')}</div><div class="pick-caption"><div><p class="eyebrow">03 / ANIMATED SERIES PROPOSAL</p><h3>ATypical Office</h3></div><span aria-hidden="true">↗</span></div></a></div>
<div class="portfolio-link-row"><a class="pill" href="/portfolio/">The whole portfolio <span aria-hidden="true">↗</span></a>{doodle('zigzag','section-tail-doodle')}</div></div></section>
<section class="section home-reel" id="animation" aria-labelledby="home-reel-title"><div class="container">
<div class="home-reel-heading"><div><h2 id="home-reel-title">Drawn to move.</h2></div>{doodle('rays','reel-heading-doodle')}</div>
<figure class="home-reel-film"><div class="home-reel-screen">
<video id="reel-video" src="/assets/demo-reel-2026.mp4" poster="/assets/reel-poster.webp" controls playsinline preload="none" aria-label="2D animation demo reel by Martín Mora">Your browser does not support embedded video. <a href="/assets/demo-reel-2026.mp4">Open the demo reel.</a></video>
</div><figcaption class="home-reel-caption"><div><span class="eyebrow">2D DEMO REEL</span><span class="home-reel-meta">2026 · 0:52</span></div><a class="text-link" href="/reel/">Open the reel page <span class="arrow" aria-hidden="true">↗</span></a></figcaption></figure>
<div class="home-reel-bottom">{doodle('burst','reel-left-doodle')}<div class="home-reel-note" aria-hidden="true">{doodle('moon','reel-moon')}<span class="hand">one frame at a time.</span></div></div>
<p id="reel-error" class="reel-error" role="status" hidden>The video could not load. <a href="/assets/demo-reel-2026.mp4">Open the video directly ↗</a></p>
</div></section>
<section class="section home-about"><div class="container about-teaser"><div class="portrait-scene reveal">{img('perfil-4','Portrait of Martín Mora',cls='portrait')}{img('star-cluster','',cls='scene-star star-cluster',thumb=True)}{img('libris','',cls='scene-stamp',thumb=True)}<span class="hand">the human behind the stars ↘</span></div><div class="reveal"><h2>I'm Martín.<br>Nice to meet you.</h2>{doodle('wave','doodle-underline')}<p>I'm the character designer and 2D animator behind Tinyearss. I love to create new stories, play with colors and bring new characters to life</p><a class="text-link" href="/about/">A little more about me <span class="arrow" aria-hidden="true">↗</span></a></div></div></section>
<section class="section sketchbook-preview"><div class="container"><div class="section-heading reveal"><div><h2>Loose lines.<br>Loud colours.</h2></div>{doodle('flower','heading-doodle doodle-drift')}{doodle('scallop','sketch-heading-doodle')}</div><div class="sketch-strip" tabindex="0" aria-label="Sketchbook highlights">{strip}</div><div class="strip-controls"><a class="text-link" href="/sketches/">Open the sketchbook <span class="arrow" aria-hidden="true">↗</span></a><div class="action-row"><button type="button" class="icon-button" data-strip-direction="-1" aria-label="Scroll sketches left">←</button><button type="button" class="icon-button" data-strip-direction="1" aria-label="Scroll sketches right">→</button></div></div></div></section>'''

CAPTIONS = {4:'Animated series proposal',5:'Environment concept',6:'Character line-up',7:'Character poses and expressions',8:'Turnaround and design explorations',9:'Character shapes and colour explorations',10:'Silhouette and character studies',11:'Prop design',12:'Environment concepts',13:'Project title',14:'Project introduction',15:'Character line-up',16:'Character explorations',17:'Character and colour explorations',18:'Colour and outfit explorations',19:'Poses and expressions',20:'Silhouette and character studies',21:'Star design and poses',22:'Shape explorations'}
PROJECTS = [
    dict(id='heartquarters',title='Heartquarters',kind='CHARACTER DESIGN & VISUAL DEVELOPMENT',cover='heartquarters-cast-lineup',number='01',note='a cast<br>with heart.',description='Character explorations, interaction poses and prop designs for Heartquarters.',sheets=[('heartquarters-title','Project title'),('heartquarters-cast-lineup','Cast line-up'),('heartquarters-andrea','Andrea · character explorations'),('heartquarters-leo','Leo · character explorations'),('heartquarters-interactions','Interaction poses'),('heartquarters-props-v2','Prop designs'),('heartquarters-closing','Closing illustration')]),
    dict(id='lucido',title='Lúcido',kind='CHARACTER DESIGN PROPOSAL',cover='work-15',number='02',note='a little<br>dream logic.',description='An expressive cast, vivid colour explorations and a star with its own personality.',sheets=[(f'work-{n}',CAPTIONS[n]) for n in range(13,23)]),
    dict(id='atypical',title='ATypical Office',kind='ANIMATED SERIES PROPOSAL',cover='work-6',number='03',note='an unusual<br>day at work.',description='Character design, props and environment explorations for an animated series proposal.',sheets=[(f'work-{n}',CAPTIONS[n]) for n in range(4,13)])
]

def portfolio():
    chapters = ''
    for i,p in enumerate(PROJECTS,1):
        sheets = ''.join(gallery_button(asset,f'{p["title"]} · {caption}',p['id'],child=f'<span class="sheet-label">{caption}<span aria-hidden="true">↗</span></span>',thumb=True) for asset,caption in p['sheets'] if asset != p['cover'])
        cover_caption = f'{p["title"]} · {dict(p["sheets"])[p["cover"]]}'
        project_doodle = ['arrows','moon','zigzag'][i-1]
        heading_tag = 'h1' if i == 1 else 'h2'
        chapters += f'''<section class="project-chapter chapter-{i} project-{p['id']}" id="{p['id']}"><div class="container"><div class="project-top reveal"><div><span class="project-number">{p['number']} / {p['kind']}</span><{heading_tag}>{p['title']}</{heading_tag}><p>{p['description']}</p></div><span class="project-sidenote">{doodle(project_doodle,'project-doodle')}<span class="hand" style="font-size:32px;transform:rotate(-8deg)">{p['note']}</span></span></div><div class="chapter-cover reveal">{img(p['cover'],cover_caption)}<button class="cover-open" type="button" data-gallery="{p['id']}" data-image="/assets/{p['cover']}.webp" data-caption="{cover_caption}" aria-label="Enlarge {cover_caption}">↗</button></div><div class="project-expand"><button type="button" class="pill" data-project-toggle aria-controls="gallery-{p['id']}" aria-expanded="false">Explore the project <span aria-hidden="true">+</span></button>{doodle('wave','project-rule')}<p>{len(p['sheets'])} sheets · click any image to explore</p></div><div class="project-gallery" id="gallery-{p['id']}" hidden>{sheets}</div></div></section>'''
    return f'''<div class="portfolio-projects">{chapters}</div><section class="section color-wash wash-peach"><div class="container portfolio-outro"><div class="reveal"><p class="hand">A different<br>kind of character.</p><p>For illustrations, colour experiments and a look inside the sketchbook, take the scenic route.</p><div class="doodle-link-row"><a class="text-link" href="/sketches/">Explore the sketches <span class="arrow" aria-hidden="true">↗</span></a>{doodle('scallop','outro-doodle')}</div></div><a href="/sketches/" aria-label="Explore illustrations">{img('work-23','An illustrated portrait by Martín Mora')}</a></div></section>'''

SKETCHES = [('isha', 'Colour overload'), ('mujerona', 'Purple mood'), ('estela', 'A little sunshine'), ('stargirl', 'Star girl'), ('howl', 'Howl'), ('beast', 'Beast boy'), ('sophie', 'Sophie'), ('locos', 'After dark'), ('bob', 'A little pineapple'), ('hinata', 'Hinata'), ('top', 'Midwest indigo'), ('boyheron', 'The boy & the heron'), ('noya', 'Noya'), ('geisha', 'Light study'), ('yaku', 'Yaku'), ('rose', 'A quiet moment')]

def sketches():
    cards = ''
    for i,(stem,title) in enumerate(SKETCHES):
        child = f'<span class="hand">{title}</span>'
        card = gallery_button(f'sketch-{stem}',title,'sketches','sketch-item',child=child,thumb=False)
        cards += card.replace('class="sketch-item"',f'class="sketch-item" style="--rotation:{[-2,3,-1,2][i%4]}deg"')
    return f'''<section class="sketch-intro"><div class="page-intro compact-intro container"><p class="eyebrow">THE SKETCHBOOK / ILLUSTRATIONS</p><h1>A beautifully messy mind.</h1>{doodle('heart','intro-star')}<div class="intro-row"><p>Colour studies, familiar faces, and little ideas that grew into something more.</p></div></div></section><section class="section sketch-gallery color-wash wash-rose"><div class="container">{doodle('wave','sketch-wave')}<div class="sketch-grid">{cards}</div><div class="sketch-signoff">{doodle('burst','signoff-doodle doodle-drift')}<p class="sketch-note hand">More colours. More stories. Always more stars.</p>{doodle('arches','signoff-doodle')}</div></div></section>'''

def about():
    return f'''<section class="section about-hero"><div class="container about-layout"><div><p class="eyebrow">THE ARTIST / OH, HEY!</p><h1>I'm Martín.<span class="about-alias">Also, Tinyearss.</span></h1><p class="about-copy">I'm a character designer and 2D animator. Tinyearss is my little corner of the internet: a place for characters, stories and colours that refuse to sit still.</p><p class="about-copy">From a character's first silhouette to the frame that brings them to life, I love exploring how design can tell a story.</p><div class="action-row"><a class="pill" href="/portfolio/">Meet my characters ↗</a><a class="text-link" href="/contact/">Say hello ↗</a></div><div class="signature-line"><p class="hand about-signature">Nice to meet you, by the way :)</p>{doodle('moon','signature-moon')}</div></div><div class="about-portrait">{img('perfil-4','Martín Mora, the artist behind Tinyearss',cls='portrait',eager=True)}{img('star-cluster','',cls='scene-star star-cluster',thumb=True)}<span class="hand">yes, this is me! ↙</span></div></div></section>
<section class="section color-wash wash-rose"><div class="container"><p class="eyebrow">WHAT I DO</p><div class="skills-heading"><h2 style="margin-top:20px">Ideas with<br>personality.</h2>{doodle('scribble','skills-doodle doodle-drift')}</div><div class="skills-list"><div class="skill-row reveal"><span class="eyebrow">01</span><h3>Character design</h3><p>Silhouettes, expressions, costumes and the little details that make a character feel like someone.</p></div><div class="skill-row reveal"><span class="eyebrow">02</span><h3>2D animation</h3><p>Bringing those personalities into motion, one drawing and one frame at a time.</p></div><div class="skill-row reveal"><span class="eyebrow">03</span><h3>Visual development</h3><p>Shapes, palettes and environments that make room for a whole story.</p></div></div></div></section>
<section class="section notes-section"><div class="container notes-layout"><div class="reveal"><p class="eyebrow">OUTSIDE THE DRAWING BOARD</p><h2>A few things in<br>my solar system</h2><p>Photography, volleyball, video games, anime, music, my dogs, and probably a conversation that went on a little too long.</p><div class="notes-doodles">{doodle('flower','notes-flower doodle-drift')}{doodle('heart','notes-heart')}</div></div><div class="note-stack"><article class="personal-note"><span class="tape" aria-hidden="true"></span><h3 class="note-title">My essentials</h3>{img('esencial','Hand-drawn essentials: drawing tools, headphones, music and a camera')}</article><article class="personal-note"><span class="tape" aria-hidden="true"></span><h3 class="note-title">Things I love</h3>{img('like','Handwritten list: volleyball, photography, creating characters, video games, anime, music and my dogs')}</article></div></div></section>
<section class="section"><div class="container about-links"><h2>Let's put an<br>idea into orbit.</h2>{doodle('cross','about-orbit doodle-drift')}<a class="pill fill" href="/contact/">Tell me about your project ↗</a></div></section>'''

def reel():
    return f'''<section class="reel-intro"><div class="page-intro compact-intro container"><p class="eyebrow">THE ANIMATION ROOM / 2D DEMO REEL</p><h1>Made to move.</h1>{doodle('rays','intro-star')}<div class="intro-row"><p>A home for the characters that won't sit still.<br>Character design, feeling and movement.</p></div></div></section>
<section class="reel-page"><div class="container"><div class="reel-stage"><video id="reel-video" src="/assets/demo-reel-2026.mp4" poster="/assets/reel-poster.webp" controls playsinline preload="metadata" aria-label="2D animation demo reel by Martín Mora">Your browser does not support embedded video. <a href="/assets/demo-reel-2026.mp4">Open the demo reel.</a></video><span class="frame-corner tl"></span><span class="frame-corner tr"></span><span class="frame-corner bl"></span><span class="frame-corner br"></span></div><div class="reel-caption"><span id="reel-label">2D Animation Demo Reel · 2026 · 0:52</span><a href="/assets/demo-reel-2026.mp4" target="_blank" rel="noopener noreferrer">Open video ↗</a>{motion()}</div><p id="reel-error" class="reel-error" role="status" hidden>The video could not load. <a href="/assets/demo-reel-2026.mp4">Open the video directly ↗</a></p>{doodle('rays','reel-margin-doodle')}</div></section>
<section class="section paper-section color-wash reel-process"><div class="container process-row"><div class="process-art reveal">{img('work-17','Character exploration and colour design for Lúcido')}</div><div class="reveal"><p class="eyebrow">BEFORE THE FIRST FRAME</p><h2>It starts<br>with a character.</h2><p>Expressions, silhouettes and colour explorations: the ideas behind the faces. Take a look at the design side of my work.</p><div class="doodle-link-row"><a class="text-link" href="/portfolio/">Back to the drawing board <span class="arrow" aria-hidden="true">↗</span></a>{doodle('arches','process-doodle')}</div></div></div></section>'''

def contact():
    return f'''<section class="contact-section"><div class="container contact-layout"><div><p class="eyebrow">THE INBOX / LET'S TALK</p><h1>Let's make<span>something</span><span>stellar.</span></h1><div class="contact-email"><a class="email-link" href="mailto:tinyearss8@gmail.com">tinyearss8@gmail.com</a><button class="copy-email" type="button" aria-label="Copy email address">COPY</button></div>{socials()}</div><div class="contact-graphic">{img('libris','Tinyearss illustrated signature stamp',cls='stamp',eager=True)}<p class="hand">a little hello<br>can go a long way.</p></div></div></section>
<section class="section color-wash wash-peach"><div class="container contact-form-layout"><div class="reveal"><p class="eyebrow" style="margin-bottom:20px">HAVE SOMETHING IN MIND?</p><h2>Tell me<br>your story.</h2><p>A character, an animation, a collaboration — or just a friendly hello. I'd love to hear from you.</p><div class="contact-doodles">{doodle('heart','contact-heart doodle-drift')}{doodle('rays','contact-rays')}</div>{doodle('loop','contact-margin-doodle')}</div><form class="contact-form" id="contact-form"><div class="form-field"><label for="contact-name">Your name</label><input id="contact-name" name="name" autocomplete="name" maxlength="100" placeholder="Nice to meet you!" required></div><div class="form-field"><label for="contact-email">Your email</label><input id="contact-email" name="email" type="email" autocomplete="email" maxlength="254" placeholder="you@example.com" required></div><div class="form-field full"><label for="contact-project">What are you thinking?</label><select id="contact-project" name="project"><option>Character design</option><option>2D animation</option><option>Visual development</option><option>Illustration</option><option>Collaboration</option><option>Just saying hello</option></select></div><div class="form-field full"><label for="contact-message">Your idea</label><textarea id="contact-message" name="message" maxlength="3000" rows="5" placeholder="It all starts with a little idea…" required></textarea></div><button class="pill fill" type="submit">Open an email draft <span aria-hidden="true">↗</span></button><p class="form-note">Opens your email app with a draft. Nothing is sent automatically.</p><div id="form-status" class="form-status" role="status" aria-live="polite"></div></form></div></section>'''

shell('home','Characters, stories & a little sparkle','Martín Mora · Tinyearss. Character design, visual development and 2D animation.',home(),True)
shell('portfolio','Portfolio','Explore Heartquarters, Lúcido and ATypical Office: character design and visual development by Martín Mora.',portfolio())
shell('sketches','Sketches','Illustrations, colour studies and experiments from the Tinyearss sketchbook.',sketches())
shell('about','About Martín','Meet Martín Mora, the character designer and 2D animator behind Tinyearss.',about())
shell('demo-reel','2D Demo Reel','Watch the 2026 2D animation demo reel by Martín Mora: rough animation, cleanup and finished shots.',reel(),True)
shell('contact','Contact','Get in touch with Martín Mora for character design, 2D animation and illustration.',contact())
(DIST/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n')
(DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{ORIGIN}{path}</loc></url>' for _,path in NAV)+'</urlset>')
from build_compat import write_compatibility_pages
write_compatibility_pages(ROOT, ORIGIN)
print('Built six pages, legacy routes, 404, sitemap and robots.txt.')
