// Cercle Énergie — interactions du site de démonstration
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // menu mobile
  const burger = $('.burger'), nav = $('.nav');
  if (burger && nav) burger.addEventListener('click', () => {
    burger.setAttribute('aria-expanded', String(nav.classList.toggle('open')));
  });
  $$('.nav a').forEach((l) => l.addEventListener('click', () => { nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }));

  // apparition au défilement
  const items = $$('.rv');
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    items.forEach((el) => io.observe(el));
  } else items.forEach((el) => el.classList.add('in'));

  // texte qui se remplit au défilement
  const fill = $('[data-fill]');
  let words = [];
  if (fill) {
    const green = +fill.dataset.green || 0;
    const list = fill.textContent.trim().split(/\s+/);
    fill.innerHTML = list.map((w, i) => `<span class="w${i >= green && i < green + 6 ? ' g' : ''}">${w}</span>`).join(' ');
    words = $$('.w', fill);
    if (reduce) words.forEach((w) => w.classList.add('on'));
  }

  // étapes de service
  const steps = $$('.s2'), rail = $('#rail'), fillbar = $('#fillbar'), bigno = $('#bigno');
  const header = $('.site-header'), progress = $('#progress');
  let lastY = 0;

  const onScroll = () => {
    const y = scrollY, vh = innerHeight;
    if (progress) progress.style.transform = `scaleX(${y / Math.max(1, document.documentElement.scrollHeight - vh)})`;
    if (header) { header.classList.toggle('hide', y > lastY && y > 500 && !nav.classList.contains('open')); lastY = y; }
    if (fill && !reduce) {
      const r = fill.getBoundingClientRect();
      const p = Math.min(1, Math.max(0, (vh * 0.85 - r.top) / (r.height + vh * 0.35)));
      const n = Math.round(p * words.length);
      words.forEach((w, i) => w.classList.toggle('on', i < n));
    }
    if (rail) {
      const r = rail.getBoundingClientRect();
      const p = Math.min(1, Math.max(0, (vh * 0.55 - r.top) / r.height));
      fillbar.style.height = p * 100 + '%';
      let act = 0;
      steps.forEach((s, i) => { if (s.getBoundingClientRect().top < vh * 0.6) act = i; });
      steps.forEach((s, i) => s.classList.toggle('act', i <= act));
      if (bigno) bigno.textContent = steps[act].dataset.n;
    }
  };
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll);
  onScroll();

  // comparateur sans / avec
  const sw = $('#switch'), cmp = $('#compare');
  if (sw) {
    const knob = $('.knob', sw), btns = $$('button', sw);
    const set = (b) => {
      btns.forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      knob.style.left = b.offsetLeft + 'px'; knob.style.width = b.offsetWidth + 'px';
      const on = b.dataset.v === 'avec';
      sw.classList.toggle('with', on); cmp.classList.toggle('with-on', on);
    };
    btns.forEach((b) => b.addEventListener('click', () => set(b)));
    const init = () => set(btns.find((b) => b.getAttribute('aria-pressed') === 'true'));
    document.fonts ? document.fonts.ready.then(init) : init();
    addEventListener('resize', init);
    // bascule automatique à la première apparition
    if ('IntersectionObserver' in window && !reduce) {
      const o = new IntersectionObserver((es) => { if (es[0].isIntersecting) { setTimeout(() => set(btns[1]), 1100); o.disconnect(); } }, { threshold: 0.6 });
      o.observe(cmp);
    }
  }

  // panneaux secteurs
  const panels = $$('.panel');
  const open = (p) => panels.forEach((x) => x.classList.toggle('on', x === p));
  panels.forEach((p) => {
    p.addEventListener('mouseenter', () => open(p));
    p.addEventListener('click', () => open(p));
    p.addEventListener('focus', () => open(p));
  });

  // formulaire partenaire (démo : aucune donnée n'est envoyée)
  const form = $('#lead-form');
  if (form) form.addEventListener('submit', (ev) => {
    ev.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    $('#form-ok').classList.add('on');
    $('button[type=submit]', form).disabled = true;
  });
})();
