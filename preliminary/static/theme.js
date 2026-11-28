
document.querySelectorAll('.theme-btn').forEach(btn => {
  btn.addEventListener('click', e => {
    e.preventDefault();
    const theme = btn.getAttribute('href').split('theme=')[1] || '';

    document.body.setAttribute('data-theme', theme);

    // Update .active class
    document.querySelectorAll('.theme-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    // Update URL without reloading
    history.pushState({}, '', '/?theme=' + theme);

    // Update hidden input so video form preserves theme
    const hidden = document.querySelector('input[name="theme"]');
    if (hidden) hidden.value = theme;
  });
});

// Handle browser back/forward
window.addEventListener('popstate', () => {
  const theme = new URLSearchParams(location.search).get('theme') || '';
  document.body.setAttribute('data-theme', theme);
  document.querySelectorAll('.theme-btn').forEach(b => {
    const t = b.getAttribute('href').split('theme=')[1] || '';
    b.classList.toggle('active', t === theme);
  });
});
