// Mobile nav
const t = document.querySelector('.nav-toggle'), n = document.getElementById('nav');
if (t && n) t.addEventListener('click', () => {
  const open = n.classList.toggle('open');
  t.setAttribute('aria-expanded', open);
  document.body.style.overflow = open ? 'hidden' : '';
});
// Reveal on scroll
const io = 'IntersectionObserver' in window && new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
}), { rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.reveal').forEach(el => io ? io.observe(el) : el.classList.add('in'));
// Project filters
const btns = document.querySelectorAll('.filters button');
btns.forEach(b => b.addEventListener('click', () => {
  btns.forEach(x => x.setAttribute('aria-pressed', x === b));
  const f = b.dataset.filter;
  document.querySelectorAll('#gallery figure').forEach(fig =>
    fig.classList.toggle('hidden', f !== 'all' && fig.dataset.cat !== f));
}));
