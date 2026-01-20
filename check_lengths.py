#!/usr/bin/env python3
"""Check if any translations exceed Discord's character limits"""
import json
from pathlib import Path

DISCORD_LIMITS = {
    "embed_title": 256,
    "embed_description": 4096,
    "field_name": 256,
    "field_value": 1024,
    "footer_text": 2048,
}

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

def check_lengths():
    """Check string lengths against Discord limits"""
    languages = ['en', 'es', 'fr', 'de', 'ja', 'ko', 'pt']
    issues = []
    
    for lang in languages:
        with open(f"{lang}.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        strings = get_all_strings(data)
        
        for key, value in strings:
            length = len(value)
            # Most strings are field values or titles
            if length > 1024:
                issues.append(f"{lang}.json: {key} ({length} chars) exceeds field_value limit (1024)")
            elif length > 256 and 'title' in key.lower():
                issues.append(f"{lang}.json: {key} ({length} chars) may exceed title limit (256)")
    
    if issues:
        print(f"Found {len(issues)} potential length issues:")
        for issue in issues[:10]:  # Show first 10
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more")
        return False
    else:
        print("[OK] No strings exceed Discord character limits")
        return True

if __name__ == "__main__":
    if check_lengths():
        exit(0)
    else:
        exit(1)
