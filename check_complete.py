#!/usr/bin/env python3
"""Check and report complete translation files (100% translated)"""
import json
from pathlib import Path
from validate_locales import (
    get_all_keys,
    validate_locale_file
)

def check_complete():
    """Check for complete translation files and report them"""
    # Load English file as reference
    with open("en.json", 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    en_keys = set(get_all_keys(en_data))
    
    # Get all string values from English for comparison
    from check_english import get_all_strings
    en_strings = dict(get_all_strings(en_data))
    
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
        return
    
    languages.sort()  # Sort for consistent output
    complete_files = []
    
    for lang in languages:
        valid, message, missing_keys, untranslated_keys = validate_locale_file(
            lang, en_keys, en_strings
        )
        
        if valid:
            # Count total keys for reporting
            total_keys = len(en_keys)
            complete_files.append((lang, total_keys))
            print(f"[COMPLETE] {lang}.json: 100% complete ({total_keys}/{total_keys} keys translated)")
    
    print()
    if complete_files:
        print(f"[INFO] {len(complete_files)} translation file(s) are complete:")
        for lang, count in complete_files:
            print(f"  - {lang}.json ({count} keys)")
    else:
        print("[INFO] No translation files are currently complete")

if __name__ == "__main__":
    check_complete()
    exit(0)  # Always succeed (informational only)
