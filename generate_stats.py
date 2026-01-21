#!/usr/bin/env python3
"""Generate translation statistics using functions from check_english.py"""
import json
from pathlib import Path
from check_english import (
    get_all_strings,
    is_likely_english_match,
    should_skip_key
)

def deep_merge(main, develop):
    """Merge develop branch data into main, with develop taking precedence"""
    # If develop is None/empty, return main
    if not develop:
        return main
    # If main is None/empty, return develop
    if not main:
        return develop
    
    # If develop is not a dict or is a list, return develop (develop takes precedence)
    if not isinstance(develop, dict) or isinstance(develop, list):
        return develop
    
    # If main is not a dict or is a list, return develop
    if not isinstance(main, dict) or isinstance(main, list):
        return develop
    
    # Merge dictionaries recursively
    merged = main.copy()
    for key, develop_value in develop.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(develop_value, dict):
            # Recursively merge nested objects
            merged[key] = deep_merge(merged[key], develop_value)
        else:
            # develop takes precedence for non-object values or when types don't match
            merged[key] = develop_value
    
    return merged

def calculate_stats(lang_code, en_strings, lang_data):
    """Calculate translation statistics for a language"""
    if lang_code == 'en':
        # For English, return 100% as it's the reference
        en_strings_list = list(en_strings.items())
        return {
            'total': len(en_strings_list),
            'translated': len(en_strings_list),
            'missing': 0,
            'untranslated': 0,
            'completeness': '100.0',
            'missingKeys': [],
            'untranslatedKeys': []
        }
    
    # Get all string values from target language
    lang_strings = dict(get_all_strings(lang_data))
    
    total = 0
    translated = 0
    untranslated = 0
    missing_keys = []
    untranslated_keys = []
    
    # Compare each English string with the translation
    for key, en_value in en_strings.items():
        # Skip keys that should be excluded
        if should_skip_key(key, en_value):
            continue
        
        total += 1
        
        if key not in lang_strings:
            # Key is missing
            missing_keys.append(key)
        else:
            lang_value = lang_strings[key]
            # Check if translation matches English
            is_match, _ = is_likely_english_match(en_value, lang_value)
            
            if is_match:
                untranslated += 1
                untranslated_keys.append(key)
            else:
                translated += 1
    
    completeness = f"{((translated / total) * 100):.1f}" if total > 0 else '0.0'
    
    return {
        'total': total,
        'translated': translated,
        'missing': len(missing_keys),
        'untranslated': untranslated,
        'completeness': completeness,
        'missingKeys': missing_keys,
        'untranslatedKeys': untranslated_keys
    }

def load_language_file(branch, lang_code):
    """Load a language file from a specific branch"""
    try:
        # Try to read from branch-specific path
        # In workflow, we'll have both branches checked out
        path = f"{branch}/{lang_code}.json" if Path(f"{branch}/{lang_code}.json").exists() else f"{lang_code}.json"
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"[WARN] Failed to parse {lang_code}.json from {branch}: {e}")
        return None

def generate_stats():
    """Generate translation statistics for all language files, merging main and develop branches"""
    # Load English as reference (from current branch, should be same in both)
    en_data = None
    for branch in ['main', 'develop', '.']:
        en_data = load_language_file(branch, 'en')
        if en_data:
            break
    
    if not en_data:
        print("[ERROR] Could not load en.json from any branch")
        return {}
    
    en_strings = dict(get_all_strings(en_data))
    
    # Get list of all language files to check
    language_files = ['en', 'de', 'es', 'fr', 'ja', 'ko', 'pt']
    
    stats = {}
    
    for lang_code in language_files:
        # Load from both branches
        main_data = load_language_file('main', lang_code)
        develop_data = load_language_file('develop', lang_code)
        
        # If neither exists, try current directory
        if not main_data and not develop_data:
            main_data = load_language_file('.', lang_code)
        
        # Merge data (develop takes precedence)
        lang_data = deep_merge(main_data, develop_data) if main_data or develop_data else None
        
        if lang_data:
            stats[lang_code] = calculate_stats(lang_code, en_strings, lang_data)
        else:
            print(f"[WARN] {lang_code}.json not found in main or develop branches, skipping...")
    
    # Write stats to JSON file
    with open("translation_stats.json", 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Generated translation_stats.json with statistics for {len(stats)} languages")
    return stats

if __name__ == "__main__":
    generate_stats()
