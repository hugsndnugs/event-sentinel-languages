#!/usr/bin/env python3
"""Check that translations don't contain untranslated English text"""
import json
import re
from pathlib import Path

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

def normalize_for_comparison(text):
    """Normalize text for comparison by removing placeholders"""
    # Remove {placeholder} patterns for comparison
    return re.sub(r'\{[^}]+\}', '', text).strip()

def is_emoji_only(text):
    """Check if text contains only emoji and whitespace"""
    # Remove emoji ranges and whitespace
    cleaned = re.sub(r'[\U0001F300-\U0001F9FF\U00002600-\U000026FF\U00002700-\U000027BF\s]', '', text)
    return len(cleaned) == 0 and len(text.strip()) > 0

def is_likely_english_match(en_value, lang_value):
    """Determine if lang_value is likely untranslated English"""
    # Exact match (case-sensitive)
    if en_value == lang_value:
        return True, "exact"
    
    # Case-insensitive match
    if en_value.lower() == lang_value.lower():
        return True, "case-insensitive"
    
    # Normalized comparison (ignoring placeholders)
    en_normalized = normalize_for_comparison(en_value)
    lang_normalized = normalize_for_comparison(lang_value)
    
    if en_normalized and lang_normalized:
        # Exact normalized match
        if en_normalized == lang_normalized:
            return True, "normalized-exact"
        # Case-insensitive normalized match
        if en_normalized.lower() == lang_normalized.lower():
            return True, "normalized-case-insensitive"
    
    return False, None

def should_skip_key(key_path, value):
    """Determine if a key should be skipped from English detection checks"""
    # Skip very short strings (might be single words that are the same)
    if len(value.strip()) <= 1:
        return True
    
    # Skip emoji-only strings (they're universal)
    if is_emoji_only(value):
        return True
    
    # Skip strings that are purely technical (IDs, etc.)
    # These often appear in technical fields like "user_id", "channel_id"
    if re.match(r'^[A-Z_]+$', value.strip()):
        return True
    
    return False

def check_english():
    """Check for untranslated English text in locale files"""
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
        if lang_code != "en":  # Exclude en.json as it's the reference
            languages.append(lang_code)
    
    if not languages:
        print("[WARN] No language files found (except en.json)")
        return True
    
    languages.sort()  # Sort for consistent output
    all_ok = True
    
    for lang in languages:
        with open(f"{lang}.json", 'r', encoding='utf-8') as f:
            lang_data = json.load(f)
        
        lang_strings = dict(get_all_strings(lang_data))
        issues = []
        
        for key, en_value in en_strings.items():
            if key not in lang_strings:
                continue  # Missing keys are handled by validate_locales.py
            
            lang_value = lang_strings[key]
            
            # Skip certain types of strings that may legitimately match
            if should_skip_key(key, en_value):
                continue
            
            # Check if the translation matches English
            is_match, match_type = is_likely_english_match(en_value, lang_value)
            
            if is_match:
                # Show a preview of the value (truncate if too long)
                preview = lang_value[:50] + "..." if len(lang_value) > 50 else lang_value
                issues.append(f"{key}: '{preview}' ({match_type} match)")
        
        if issues:
            print(f"[FAIL] {lang}.json has potential untranslated English text:")
            for issue in issues[:10]:  # Show first 10
                print(f"  - {issue}")
            if len(issues) > 10:
                print(f"  ... and {len(issues) - 10} more")
            all_ok = False
        else:
            print(f"[OK] {lang}.json: No untranslated English text detected")
    
    return all_ok

if __name__ == "__main__":
    if check_english():
        print("\n[OK] No untranslated English text found in translation files!")
        exit(0)
    else:
        print("\n[FAIL] Some translation files may contain untranslated English text")
        exit(1)
