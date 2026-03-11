from utils.prompt_loader import load_prompts

def keyword_search(query, category=None):
    prompts = load_prompts()
    query_lower = query.lower().strip()
    results = []
    for p in prompts:
        if category and p.get('category') != category and p.get('subcategory') != category:
            continue
        searchable = ' '.join([
            p.get('title', ''),
            p.get('category', ''),
            p.get('subcategory', ''),
            p.get('preview', ''),
            ' '.join(p.get('tags', [])),
            p.get('use_case', '')
        ]).lower()
        if query_lower in searchable:
            results.append(p)
    return results

def filter_by_category(category):
    prompts = load_prompts()
    return [p for p in prompts if p.get('category') == category or p.get('subcategory') == category]
