#!/usr/bin/env python3
"""Compare completeness of translation files between main and develop branches"""
import json
import sys
from pathlib import Path
from validate_locales import get_all_keys
from check_english import get_all_strings, is_likely_english_match, should_skip_key

def check_file_completeness(lang_code, branch_path, en_keys, en_strings):
    """Check if a translation file is complete in a specific branch directory"""
    file_path = Path(branch_path) / f"{lang_code}.json"
    
    if not file_path.exists():
        return False, 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Get all keys from this language file
        lang_keys = set(get_all_keys(data))
        lang_strings = dict(get_all_strings(data))
        
        # Check for missing keys
        missing_keys = en_keys - lang_keys
        if missing_keys:
            return False, 0
        
        # Check for extra keys
        extra_keys = lang_keys - en_keys
        if extra_keys:
            return False, 0
        
        # Check for untranslated keys (English stubs)
        for key, en_value in en_strings.items():
            if key not in lang_strings:
                return False, 0
            
            # Skip keys that should be excluded from English detection
            if should_skip_key(key, en_value):
                continue
            
            # Check if the translation matches English
            lang_value = lang_strings[key]
            is_match, _ = is_likely_english_match(en_value, lang_value)
            
            if is_match:
                return False, 0
        
        # All checks passed - file is complete
        total_keys = len(en_keys)
        return True, total_keys
        
    except (json.JSONDecodeError, Exception):
        return False, 0

def get_complete_languages(branch_path, en_keys, en_strings):
    """Get set of complete language codes for a branch"""
    complete = {}
    branch_dir = Path(branch_path)
    
    if not branch_dir.exists():
        return complete
    
    # Discover all language files in the branch
    json_files = list(branch_dir.glob("*.json"))
    excluded_files = {"en", "translation_stats"}
    
    for json_file in json_files:
        lang_code = json_file.stem
        if lang_code not in excluded_files:
            is_complete, key_count = check_file_completeness(
                lang_code, branch_path, en_keys, en_strings
            )
            if is_complete:
                complete[lang_code] = key_count
    
    return complete

def compare_branches(main_path, develop_path):
    """Compare completeness between main and develop branches"""
    # Load English file as reference (use main branch as source of truth)
    en_file = Path(main_path) / "en.json"
    if not en_file.exists():
        en_file = Path(develop_path) / "en.json"
    
    if not en_file.exists():
        print("[ERROR] en.json not found in either branch")
        return None
    
    with open(en_file, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    en_keys = set(get_all_keys(en_data))
    en_strings = dict(get_all_strings(en_data))
    
    # Get complete languages from each branch
    main_complete = get_complete_languages(main_path, en_keys, en_strings)
    develop_complete = get_complete_languages(develop_path, en_keys, en_strings)
    
    # Compare results
    ready_to_move = {
        lang: count 
        for lang, count in develop_complete.items() 
        if lang not in main_complete
    }
    
    complete_on_both = {
        lang: count 
        for lang, count in main_complete.items() 
        if lang in develop_complete
    }
    
    complete_on_main_only = {
        lang: count 
        for lang, count in main_complete.items() 
        if lang not in develop_complete
    }
    
    return {
        'ready_to_move': ready_to_move,
        'complete_on_both': complete_on_both,
        'complete_on_main_only': complete_on_main_only,
        'main_complete': main_complete,
        'develop_complete': develop_complete
    }

def main():
    """Main function to run branch comparison"""
    if len(sys.argv) < 3:
        print("Usage: check_complete_compare.py <main_branch_path> <develop_branch_path>")
        sys.exit(1)
    
    main_path = sys.argv[1]
    develop_path = sys.argv[2]
    
    print("[BRANCH COMPARISON - Completeness Status]")
    print()
    
    results = compare_branches(main_path, develop_path)
    
    if results is None:
        sys.exit(1)
    
    # Print summary
    main_langs = sorted(results['main_complete'].keys())
    develop_langs = sorted(results['develop_complete'].keys())
    
    print(f"Main branch complete languages: {', '.join(main_langs) if main_langs else '(none)'}")
    print(f"Develop branch complete languages: {', '.join(develop_langs) if develop_langs else '(none)'}")
    print()
    
    # Languages ready to move
    ready_to_move = results['ready_to_move']
    if ready_to_move:
        print("Languages ready to move to main:")
        for lang in sorted(ready_to_move.keys()):
            count = ready_to_move[lang]
            print(f"  ✓ {lang}.json - 100% complete ({count}/{count} keys)")
    else:
        print("Languages ready to move to main: (none)")
    print()
    
    # Languages complete on both
    complete_on_both = results['complete_on_both']
    if complete_on_both:
        print("Languages complete on both branches:")
        for lang in sorted(complete_on_both.keys()):
            count = complete_on_both[lang]
            print(f"  ✓ {lang}.json - 100% complete ({count}/{count} keys)")
    else:
        print("Languages complete on both branches: (none)")
    print()
    
    # Languages complete on main only (shouldn't normally happen)
    complete_on_main_only = results['complete_on_main_only']
    if complete_on_main_only:
        print("Languages complete on main only (may need attention):")
        for lang in sorted(complete_on_main_only.keys()):
            count = complete_on_main_only[lang]
            print(f"  ⚠ {lang}.json - 100% complete ({count}/{count} keys)")
    print()
    
    # Output JSON for issue creation step
    output_json = {
        'ready_to_move': list(ready_to_move.keys()),
        'complete_on_both': list(complete_on_both.keys()),
        'complete_on_main_only': list(complete_on_main_only.keys())
    }
    
    # Write to file for GitHub Actions to read
    with open('completeness_results.json', 'w', encoding='utf-8') as f:
        json.dump(output_json, f, indent=2)
    
    print(f"[INFO] Results written to completeness_results.json")
    
    # Always succeed (informational only)
    sys.exit(0)

if __name__ == "__main__":
    main()
