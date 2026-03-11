// Live search debounce
const searchInput = document.querySelector('.smart-input, .hero-input');
if (searchInput) {
  let debounceTimer;
  searchInput.addEventListener('input', function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      // Could trigger live search preview in future
    }, 300);
  });
}
