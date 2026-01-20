#!/usr/bin/env python3
"""Check that placeholders are preserved in all locale files"""
import json
import re
from pathlib import Path

def find_placeholders(text):
    """Find all {placeholder} patterns in text"""
    return re.findall(r'\{(\w+)\}', text)

def get_all_strings(d, prefix=''):
    """Get all string values from nested dict"""
    strings = []
    for k, v in d.items():
        key_path = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            strings.extend(get_all_strings(v, key_path))
        elif isinstance(v, str):
            strings.append((key_path, v))
    return strings

def check_placeholders():
    """Check placeholders across all locale files"""
    # Load English as reference
    with open("en.json", 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    en_strings = dict(get_all_strings(en_data))
    
    # Get placeholders from English
    en_placeholders = {}
    for key, value in en_strings.items():
        placeholders = find_placeholders(value)
        if placeholders:
            en_placeholders[key] = set(placeholders)
    
    languages = ['es', 'fr', 'de', 'ja', 'ko', 'pt']
    all_ok = True
    
    for lang in languages:
        with open(f"{lang}.json", 'r', encoding='utf-8') as f:
            lang_data = json.load(f)
        
        lang_strings = dict(get_all_strings(lang_data))
        issues = []
        
        for key, en_ph in en_placeholders.items():
            if key in lang_strings:
                lang_ph = set(find_placeholders(lang_strings[key]))
                if lang_ph != en_ph:
                    issues.append(f"{key}: missing {en_ph - lang_ph}, extra {lang_ph - en_ph}")
        
        if issues:
            print(f"[FAIL] {lang}.json has placeholder issues:")
            for issue in issues[:5]:  # Show first 5
                print(f"  - {issue}")
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more")
            all_ok = False
        else:
            print(f"[OK] {lang}.json: All placeholders preserved")
    
    return all_ok

if __name__ == "__main__":
    if check_placeholders():
        print("\n[OK] All placeholders are correctly preserved!")
        exit(0)
    else:
        print("\n[FAIL] Some placeholders are missing or incorrect")
        exit(1)
