const translations = {
  en: {
    home: "Home",
    categories: "Categories",
    search: "Search",
    favourites: "Favourites",
    login: "Login",
    signup: "Sign Up",
    logout: "Logout",
    profile: "Profile",
    explorePrompts: "Explore Prompts",
    searchPrompts: "Search Prompts",
    smartFind: "Smart Find",
    smartFinder: "✦ Smart Prompt Finder",
    keywordSearch: "Keyword Search",
    findPrompts: "Find Prompts",
    copyPrompt: "Copy Prompt",
    featuredPrompts: "Featured Prompts",
    exploreAll: "Explore All Prompts",
    heroSub: "Discover AI prompts for academic work, career growth, and HR communication."
  },
  ta: {
    home: "முகப்பு",
    categories: "வகைகள்",
    search: "தேடல்",
    favourites: "பிடித்தவை",
    login: "உள்நுழை",
    signup: "பதிவு செய்",
    logout: "வெளியேறு",
    profile: "சுயவிவரம்",
    explorePrompts: "தூண்டுதல்களை ஆராயுங்கள்",
    searchPrompts: "தூண்டுதல்களைத் தேடுங்கள்",
    smartFind: "புத்திசாலி தேடல்",
    smartFinder: "✦ புத்திசாலி தூண்டுதல் கண்டுபிடிப்பான்",
    keywordSearch: "முக்கியச்சொல் தேடல்",
    findPrompts: "தூண்டுதல்களைக் கண்டுபிடி",
    copyPrompt: "நகலெடு",
    featuredPrompts: "சிறப்பு தூண்டுதல்கள்",
    exploreAll: "அனைத்து தூண்டுதல்களையும் ஆராயுங்கள்",
    heroSub: "கல்வி, தொழில் வளர்ச்சி மற்றும் HR தொடர்பிற்கான AI தூண்டுதல்களை கண்டறியுங்கள்."
  }
};

let currentLang = localStorage.getItem('lang') || 'en';

function applyTranslations(lang) {
  const t = translations[lang];
  if (!t) return;
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (t[key]) el.textContent = t[key];
  });
  // Update lang indicator
  const indicator = document.getElementById('currentLang');
  if (indicator) indicator.textContent = lang === 'ta' ? 'தமிழ்' : 'EN';
  // Update active buttons
  document.querySelectorAll('.lang-option').forEach(btn => btn.classList.remove('active'));
  const activeBtn = document.getElementById('lang-' + lang);
  if (activeBtn) activeBtn.classList.add('active');
}

function switchLanguage(lang) {
  currentLang = lang;
  localStorage.setItem('lang', lang);
  applyTranslations(lang);
  closeLangDropdown();
}

function closeLangDropdown() {
  const dd = document.getElementById('langDropdown');
  if (dd) dd.classList.remove('open');
}

// Toggle dropdown
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('langBtn');
  const dropdown = document.getElementById('langDropdown');
  if (btn && dropdown) {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      dropdown.classList.toggle('open');
    });
    document.addEventListener('click', () => dropdown.classList.remove('open'));
  }
  applyTranslations(currentLang);
});
