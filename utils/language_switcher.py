# Backend language utility (not used directly - JS handles UI translation)
TRANSLATIONS = {
    'en': {
        'home': 'Home',
        'categories': 'Categories',
        'search': 'Search',
        'favourites': 'Favourites',
        'login': 'Login',
        'signup': 'Sign Up',
    },
    'ta': {
        'home': 'முகப்பு',
        'categories': 'வகைகள்',
        'search': 'தேடல்',
        'favourites': 'பிடித்தவை',
        'login': 'உள்நுழை',
        'signup': 'பதிவு செய்',
    }
}

def get_translation(lang, key):
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)
