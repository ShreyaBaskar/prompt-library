// Favourites page JS (additional helpers loaded alongside prompt_actions.js)
document.addEventListener('DOMContentLoaded', () => {
  // Animate cards on load
  document.querySelectorAll('.prompt-card').forEach((card, i) => {
    card.style.animationDelay = (i * 0.05) + 's';
    card.classList.add('fade-in');
  });
});
