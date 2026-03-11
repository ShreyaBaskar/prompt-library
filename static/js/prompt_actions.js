// Toast notification
function showToast(msg, duration = 2500) {
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    toast.className = 'toast hidden';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.remove('hidden');
  setTimeout(() => toast.classList.add('hidden'), duration);
}

// Copy prompt via API
function copyPrompt(promptId, btn) {
  fetch('/api/copy-prompt', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({prompt_id: promptId})
  })
  .then(r => r.json())
  .then(data => {
    if (data.limit_reached) {
      showToast('Guest limit reached. Please log in for unlimited access.', 4000);
      const warn = document.getElementById('guestWarning');
      if (warn) { warn.classList.remove('hidden'); document.getElementById('guestCount').textContent = 0; }
      return;
    }
    if (data.success) {
      navigator.clipboard.writeText(data.template).then(() => {
        showToast('✓ Prompt copied to clipboard!');
        if (btn) {
          const orig = btn.innerHTML;
          btn.innerHTML = '✓ Copied!';
          btn.style.background = '#000066';
          btn.style.color = '#fff';
          setTimeout(() => { btn.innerHTML = orig; btn.style = ''; }, 1800);
        }
        if (data.remaining !== null && data.remaining !== undefined) {
          updateGuestWarning(data.remaining);
        }
      }).catch(() => {
        showToast('Copy failed — try again.');
      });
    }
  })
  .catch(() => showToast('Something went wrong.'));
}

function updateGuestWarning(remaining) {
  const warn = document.getElementById('guestWarning');
  const count = document.getElementById('guestCount');
  if (!warn) return;
  if (remaining <= 0) {
    if (count) count.textContent = 0;
    warn.classList.remove('hidden');
  } else if (remaining < 5) {
    if (count) count.textContent = remaining;
    warn.classList.remove('hidden');
  }
}

// Toggle favourite
function toggleFav(promptId, btn) {
  fetch('/api/toggle-favourite', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({prompt_id: promptId})
  })
  .then(r => {
    if (r.status === 401) {
      window.location.href = '/login';
      return null;
    }
    return r.json();
  })
  .then(data => {
    if (!data) return;
    if (data.success) {
      if (data.action === 'added') {
        btn.textContent = '♥';
        btn.classList.add('fav-active');
        showToast('Added to favourites ♥');
      } else {
        btn.textContent = '♡';
        btn.classList.remove('fav-active');
        showToast('Removed from favourites');
        // If on favourites page, remove card
        const card = btn.closest('.prompt-card');
        if (card && window.location.pathname === '/favourites') {
          card.style.opacity = '0';
          setTimeout(() => card.remove(), 300);
        }
      }
    }
  })
  .catch(() => showToast('Something went wrong.'));
}
