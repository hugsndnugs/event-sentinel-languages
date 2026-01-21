#!/usr/bin/env python3
"""Generate translation statistics using functions from check_english.py"""
import json
from pathlib import Path
from check_english import (
    get_all_strings,
    is_likely_english_match,
    should_skip_key
)

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
            'missingKeys': []
        }
    
    # Get all string values from target language
    lang_strings = dict(get_all_strings(lang_data))
    
    total = 0
    translated = 0
    untranslated = 0
    missing_keys = []
    
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
            else:
                translated += 1
    
    completeness = f"{((translated / total) * 100):.1f}" if total > 0 else '0.0'
    
    return {
        'total': total,
        'translated': translated,
        'missing': len(missing_keys),
        'untranslated': untranslated,
        'completeness': completeness,
        'missingKeys': missing_keys
    }

def generate_stats():
    """Generate translation statistics for all language files"""
    # Load English as reference
    with open("en.json", 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    en_strings = dict(get_all_strings(en_data))
    
    # Discover all language files dynamically
    locale_dir = Path(".")
    json_files = list(locale_dir.glob("*.json"))
    languages = []
    for json_file in json_files:
        lang_code = json_file.stem  # Get filename without extension
        languages.append(lang_code)
    
    languages.sort()  # Sort for consistent output
    
    stats = {}
    
    for lang_code in languages:
        try:
            with open(f"{lang_code}.json", 'r', encoding='utf-8') as f:
                lang_data = json.load(f)
            
            stats[lang_code] = calculate_stats(lang_code, en_strings, lang_data)
        except FileNotFoundError:
            print(f"[WARN] {lang_code}.json not found, skipping...")
        except json.JSONDecodeError as e:
            print(f"[ERROR] Failed to parse {lang_code}.json: {e}")
    
    # Write stats to JSON file
    with open("translation_stats.json", 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Generated translation_stats.json with statistics for {len(stats)} languages")
    return stats

if __name__ == "__main__":
    generate_stats()
