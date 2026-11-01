(() => {
  'use strict';
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const config = window.TINYEARSS;
  const motionQuery = matchMedia('(prefers-reduced-motion: reduce)');
  let storedMotion = null;
  try { storedMotion = localStorage.getItem('tinyearss-motion'); } catch (_) {}
  let motionPaused = motionQuery.matches || storedMotion === 'paused';
  let toastTimer;
  const toast = (message) => {
    const el = $('#toast');
    if (!el) return;
    el.textContent = message;
    el.classList.add('visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove('visible'), 3000);
  };
  function setMotion(paused, save = false) {
    motionPaused = paused;
    document.documentElement.classList.toggle('motion-paused', paused);
    $$('.motion-toggle').forEach(button => {
      button.setAttribute('aria-pressed', String(paused));
      button.disabled = motionQuery.matches;
      $('span', button).textContent = motionQuery.matches ? 'Reduced motion' : paused ? 'Play motion' : 'Pause motion';
    });
    $$('video[data-decorative]').forEach(video => {
      if (paused) video.pause();
      else video.play().catch(() => {});
    });
    if (save) {
      storedMotion = paused ? 'paused' : 'playing';
      try { localStorage.setItem('tinyearss-motion', paused ? 'paused' : 'playing'); } catch (_) {}
    }
  }
  $$('.motion-toggle').forEach(button => button.addEventListener('click', () => setMotion(!motionPaused, true)));
  motionQuery.addEventListener('change', event => setMotion(event.matches || storedMotion === 'paused'));
  setMotion(motionPaused);

  const menu = $('#site-menu');
  const menuToggle = $('#menu-toggle');
  let menuOpen = false;
  let menuFocusTimer;
  const background = [$('#main'), $('.site-footer'), $('.brand'), $('.header-links')].filter(Boolean);
  function setMenu(open) {
    menuOpen = open;
    document.body.classList.toggle('menu-open', open);
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.setAttribute('aria-label', open ? 'Close navigation menu' : 'Open navigation menu');
    $('span', menuToggle).textContent = open ? 'CLOSE' : 'MENU';
    menu.inert = !open;
    menu.setAttribute('aria-hidden', String(!open));
    background.forEach(el => { el.inert = open; });
    clearTimeout(menuFocusTimer);
    if (open) menuFocusTimer = setTimeout(() => $('.menu-nav a', menu).focus(), motionPaused ? 0 : 350);
    else menuToggle.focus({preventScroll: true});
  }
  menuToggle.addEventListener('click', () => setMenu(!menuOpen));
  menu.addEventListener('click', event => {
    if (event.target.closest('a')) setMenu(false);
  });
  document.addEventListener('keydown', event => {
    if (!menuOpen) return;
    if (event.key === 'Escape') { event.preventDefault(); setMenu(false); }
    if (event.key === 'Tab') {
      const items = [menuToggle, ...$$('a[href],button:not([disabled])', menu)];
      const current = items.indexOf(document.activeElement);
      const next = (current + (event.shiftKey ? -1 : 1) + items.length) % items.length;
      event.preventDefault();
      items[next].focus();
    }
  });

  // These are the artist's original star illustrations, not stock graphics.
  function sparkle(x, y, amount = 6) {
    if (motionPaused) return;
    for (let i = 0; i < amount; i++) {
      const particle = document.createElement('span');
      particle.className = 'spark';
      particle.setAttribute('aria-hidden', 'true');
      particle.textContent = '✦';
      particle.style.left = `${x}px`;
      particle.style.top = `${y}px`;
      particle.style.setProperty('--dx', `${(Math.random() - .5) * 170}px`);
      particle.style.setProperty('--dy', `${-30 - Math.random() * 100}px`);
      if (i % 2) particle.style.color = '#ff548d';
      document.body.append(particle);
      particle.addEventListener('animationend', () => particle.remove(), {once: true});
      setTimeout(() => particle.remove(), 1200);
    }
  }
  $$('.hero-star').forEach(star => star.addEventListener('click', event => {
    if (motionPaused) return;
    star.classList.remove('pop');
    void star.offsetWidth;
    star.classList.add('pop');
    const bounds = star.getBoundingClientRect();
    sparkle(event.detail ? event.clientX : bounds.x + bounds.width/2, event.detail ? event.clientY : bounds.y + bounds.height/2);
  }));
  const hero = $('.hero');
  if (hero && matchMedia('(pointer: fine)').matches) {
    let lastSpark = 0;
    hero.addEventListener('pointermove', event => {
      if (motionPaused || menuOpen || event.timeStamp - lastSpark < 170) return;
      lastSpark = event.timeStamp;
      sparkle(event.clientX, event.clientY, 1);
    });
  }

  if ('IntersectionObserver' in window && !motionPaused) {
    document.documentElement.classList.add('js-reveal');
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {threshold: .06});
    $$('.reveal').forEach(el => observer.observe(el));
  }
  const headerObserver = 'IntersectionObserver' in window && hero ? new IntersectionObserver(entries => {
    entries.forEach(entry => {
      const video = $('video', hero);
      if (!video) return;
      if (entry.isIntersecting && !motionPaused && !document.hidden) video.play().catch(() => {});
      else video.pause();
    });
  }, {threshold: 0}) : null;
  if (headerObserver) headerObserver.observe(hero);
  document.addEventListener('visibilitychange', () => {
    $$('video[data-decorative]').forEach(video => {
      if (document.hidden) video.pause();
      else if (!motionPaused && (hero?.getBoundingClientRect().bottom ?? 0) > 0) video.play().catch(() => {});
    });
  });

  // Projects expand into complete development galleries.
  $$('[data-project-toggle]').forEach(button => {
    const gallery = document.getElementById(button.getAttribute('aria-controls'));
    button.addEventListener('click', () => {
      const open = button.getAttribute('aria-expanded') !== 'true';
      button.setAttribute('aria-expanded', String(open));
      gallery.hidden = !open;
      button.innerHTML = open ? 'Close development sheets <span aria-hidden="true">−</span>' : 'Explore the project <span aria-hidden="true">+</span>';
    });
  });

  $$('[data-strip-direction]').forEach(button => button.addEventListener('click', () => {
    $('.sketch-strip').scrollBy({left: Number(button.dataset.stripDirection) * 290, behavior: motionPaused ? 'instant' : 'smooth'});
  }));

  const lightbox = $('#art-lightbox');
  let galleryItems = [];
  let currentArtwork = 0;
  let returnFocus = null;
  const wrap = $('.lightbox-image-wrap', lightbox);
  function drawArtwork() {
    const item = galleryItems[currentArtwork];
    const image = $('#lightbox-image');
    image.src = item.dataset.image;
    image.alt = item.dataset.caption;
    $('#lightbox-title').textContent = item.dataset.caption;
    $('#lightbox-count').textContent = `${currentArtwork + 1} / ${galleryItems.length}`;
    wrap.classList.remove('zoomed');
    $('#lightbox-zoom').setAttribute('aria-pressed', 'false');
    $('#lightbox-zoom').textContent = 'Zoom in';
    $('#lightbox-prev').disabled = galleryItems.length < 2;
    $('#lightbox-next').disabled = galleryItems.length < 2;
  }
  $$('[data-gallery]').forEach(trigger => trigger.addEventListener('click', () => {
    galleryItems = $$('[data-gallery]').filter(item => item.dataset.gallery === trigger.dataset.gallery && !item.hidden);
    currentArtwork = galleryItems.indexOf(trigger);
    returnFocus = trigger;
    drawArtwork();
    lightbox.showModal();
    document.body.classList.add('art-open');
  }));
  function changeArtwork(direction) {
    currentArtwork = (currentArtwork + direction + galleryItems.length) % galleryItems.length;
    drawArtwork();
  }
  $('#lightbox-close').addEventListener('click', () => lightbox.close());
  $('#lightbox-prev').addEventListener('click', () => changeArtwork(-1));
  $('#lightbox-next').addEventListener('click', () => changeArtwork(1));
  $('#lightbox-zoom').addEventListener('click', event => {
    const zoomed = wrap.classList.toggle('zoomed');
    event.currentTarget.setAttribute('aria-pressed', String(zoomed));
    event.currentTarget.textContent = zoomed ? 'Fit to screen' : 'Zoom in';
  });
  lightbox.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') { event.preventDefault(); changeArtwork(-1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); changeArtwork(1); }
  });
  lightbox.addEventListener('click', event => {
    if (event.target === lightbox) lightbox.close();
  });
  lightbox.addEventListener('close', () => {
    document.body.classList.remove('art-open');
    returnFocus?.focus({preventScroll: true});
  });
  let touchX;
  wrap.addEventListener('touchstart', event => { touchX = event.changedTouches[0].clientX; }, {passive: true});
  wrap.addEventListener('touchend', event => {
    const diff = event.changedTouches[0].clientX - touchX;
    if (!wrap.classList.contains('zoomed') && Math.abs(diff) > 65) changeArtwork(diff > 0 ? -1 : 1);
  }, {passive: true});

  $$('.copy-email').forEach(button => button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(config.email);
      toast('Email copied. See you in the inbox :)');
    } catch (_) {
      toast('Copy this address: ' + config.email);
    }
  }));
  const form = $('#contact-form');
  form?.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const name = String(data.get('name')).trim();
    const subject = `Tinyearss · ${data.get('project')} · ${name}`;
    const body = `Hi Martín!\n\n${String(data.get('message')).trim()}\n\n${name}\nReply to: ${data.get('email')}`;
    window.location.href = `mailto:${config.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    $('#form-status').textContent = 'Your email app should open with a draft. If it does not, use the email address above.';
  });

  // The published reel works without JavaScript; enhance motion and errors here.
  const backgroundVideo = $('.hero-video');
  if (backgroundVideo) {
    if (backgroundVideo.getAttribute('src') !== config.reelBackgroundSrc) {
      backgroundVideo.src = config.reelBackgroundSrc;
    }
    backgroundVideo.muted = true;
    backgroundVideo.loop = true;
    backgroundVideo.playsInline = true;
    backgroundVideo.poster = config.landingPoster;
    backgroundVideo.addEventListener('error', () => {
      // Keep a still from the landing video if video loading is unavailable.
      backgroundVideo.removeAttribute('src');
      backgroundVideo.load();
    }, {once: true});
    if (!motionPaused && !document.hidden) backgroundVideo.play().catch(() => {});
  }
  const reelVideo = $('#reel-video');
  if (reelVideo) {
    if (reelVideo.getAttribute('src') !== config.reelSrc) reelVideo.src = config.reelSrc;
    reelVideo.poster = config.reelPoster;
    reelVideo.addEventListener('error', () => { $('#reel-error').hidden = false; });
  }
})();
