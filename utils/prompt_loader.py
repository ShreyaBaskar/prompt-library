import json
import os

_prompts_cache = None

def load_prompts(filepath=None):
    global _prompts_cache
    if _prompts_cache is not None:
        return _prompts_cache
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), '..', 'data', 'prompts.json')
    with open(filepath, 'r', encoding='utf-8') as f:
        _prompts_cache = json.load(f)
    return _prompts_cache

def get_prompt_by_id(prompt_id):
    prompts = load_prompts()
    for p in prompts:
        if p['id'] == int(prompt_id):
            return p
    return None

def get_all_categories():
    prompts = load_prompts()
    categories = {}
    for p in prompts:
        sub = p.get('subcategory', 'General')
        cat = p.get('category', 'General')
        if sub not in categories:
            categories[sub] = []
        if cat not in categories[sub]:
            categories[sub].append(cat)
    return categories
