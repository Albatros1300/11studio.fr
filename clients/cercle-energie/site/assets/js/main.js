// Cercle Énergie — interactions du site de démonstration
(() => {
  // menu mobile
  const burger = document.querySelector('.burger');
  const nav = document.querySelector('.nav');
  if (burger && nav) {
    burger.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', String(open));
    });
  }

  // apparition au défilement
  const items = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      }
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    items.forEach((el) => io.observe(el));
  } else {
    items.forEach((el) => el.classList.add('in'));
  }

  // formulaire partenaire (démo : aucune donnée n'est envoyée)
  const form = document.getElementById('lead-form');
  if (form) {
    form.addEventListener('submit', (ev) => {
      ev.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      document.getElementById('form-ok').classList.add('on');
      form.querySelector('button[type=submit]').disabled = true;
    });
  }
})();
