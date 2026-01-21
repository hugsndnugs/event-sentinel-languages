#!/usr/bin/env python3
"""Validate all locale files for JSON syntax and key completeness"""
import json
import os
from pathlib import Path
from check_english import (
    get_all_strings,
    is_likely_english_match,
    should_skip_key
)

def get_all_keys(d, prefix=''):
    """Recursively get all keys from a nested dictionary"""
    keys = []
    for k, v in d.items():
        key_path = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            keys.extend(get_all_keys(v, key_path))
        else:
            keys.append(key_path)
    return keys

def validate_locale_file(lang_code, en_keys, en_strings):
    """Validate a single locale file"""
    file_path = Path(f"{lang_code}.json")
    
    if not file_path.exists():
        return False, f"File not found: {file_path}", [], []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Get all keys from this language file
        lang_keys = set(get_all_keys(data))
        
        # Get all string values from this language file
        lang_strings = dict(get_all_strings(data))
        
        # Check for missing keys (keys that don't exist in the translation file)
        missing_keys = sorted(list(en_keys - lang_keys))
        
        # Check for extra keys (keys in translation but not in English)
        extra_keys = sorted(list(lang_keys - en_keys))
        
        # Check for English stubs (keys that exist but match English values)
        untranslated_keys = []
        for key, en_value in en_strings.items():
            # Skip if key is missing (already handled above)
            if key not in lang_strings:
                continue
            
            # Skip keys that should be excluded from English detection
            if should_skip_key(key, en_value):
                continue
            
            # Check if the translation matches English
            lang_value = lang_strings[key]
            is_match, _ = is_likely_english_match(en_value, lang_value)
            
            if is_match:
                untranslated_keys.append(key)
        
        untranslated_keys = sorted(untranslated_keys)
        
        # Build issues list
        issues = []
        if missing_keys:
            issues.append(f"Missing {len(missing_keys)} keys")
        if untranslated_keys:
            issues.append(f"{len(untranslated_keys)} untranslated (English stubs)")
        if extra_keys:
            issues.append(f"Extra {len(extra_keys)} keys")
        
        if issues:
            return False, "; ".join(issues), missing_keys, untranslated_keys
        return True, "All keys present and translated", [], []
        
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}", [], []
    except Exception as e:
        return False, f"Error: {e}", [], []

def main():
    # Load English file as reference
    with open("en.json", 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    en_keys = set(get_all_keys(en_data))
    en_strings = dict(get_all_strings(en_data))
    print(f"English file has {len(en_keys)} keys")
    print()
    
    # Discover all language files dynamically
    locale_dir = Path(".")
    json_files = list(locale_dir.glob("*.json"))
    languages = []
    excluded_files = {"en", "translation_stats"}  # Exclude reference and generated files
    for json_file in json_files:
        lang_code = json_file.stem  # Get filename without extension
        if lang_code not in excluded_files:
            languages.append(lang_code)
    
    if not languages:
        print("[WARN] No language files found (except en.json)")
        return 0
    
    languages.sort()  # Sort for consistent output
    all_valid = True
    
    for lang in languages:
        valid, message, missing_keys, untranslated_keys = validate_locale_file(lang, en_keys, en_strings)
        status = "[OK]" if valid else "[FAIL]"
        print(f"{status} {lang}.json: {message}")
        
        # Show detailed information for failed validations
        if not valid:
            all_valid = False
            if missing_keys:
                # Show first 5 missing keys as examples
                examples = missing_keys[:5]
                example_str = ", ".join(examples)
                if len(missing_keys) > 5:
                    example_str += f", ... ({len(missing_keys) - 5} more)"
                print(f"  - Missing {len(missing_keys)} keys: {example_str}")
            
            if untranslated_keys:
                # Show first 5 untranslated keys as examples
                examples = untranslated_keys[:5]
                example_str = ", ".join(examples)
                if len(untranslated_keys) > 5:
                    example_str += f", ... ({len(untranslated_keys) - 5} more)"
                print(f"  - Untranslated {len(untranslated_keys)} keys (English stubs): {example_str}")
    
    print()
    if all_valid:
        print("[OK] All locale files are valid and complete!")
        return 0
    else:
        print("[FAIL] Some locale files have issues")
        return 1

if __name__ == "__main__":
    exit(main())
