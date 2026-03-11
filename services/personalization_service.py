from utils.placeholder_replacer import replace_placeholders
from utils.prompt_loader import load_prompts

def personalize_prompt(template, user):
    profile = {
        'name': getattr(user, 'name', '') or '',
        'department': getattr(user, 'department', '') or '',
        'year': getattr(user, 'year', '') or '',
        'college': getattr(user, 'college', '') or '',
    }
    return replace_placeholders(template, profile)

def find_best_template(role, category, description):
    """Find the best matching prompt template based on user inputs."""
    prompts = load_prompts()
    query = f"{role} {category} {description}".lower()
    
    best_match = None
    best_score = 0
    
    for p in prompts:
        score = 0
        searchable = f"{p['title']} {p['category']} {p['subcategory']} {' '.join(p.get('tags', []))}".lower()
        
        # Score based on keyword overlap
        for word in query.split():
            if word in searchable:
                score += 1
        
        # Category match bonus
        if category.lower() in searchable:
            score += 3
            
        if score > best_score:
            best_score = score
            best_match = p
    
    return best_match
