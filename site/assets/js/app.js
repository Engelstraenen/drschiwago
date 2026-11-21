/* DR. SCHIWAGO · Goldene Nacht · V2 (Essen zuerst) */
(() => {
  const IMG = window.IMG || {};
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const ease = t => 1 - Math.pow(1 - t, 3);
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const touch = matchMedia('(hover: none)').matches;
  const phone = matchMedia('(max-width: 720px)').matches;

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
    img.sizes = img.closest('.bar, .dress__grid figure, .reel__card, .gal__item, .course__img') ? '(max-width: 720px) 90vw, 50vw' : '100vw';
    img.decoding = 'async';
    if (!img.closest('.hero, .chero')) img.loading = 'lazy';
    img.width = m.w; img.height = m.h;
  });

  /* Nav */
  const nav = $('#nav');
  const burger = $('.nav__burger');
  burger.addEventListener('click', () => { const o = nav.classList.toggle('is-open'); burger.setAttribute('aria-expanded', o); });
  $$('.nav__links a').forEach(a => a.addEventListener('click', () => { nav.classList.remove('is-open'); burger.setAttribute('aria-expanded', false); }));

  /* Hero: Licht geht an */
  const hero = $('.hero, .chero');
  const heroImg = hero && $('img[data-img]', hero);
  const lightUp = () => requestAnimationFrame(() => hero && hero.classList.add('is-lit'));
  if (heroImg && !heroImg.classList.contains('is-missing')) {
    if (heroImg.complete && heroImg.naturalWidth) setTimeout(lightUp, 200);
    else { heroImg.addEventListener('load', () => setTimeout(lightUp, 120), { once: true }); setTimeout(lightUp, 2500); }
  } else lightUp();
  if (hero && !touch && !reduce) hero.addEventListener('pointermove', e => {
    const r = hero.getBoundingClientRect();
    hero.style.setProperty('--mx', (((e.clientX - r.left) / r.width - .5) * -1.6).toFixed(2) + '%');
    hero.style.setProperty('--my', (((e.clientY - r.top) / r.height - .5) * -1.2).toFixed(2) + '%');
  });

  /* Glut (Hero, steigt vom Buffet auf) und Goldstaub (Terrasse) */
  function sparks(canvas, mode) {
    const ctx = canvas.getContext('2d');
    let w, h, dpr, parts = [], on = false, raf;
    const N = mode === 'hero' ? (phone ? 40 : 70) : (phone ? 60 : 110);
    const size = () => { dpr = Math.min(2, devicePixelRatio || 1); w = canvas.clientWidth; h = canvas.clientHeight; canvas.width = w * dpr; canvas.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
    const spawn = (p, init) => {
      if (mode === 'hero') {
        p.x = Math.random() * w; p.y = init ? h * (.3 + Math.random() * .7) : h * (.75 + Math.random() * .3);
        p.vx = (Math.random() - .5) * .25; p.vy = -(.25 + Math.random() * .6);
      } else {
        p.x = Math.random() * w; p.y = init ? Math.random() * h : -10;
        p.vx = .1 + Math.random() * .25; p.vy = .15 + Math.random() * .35;
      }
      p.r = Math.random() * 1.5 + .3;
      p.life = 0; p.max = 160 + Math.random() * 260; p.ph = Math.random() * 6.28;
      return p;
    };
    const tick = () => {
      ctx.clearRect(0, 0, w, h);
      ctx.globalCompositeOperation = 'lighter';
      for (const p of parts) {
        p.life++; p.x += p.vx + Math.sin((p.life + p.ph * 40) / 60) * .18; p.y += p.vy;
        const a = Math.sin(Math.PI * p.life / p.max) * (.55 + .45 * Math.sin(p.life / 7 + p.ph));
        if (p.life > p.max || p.y > h + 10 || p.y < -10 || p.x > w + 10) spawn(p);
        const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 5);
        g.addColorStop(0, `rgba(255,226,160,${a})`); g.addColorStop(.35, `rgba(245,170,80,${a * .45})`); g.addColorStop(1, 'rgba(200,120,40,0)');
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
  const pass = sec => { const r = sec.getBoundingClientRect(); return clamp(1 - (r.top + r.height) / (innerHeight + r.height)); };
  const visible = el => { const r = el.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; };
  const scrollToFrac = (sec, f) => { const top = sec.getBoundingClientRect().top + scrollY; scrollTo({ top: top + (sec.offsetHeight - innerHeight) * f, behavior: reduce ? 'auto' : 'smooth' }); };

  /* BUFFET: Szenen */
  const feast = $('#buffet');
  let F = null;
  if (feast) {
    const scenes = $$('.feast__scene', feast), texts = $$('.feast__text', feast), btns = $$('.feast__nav button', feast);
    const keep = scenes.map(s => !s.classList.contains('is-missing'));
    const S = scenes.filter((_, i) => keep[i]), T = texts.filter((_, i) => keep[i]), B = btns.filter((_, i) => keep[i]);
    texts.forEach((t, i) => { if (!keep[i]) t.remove(); }); btns.forEach((b, i) => { if (!keep[i]) b.remove(); });
    if (S.length) {
      $('.feast__nav', feast).style.gridTemplateColumns = `repeat(${S.length}, 1fr)`;
      const INTRO = .7, U = INTRO + S.length;
      F = { S, T, B, U, INTRO, count: $('[data-count]', feast), k: -2 };
      B.forEach((b, i) => b.addEventListener('click', () => scrollToFrac(feast, (INTRO + i + .12) / U)));
    } else feast.classList.add('is-missing');
  }

  /* ECHTE FOTOS: horizontale Fahrt */
  const reel = $('#fotos');
  const track = reel && $('.reel__track', reel);
  if (reel && !$$('.reel__card:not(.is-missing)', reel).length) reel.classList.add('is-missing');

  /* Tag / Nacht */
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

  const garden = $('#terrasse');
  const kara = $('#karaoke');
  const lyPaths = $$('.lyrics textPath');
  const cater = $('#catering');
  const fin = $('.final');
  const cta = $('.sticky-cta');
  const resvSec = $('#reservieren');
  const heroText = $('.hero__text, .chero__text');

  const t0 = performance.now();
  function frame(now) {
    const y = scrollY;
    nav.classList.toggle('is-solid', y > 40);

    if (hero && heroText) {
      const hp = clamp(y / innerHeight);
      heroText.style.opacity = 1 - hp * 1.5; heroText.style.translate = `0 ${-hp * 70}px`;
    }

    // Buffet-Szenen
    if (F && visible(feast)) {
      const x = prog(feast) * F.U;
      const ix = clamp(x / F.INTRO);
      feast.style.setProperty('--io', (.72 * (1 - ease(clamp((ix - .55) / .45)))).toFixed(3));
      feast.style.setProperty('--iv', (1 - ease(clamp((ix - .7) / .3))).toFixed(3));
      feast.style.setProperty('--ic', (1 + ix * .18).toFixed(3));
      if (F.count) F.count.textContent = Math.round(50 * ease(clamp(ix / .75)));
      feast.style.setProperty('--nv', ease(clamp((x - .55) / .3)).toFixed(3));
      let k = x >= .55 ? 0 : -1;
      F.S.forEach((s, i) => {
        const st = F.INTRO + i;
        if (i > 0) {
          const t = clamp((x - st + .42) / .42), r = t * t * (3 - 2 * t); // langsam rein, langsam raus
          s.style.setProperty('--r', (r * 100).toFixed(2) + '%');
          if (r >= .45) k = i; // Text wechselt, wenn das neue Gericht das Bild zur Hälfte füllt
        }
        s.style.setProperty('--s', (1.16 - .14 * clamp((x - st + .42) / 1.42)).toFixed(4));
        F.B[i].querySelector('i').style.setProperty('--f', clamp(x - st + .2).toFixed(3));
      });
      if (k !== F.k) { F.k = k; F.T.forEach((t, i) => t.classList.toggle('is-on', i === k)); F.B.forEach((b, i) => b.classList.toggle('is-on', i === k)); }
    }

    // Fotos: horizontal
    if (track && visible(reel)) {
      const p = prog(reel);
      const max = Math.max(0, track.scrollWidth - innerWidth);
      track.style.setProperty('--tx', (-max * p).toFixed(1) + 'px');
    }

    // Tag / Nacht
    if (splitStage && visible(split) && !split.classList.contains('is-missing')) {
      const q = prog(split);
      if (q <= 0.001) manual = null;
      const auto = 1 - .5 * ease(clamp(q / .55));
      const v = manual ?? auto;
      splitStage.style.setProperty('--p', (v * 100).toFixed(2) + '%');
      $('.split__label--r', split).style.opacity = clamp((1 - v) * 4);
      $('.split__label--l', split).style.opacity = clamp(v * 4);
      $('.split__hint', split).style.opacity = manual === null && q > .45 ? 1 : 0;
    }

    if (garden && visible(garden) && !garden.classList.contains('is-missing')) {
      const g = pass(garden);
      garden.style.setProperty('--py', ((g - .5) * -6) + '%');
      garden.style.setProperty('--gs', (1.14 - g * .1).toFixed(3));
    }

    if (kara && visible(kara) && !kara.classList.contains('is-missing')) {
      const k = pass(kara);
      kara.style.setProperty('--ks', (1.1 - k * .08).toFixed(3));
      const tt = reduce ? 0 : (now - t0) / 1000;
      lyPaths.forEach((tp, i) => {
        const dir = i % 2 ? 1 : -1;
        const off = ((tt * (1.1 + i * .25) + k * 30) * dir) % 50;
        tp.setAttribute('startOffset', (off - (dir > 0 ? 50 : 0)) + '%');
      });
    }

    if (cater && visible(cater)) cater.style.setProperty('--cy', ((pass(cater) - .5) * -8).toFixed(2) + '%');
    if (fin && visible(fin)) fin.style.setProperty('--fs', (1.14 - pass(fin) * .12).toFixed(3));

    if (cta && resvSec) {
      const rr = resvSec.getBoundingClientRect();
      cta.classList.toggle('is-on', y > innerHeight * .8 && !(rr.top < innerHeight && rr.bottom > 0));
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  /* Bars */
  const bars = $$('.bar:not(.is-missing)');
  const row = $('.bars__row');
  const activate = b => bars.forEach(x => x.classList.toggle('is-active', x === b));
  if (!touch) bars.forEach(b => b.addEventListener('mouseenter', () => activate(b)));
  bars.forEach(b => b.addEventListener('click', () => activate(b)));
  if (row) row.addEventListener('mouseleave', () => { if (!touch) activate(bars.find(b => b.dataset.need === 'bar-saal') || bars[0]); });
  if (row && phone) {
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

  /* Feiern: Anlass wählen */
  const evs = $$('.ev');
  if (evs.length) {
    const D = [
      ['Hochzeiten', 'Vom Sektempfang in der Lounge bis zur Tanzfläche im großen Saal, mit bis zu 200 Gästen und unserer Küche.', 'Hochzeit'],
      ['Geburtstage & Jubiläen', 'Runde Geburtstage und Jubiläen im großen Kreis oder mit der Familie. Raum, Buffet und Musik stimmen wir auf Ihre Feier ab.', 'Geburtstag'],
      ['Firmen- & Weihnachtsfeiern', 'Weihnachtsfeiern, Firmenjubiläen und Sommerfeste mit vollem Service, gut erreichbar aus Duisburg und Düsseldorf.', 'Firmenveranstaltung'],
      ['Taufe, Verlobung, Familienfest', 'Verlobungen, Taufen und Abschlussfeiern im kleineren Rahmen, mit persönlicher Betreuung.', 'Familienfest'],
    ];
    const pics = $$('.evp');
    const title = $('[data-ev-title]'), text = $('[data-ev-text]'), link = $('[data-ev-link]');
    let cur = 0, touched = false;
    const show = i => {
      cur = i;
      evs.forEach((b, j) => { b.classList.toggle('is-on', j === i); b.setAttribute('aria-selected', j === i); });
      const okPics = pics.filter(p => !p.classList.contains('is-missing'));
      const pic = pics[i] && !pics[i].classList.contains('is-missing') ? pics[i] : okPics[i % Math.max(1, okPics.length)];
      pics.forEach(p => p.classList.toggle('is-on', p === pic));
      title.textContent = D[i][0]; text.textContent = D[i][1];
      link.href = 'https://www.angerhof-duisburg.de/angebot?anlass=' + encodeURIComponent(D[i][2]);
    };
    evs.forEach((b, i) => { b.addEventListener('click', () => { touched = true; show(i); }); if (!touch) b.addEventListener('mouseenter', () => { touched = true; show(i); }); });
    show(0);
    const stage = $('.events__stage');
    if (!reduce) setInterval(() => { if (!touched && visible(stage)) show((cur + 1) % D.length); }, 4200);
  }

  /* Instagram: neue Videos automatisch über Feed (Behold), sonst offizielle Einbettung der letzten Reels */
  const igRow = $('[data-ig-row]');
  if (igRow) {
    const embed = () => {
      if (window.instgrm) { window.instgrm.Embeds.process(); return; }
      const sc = document.createElement('script'); sc.async = true; sc.src = 'https://www.instagram.com/embed.js'; document.body.append(sc);
    };
    const feed = (window.DRS_IG_FEED || '').trim();
    const esc = x => String(x || '').replace(/[<>&"]/g, '');
    const go = () => {
      if (!feed) return embed();
      fetch(feed).then(r => r.json()).then(d => {
        const posts = (d.posts || d || []).slice(0, 8);
        if (!posts.length) return embed();
        igRow.innerHTML = posts.map(p => {
          const vid = p.mediaType === 'VIDEO' && p.mediaUrl;
          const thumb = p.thumbnailUrl || (p.sizes && p.sizes.medium && p.sizes.medium.mediaUrl) || p.mediaUrl;
          const media = vid ? '<video src="' + esc(vid) + '" poster="' + esc(thumb) + '" muted loop playsinline preload="none"></video>' : '<img src="' + esc(thumb) + '" alt="" loading="lazy">';
          return '<a class="igf" href="' + esc(p.permalink) + '" target="_blank" rel="noopener">' + media + '<span>' + esc(p.prunedCaption || p.caption) + '</span></a>';
        }).join('');
        const vio = new IntersectionObserver(es => es.forEach(e => { const v = e.target; if (e.isIntersecting) v.play().catch(() => {}); else v.pause(); }), { threshold: .5 });
        $$('video', igRow).forEach(v => vio.observe(v));
      }).catch(embed);
    };
    const iio = new IntersectionObserver(([e]) => { if (e.isIntersecting) { go(); iio.disconnect(); } }, { rootMargin: '600px 0px' });
    iio.observe(igRow);
  }

  /* Zähler */
  const fmtN = new Intl.NumberFormat('de-DE');
  const countUp = el => {
    const to = +el.dataset.to, suf = el.dataset.suffix || '', t1 = performance.now(), dur = 1700;
    const step = n => { const t = clamp((n - t1) / dur); el.textContent = fmtN.format(Math.round(to * ease(t))) + suf; if (t < 1) requestAnimationFrame(step); };
    reduce ? (el.textContent = fmtN.format(to) + suf) : requestAnimationFrame(step);
  };
  const cio = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { countUp(e.target); cio.unobserve(e.target); } }), { threshold: .4 });
  $$('[data-to]').forEach(el => cio.observe(el));

  /* Einblenden */
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } }), { threshold: .2 });
  $$('.reveal, .voices').forEach(el => io.observe(el));

  /* Lightbox für echte Fotos */
  const lb = $('#lightbox');
  if (lb) {
    const lbImg = $('img', lb), lbCap = $('.lightbox__cap', lb);
    const close = () => { lb.classList.remove('is-on'); setTimeout(() => { lb.hidden = true; }, 300); };
    $$('.reel__card, .gal__item').forEach(c => c.addEventListener('click', () => {
      const m = IMG[$('img', c).dataset.img]; if (!m) return;
      lbImg.src = m.l; lbImg.alt = $('img', c).alt; lbCap.textContent = ($('figcaption', c) || {}).textContent || '';
      lb.hidden = false; requestAnimationFrame(() => lb.classList.add('is-on'));
    }));
    lb.addEventListener('click', e => { if (e.target !== lbImg) close(); });
    addEventListener('keydown', e => { if (e.key === 'Escape' && !lb.hidden) close(); });
  }

  /* Stimmen (echte Google-Bewertungen, gekürzt) */
  const qBox = $('.quote');
  if (qBox) {
    const quotes = [
      ['»Setzt neue Maßstäbe.«', 'Lala S.'],
      ['»Beste Ost-Europa Atmosphäre.«', 'xetra11'],
      ['»Essen schmeckt 10 von 10.«', 'Elina G.'],
      ['»Hausgemacht, frisch und 1A Qualität.«', 'Steffen S.'],
    ];
    const qP = $('[data-quote]'), qBy = $('[data-quote-by]');
    let qi = 0;
    if (!reduce) setInterval(() => {
      if (!visible(qBox)) return;
      qBox.classList.add('is-swap');
      setTimeout(() => { qi = (qi + 1) % quotes.length; qP.textContent = quotes[qi][0]; qBy.textContent = quotes[qi][1]; qBox.classList.remove('is-swap'); }, 800);
    }, 5200);
  }

  /* Reservierung: nur Samstage */
  const selD = $('#resv-datum'), selP = $('#resv-personen');
  if (selD && selP) {
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
  }
})();
