#!/usr/bin/env python3
"""Validate all locale files for JSON syntax and key completeness"""
import json
import os
from pathlib import Path

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

def validate_locale_file(lang_code, en_keys):
    """Validate a single locale file"""
    file_path = Path(f"{lang_code}.json")
    
    if not file_path.exists():
        return False, f"File not found: {file_path}"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Get all keys from this language file
        lang_keys = set(get_all_keys(data))
        
        # Check for missing keys
        missing = en_keys - lang_keys
        extra = lang_keys - en_keys
        
        issues = []
        if missing:
            issues.append(f"Missing {len(missing)} keys")
        if extra:
            issues.append(f"Extra {len(extra)} keys")
        
        if issues:
            return False, "; ".join(issues)
        return True, "All keys present"
        
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, f"Error: {e}"

def main():
    # Load English file as reference
    with open("en.json", 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    en_keys = set(get_all_keys(en_data))
    print(f"English file has {len(en_keys)} keys")
    print()
    
    # Validate all language files
    languages = ['es', 'fr', 'de', 'ja', 'ko', 'pt']
    all_valid = True
    
    for lang in languages:
        valid, message = validate_locale_file(lang, en_keys)
        status = "[OK]" if valid else "[FAIL]"
        print(f"{status} {lang}.json: {message}")
        if not valid:
            all_valid = False
    
    print()
    if all_valid:
        print("[OK] All locale files are valid and complete!")
        return 0
    else:
        print("[FAIL] Some locale files have issues")
        return 1

if __name__ == "__main__":
    exit(main())
