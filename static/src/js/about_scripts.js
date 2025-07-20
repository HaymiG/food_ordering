// static/src/js/about_scripts.js

document.addEventListener('DOMContentLoaded', () => {
  const heading = document.querySelector('.section-about h1');
  if (heading) {
    heading.style.transition = 'color 1s ease-in-out';
    setTimeout(() => {
      heading.style.color = '#e67e22';
    }, 500);
  }
});
