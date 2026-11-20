/* DR. SCHIWAGO · Goldene Nacht */
(() => {
  const IMG = window.IMG || {};
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const ease = t => 1 - Math.pow(1 - t, 3);
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const touch = matchMedia('(hover: none)').matches;

  /* Bilder: fehlt ein Motiv, verschwindet das Element (keine Platzhalter) */
  $$('[data-need]').forEach(el => { if (!IMG[el.dataset.need]) el.classList.add('is-missing'); });
  const portrait = matchMedia('(max-aspect-ratio: 4/5)').matches;
  $$('img[data-img]').forEach(img => {
    let key = img.dataset.img;
    if (portrait && IMG[key + '-m']) key += '-m'; // eigenes Hochformat-Motiv fürs Handy
    const m = IMG[key];
    if (!m) { img.classList.add('is-missing'); return; }
    img.src = m.s;
    img.srcset = `${m.s} ${m.sw}w, ${m.l} ${m.lw}w`;
    img.sizes = img.closest('.bar, .dress__grid figure') ? '(max-width: 720px) 80vw, 40vw' : '100vw';
    img.decoding = 'async';
    if (!img.closest('.hero')) img.loading = 'lazy';
    img.width = m.w; img.height = m.h;
  });

  /* Nav */
  const nav = $('#nav');
  const burger = $('.nav__burger');
  burger.addEventListener('click', () => { const o = nav.classList.toggle('is-open'); burger.setAttribute('aria-expanded', o); });
  $$('.nav__links a').forEach(a => a.addEventListener('click', () => { nav.classList.remove('is-open'); burger.setAttribute('aria-expanded', false); }));

  /* 1 · Hero: Kronleuchter geht an */
  const hero = $('#hero');
  const heroImg = $('.hero__img');
  const lightUp = () => requestAnimationFrame(() => hero.classList.add('is-lit'));
  if (heroImg && !heroImg.classList.contains('is-missing')) {
    if (heroImg.complete && heroImg.naturalWidth) setTimeout(lightUp, 250);
    else { heroImg.addEventListener('load', () => setTimeout(lightUp, 150), { once: true }); setTimeout(lightUp, 2500); }
  } else lightUp();

  /* Goldfunken (Hero) und Goldstaub (Garten) */
  function sparks(canvas, mode) {
    const ctx = canvas.getContext('2d');
    let w, h, dpr, parts = [], on = false, raf;
    const N = mode === 'hero' ? 70 : 110;
    const size = () => { dpr = Math.min(2, devicePixelRatio || 1); w = canvas.clientWidth; h = canvas.clientHeight; canvas.width = w * dpr; canvas.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
    const spawn = (p, init) => {
      if (mode === 'hero') { // um den Kronleuchter oben in der Mitte
        p.x = w / 2 + (Math.random() - .5) * Math.min(w, h * 1.3) * .42;
        p.y = h * (.03 + Math.random() * .3);
        p.vx = (Math.random() - .5) * .12; p.vy = .05 + Math.random() * .18;
      } else {
        p.x = Math.random() * w; p.y = init ? Math.random() * h : -10;
        p.vx = .1 + Math.random() * .25; p.vy = .15 + Math.random() * .35;
      }
      p.r = Math.random() * (mode === 'hero' ? 1.6 : 1.3) + .3;
      p.life = 0; p.max = 160 + Math.random() * 260; p.ph = Math.random() * 6.28;
      return p;
    };
    const tick = () => {
      ctx.clearRect(0, 0, w, h);
      ctx.globalCompositeOperation = 'lighter';
      for (const p of parts) {
        p.life++; p.x += p.vx + Math.sin((p.life + p.ph * 40) / 60) * .15; p.y += p.vy;
        const a = Math.sin(Math.PI * p.life / p.max) * (.55 + .45 * Math.sin(p.life / 7 + p.ph));
        if (p.life > p.max || p.y > h + 10 || p.x > w + 10) spawn(p);
        const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 5);
        g.addColorStop(0, `rgba(255,232,170,${a})`); g.addColorStop(.35, `rgba(240,190,100,${a * .45})`); g.addColorStop(1, 'rgba(200,140,60,0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p.x, p.y, p.r * 5, 0, 6.283); ctx.fill();
      }
      if (on) raf = requestAnimationFrame(tick);
    };
    size(); addEventListener('resize', size);
    for (let i = 0; i < N; i++) { const p = spawn({}, true); p.life = Math.random() * p.max; parts.push(p); }
    new IntersectionObserver(([e]) => { on = e.isIntersecting && !reduce; cancelAnimationFrame(raf); if (on) tick(); }).observe(canvas);
  }
  $$('canvas[data-sparks]').forEach(c => { if (!c.closest('.is-missing')) sparks(c, c.dataset.sparks); });

  /* Fortschritt einer Sticky-Strecke: 0 = Bühne oben angekommen, 1 = Ende */
  const prog = sec => { const r = sec.getBoundingClientRect(); const run = r.height - innerHeight; return run > 0 ? clamp(-r.top / run) : clamp(1 - r.bottom / (innerHeight + r.height)); };
  const visible = el => { const r = el.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; };

  /* 2 · Spotlight */
  const spot = $('#location');
  const spotStage = spot && $('.spot__stage', spot);
  let mouse = null, mouseT = 0;
  if (spotStage) {
    const move = (x, y) => { const r = spotStage.getBoundingClientRect(); mouse = { x: (x - r.left) / r.width, y: (y - r.top) / r.height }; mouseT = performance.now(); };
    spotStage.addEventListener('pointermove', e => move(e.clientX, e.clientY));
    spotStage.addEventListener('touchmove', e => { const t = e.touches[0]; move(t.clientX, t.clientY); }, { passive: true });
  }
  let sx = .5, sy = .45;

  /* 3 · Abend / Nacht */
  const split = $('#abend');
  const splitStage = split && $('.split__stage', split);
  let manual = null;
  if (splitStage && !split.classList.contains('is-missing')) {
    const knob = $('.split__knob', split);
    let drag = false;
    const set = x => { const r = splitStage.getBoundingClientRect(); manual = clamp((x - r.left) / r.width, .03, .97); };
    knob.addEventListener('pointerdown', e => { drag = true; knob.setPointerCapture(e.pointerId); set(e.clientX); });
    knob.addEventListener('pointermove', e => { if (drag) set(e.clientX); });
    knob.addEventListener('pointerup', () => { drag = false; });
    splitStage.addEventListener('click', e => { if (e.target !== knob) set(e.clientX); });
    knob.addEventListener('keydown', e => { if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { manual = clamp((manual ?? .5) + (e.key === 'ArrowLeft' ? -.05 : .05), .03, .97); e.preventDefault(); } });
  }

  /* 4 · Garten / 6 · Karaoke */
  const garden = $('#garten');
  const kara = $('#karaoke');
  const lyPaths = $$('.lyrics textPath');

  /* Sticky-CTA (Handy) */
  const cta = $('.sticky-cta');
  const resvSec = $('#reservieren');

  let t0 = performance.now();
  function frame(now) {
    const y = scrollY;
    nav.classList.toggle('is-solid', y > 40);

    // Hero: Text weicht beim Scrollen
    const hp = clamp(y / innerHeight);
    hero.style.setProperty('--hp', hp);
    const ht = $('.hero__text');
    if (ht) { ht.style.opacity = 1 - hp * 1.4; ht.style.translate = `0 ${-hp * 60}px`; }

    // Spotlight
    if (spotStage && visible(spot) && !spot.classList.contains('is-missing')) {
      const p = prog(spot);
      const auto = { x: .5 + Math.sin(p * 5.2 + .6) * .3, y: .42 + Math.sin(p * 3.4) * .12 };
      const useMouse = mouse && now - mouseT < 2600;
      const tx = useMouse ? mouse.x : auto.x, ty = useMouse ? mouse.y : auto.y;
      sx += (tx - sx) * .12; sy += (ty - sy) * .12;
      const base = Math.min(innerWidth, innerHeight) * (touch ? .34 : .26);
      const grow = ease(clamp((p - .72) / .26));
      const r = base + grow * Math.hypot(innerWidth, innerHeight) * 1.4;
      spotStage.style.setProperty('--x', (sx * 100).toFixed(2) + '%');
      spotStage.style.setProperty('--y', (sy * 100).toFixed(2) + '%');
      spotStage.style.setProperty('--r', r.toFixed(0) + 'px');
      $('.spot__hint', spot).style.opacity = 1 - clamp((p - .55) / .2);
    }

    // Abend / Nacht
    if (splitStage && visible(split) && !split.classList.contains('is-missing')) {
      const q = prog(split);
      if (q <= 0.001) manual = null;
      const auto = 1 - .5 * ease(clamp(q / .55));
      const v = manual ?? auto;
      splitStage.style.setProperty('--p', (v * 100).toFixed(2) + '%');
      $('.split__label--r', split).style.opacity = clamp((1 - v) * 4);
      $('.split__label--l', split).style.opacity = clamp(v * 4);
    }

    // Garten: Parallaxe + langsamer Zoom
    if (garden && visible(garden) && !garden.classList.contains('is-missing')) {
      const r = garden.getBoundingClientRect();
      const g = clamp(1 - (r.top + r.height) / (innerHeight + r.height));
      garden.style.setProperty('--py', ((g - .5) * -6) + '%');
      garden.style.setProperty('--gs', (1.14 - g * .1).toFixed(3));
    }

    // Karaoke: Liedzeilen wandern, Bild zoomt leicht
    if (kara && visible(kara) && !kara.classList.contains('is-missing')) {
      const r = kara.getBoundingClientRect();
      const k = clamp(1 - (r.top + r.height) / (innerHeight + r.height));
      kara.style.setProperty('--ks', (1.1 - k * .08).toFixed(3));
      const tt = reduce ? 0 : (now - t0) / 1000;
      lyPaths.forEach((tp, i) => {
        const dir = i % 2 ? 1 : -1;
        const off = ((tt * (1.1 + i * .25) + k * 30) * dir) % 50;
        tp.setAttribute('startOffset', (off - (dir > 0 ? 50 : 0)) + '%');
      });
    }

    // Sticky-CTA
    if (cta) {
      const rr = resvSec.getBoundingClientRect();
      cta.classList.toggle('is-on', y > innerHeight * .8 && !(rr.top < innerHeight && rr.bottom > 0));
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  /* 5 · Bars */
  const bars = $$('.bar:not(.is-missing)');
  const row = $('.bars__row');
  const activate = b => bars.forEach(x => x.classList.toggle('is-active', x === b));
  if (!touch) bars.forEach(b => { b.addEventListener('mouseenter', () => activate(b)); });
  bars.forEach(b => b.addEventListener('click', () => activate(b)));
  if (row) row.addEventListener('mouseleave', () => { if (!touch) activate(bars.find(b => b.dataset.need === 'bar-saal') || bars[0]); });
  const mqPhone = matchMedia('(max-width: 720px)');
  if (row && mqPhone.matches) {
    const mid = bars.find(b => b.dataset.need === 'bar-saal');
    if (mid) requestAnimationFrame(() => { row.scrollLeft = mid.offsetLeft - (row.clientWidth - mid.clientWidth) / 2; });
    let st;
    row.addEventListener('scroll', () => { clearTimeout(st); st = setTimeout(() => {
      const c = row.scrollLeft + row.clientWidth / 2;
      let best = bars[0], d = 1e9;
      bars.forEach(b => { const bc = b.offsetLeft + b.clientWidth / 2; if (Math.abs(bc - c) < d) { d = Math.abs(bc - c); best = b; } });
      activate(best);
    }, 80); }, { passive: true });
  }

  /* Einblenden */
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } }), { threshold: .25 });
  $$('.reveal, .voices').forEach(el => io.observe(el));

  /* 7 · Stimmen (echte Google-Bewertungen, gekürzt) */
  const quotes = [
    ['»Setzt neue Maßstäbe.«', 'Lala S.'],
    ['»Beste Ost-Europa Atmosphäre.«', 'xetra11'],
    ['»Essen schmeckt 10 von 10.«', 'Elina G.'],
    ['»Hausgemacht, frisch und 1A Qualität.«', 'Steffen S.'],
  ];
  const qBox = $('.quote'), qP = $('[data-quote]'), qBy = $('[data-quote-by]');
  let qi = 0;
  if (!reduce) setInterval(() => {
    if (!visible(qBox)) return;
    qBox.classList.add('is-swap');
    setTimeout(() => { qi = (qi + 1) % quotes.length; qP.textContent = quotes[qi][0]; qBy.textContent = quotes[qi][1]; qBox.classList.remove('is-swap'); }, 800);
  }, 5200);

  /* 8 · Reservierung: nur Samstage */
  const selD = $('#resv-datum'), selP = $('#resv-personen');
  const fmt = new Intl.DateTimeFormat('de-DE', { weekday: 'short', day: '2-digit', month: '2-digit', year: 'numeric' });
  const d = new Date(); d.setHours(12, 0, 0, 0);
  d.setDate(d.getDate() + ((6 - d.getDay() + 7) % 7));
  for (let i = 0; i < 10; i++) { const o = document.createElement('option'); o.value = fmt.format(d); o.textContent = fmt.format(d) + (i === 0 ? ' · diesen Samstag' : ''); selD.append(o); d.setDate(d.getDate() + 7); }
  for (let i = 1; i <= 20; i++) { const o = document.createElement('option'); o.value = i; o.textContent = i + (i === 1 ? ' Person' : ' Personen'); if (i === 2) o.selected = true; selP.append(o); }
  { const o = document.createElement('option'); o.value = 'mehr als 20'; o.textContent = 'mehr als 20 Personen'; selP.append(o); }
  $('#resv').addEventListener('submit', e => {
    e.preventDefault();
    const datum = selD.value, pers = selP.value;
    const subj = `Tischreservierung ${datum}, ${pers} ${pers === '1' ? 'Person' : 'Personen'}`;
    const body = `Hallo Dr. Schiwago Team,\n\nich möchte gern einen Tisch reservieren:\n\nDatum: ${datum}\nPersonen: ${pers}\nName: \nTelefon: \n\nVielen Dank!`;
    location.href = `mailto:info@drschiwago.de?subject=${encodeURIComponent(subj)}&body=${encodeURIComponent(body)}`;
  });
})();
