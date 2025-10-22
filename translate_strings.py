#!/usr/bin/env python3
# translate_strings_multi.py
# Fixed for googletrans==4.0.0+ (async API)

import os
import re
import asyncio
import argparse
from collections import OrderedDict
from googletrans import Translator
from tqdm import tqdm

# ---------- CONFIG ----------
BASE_LANG = "en"
PROJECT_PATH = "./grammarchecker/Resources/Localization"
DEFAULT_LANGS = []
BASE_FILENAME = "Localizable.strings"

# ✅ Apple → Google Translate code mapping

LANGUAGE_CODE_MAP = {
    # Chinese variants
    "zh-Hans": "zh-cn",  # Simplified
    "zh-Hant": "zh-tw",  # Traditional
    "zh-HK": "zh-tw",    # Hong Kong → Traditional
    # Portuguese
    "pt-PT": "pt",
    "pt-BR": "pt",
    # English variants
    "en-GB": "en",
    "en-AU": "en",
    # Norwegian Bokmål
    "nb": "no",
    # Filipino / Hebrew adjustments
    "fil": "tl",
    "he": "iw",
        # French
    "fr-CA": "fr",
}

# Apple localizations - you can add more languages
AVAILABLE_LANGUAGES = OrderedDict([
                                   ("en", "English"),
                                   ("ar", "Arabic"),
                                   ("ca", "Catalan"),
                                   ("zh-HK", "Chinese (Hong Kong)"),
                                   ("zh-Hans", "Chinese (Simplified)"),
                                   ("zh-Hant", "Chinese (Traditional)"),
                                   ("hr", "Croatian"),
                                   ("cs", "Czech"),
                                   ("da", "Danish"),
                                   ("nl", "Dutch"),
                                   ("en-AU", "English (Australia)"),
                                   ("en-GB", "English (United Kingdom)"),
                                   ("fi", "Finnish"),
                                   ("fr", "French"),
                                   ("fr-CA", "French (Canada)"),
                                   ("de", "German"),
                                   ("el", "Greek"),
                                   ("he", "Hebrew"),
                                   ("hu", "Hungarian"),
                                   ("it", "Italian"),
                                   ("ja", "Japanese"),
                                   ("ko", "Korean"),
                                   ("pt-BR", "Portuguese (Brazil)"),
                                   ("pt-PT", "Portuguese (Portugal)"),
                                   ("es", "Spanish"),
                                   ("sv", "Swedish"),
                                   ("ru", "Russian")
                                   ])


# ---------- FILE HELPERS ----------
def parse_strings(file_path, preserve_order=False):
    """Parse .strings file into a dict."""
    result = OrderedDict() if preserve_order else {}
    if not os.path.exists(file_path):
        return result
    pattern = re.compile(r'^\s*"(?P<k>.*?)"\s*=\s*"(?P<v>.*?)";\s*$')
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            m = pattern.match(line)
            if m:
                result[m.group("k")] = m.group("v")
    return result


def write_strings(file_path, data):
    """Write key/value pairs into Localizable.strings with correct quotes and percent handling."""
    with open(file_path, "w", encoding="utf-8") as f:
        for k, v in data.items():
            # Replace double quotes in value with single quotes for clarity
            v = v.replace('"', "'")

            # Escape only double quotes (for safety in format)
            safe_key = k.replace('"', '\\"')
            safe_val = v.replace('"', '\\"')

            # Fix percent signs
            safe_val = (
                safe_val
                .replace("٪", "%")   # replace Arabic percent
            )

            f.write(f"\"{safe_key}\" = \"{safe_val}\";\n")


# ---------- ASYNC TRANSLATION ----------
async def safe_translate(translator, text, src, dest, retries=3):
    """Async translate with retries"""
    if not text:
        return text
    
    effective_dest = LANGUAGE_CODE_MAP.get(dest, dest)
    effective_src = LANGUAGE_CODE_MAP.get(src, src)
    
    for attempt in range(retries):
        try:
            result = await translator.translate(text, src=effective_src, dest=effective_dest)
            return result.text
        except Exception as e:
            if attempt < retries - 1:
                await asyncio.sleep(1.0)
            else:
                print(f"❌ Failed to translate '{text[:40]}...': {e}")
                return text


async def translate_batch(translator, items, src, dest, batch_size=50):
    """Translate items in batches to avoid overwhelming the API"""
    results = {}
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        tasks = [safe_translate(translator, value, src, dest) for key, value in batch]
        translations = await asyncio.gather(*tasks)
        
        for (key, _), translation in zip(batch, translations):
            results[key] = translation
        
        # Small delay between batches
        if i + batch_size < len(items):
            await asyncio.sleep(0.5)
    
    return results


async def translate_language_async(lang, base_strings, preserve_order=False, batch_size=50):
    """Translate all keys for one language using async"""
    """Translate all keys for one language using async"""
    lang_file = os.path.join(PROJECT_PATH, f"{lang}.lproj/{BASE_FILENAME}")
    os.makedirs(os.path.dirname(lang_file), exist_ok=True)
    
    total = len(base_strings)
    print(f"\n🌍 Translating {total} keys to '{lang}'...")
    
    translator = Translator()
    items = list(base_strings.items())
    
    # Process in batches with progress bar
    translated = OrderedDict() if preserve_order else {}
    
    with tqdm(total=total, desc=f"{lang.upper()} Progress") as pbar:
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_results = await translate_batch(translator, batch, BASE_LANG, lang, batch_size=10)
            translated.update(batch_results)
            pbar.update(len(batch))
    
    # Fill any missing keys (safety)
    for k, v in base_strings.items():
        if k not in translated:
            translated[k] = v
    
    write_strings(lang_file, translated)
    print(f"🎉 {lang}: Translation file written to: {lang_file}\n")


def translate_language(lang, base_strings, preserve_order=False):
    """Synchronous wrapper for async translation"""
    asyncio.run(translate_language_async(lang, base_strings, preserve_order))


# ---------- CLI + INTERACTIVE ----------
def interactive_select_languages():
    codes = list(AVAILABLE_LANGUAGES.keys())
    print("\nSelect languages to translate to (e.g. 1-3,7,9 or 'all').")
    for i, (code, name) in enumerate(AVAILABLE_LANGUAGES.items(), start=1):
        print(f"[ ] {i:2d}. {code:8s} — {name}")
    raw = input("\nYour selection: ").strip()
    if not raw:
        return []
    if raw.lower() == "all":
        return codes
    if raw.lower() in ("none", "n", "cancel"):
        return []
    
    selection = set()
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    for p in parts:
        if "-" in p:
            try:
                start, end = [int(x) for x in p.split("-", 1)]
                for idx in range(start, end + 1):
                    if 1 <= idx <= len(codes):
                        selection.add(codes[idx - 1])
            except ValueError:
                continue
        else:
            if p.isdigit() and 1 <= int(p) <= len(codes):
                selection.add(codes[int(p) - 1])
            elif p in AVAILABLE_LANGUAGES:
                selection.add(p)
    return sorted(selection)


def parse_cli_arguments():
    parser = argparse.ArgumentParser(description="Translate Localizable.strings into multiple languages.")
    parser.add_argument("--langs", "-l", nargs="+", help="Target language codes (space-separated)")
    parser.add_argument("--all", action="store_true", help="Translate to all available languages")
    parser.add_argument("--preserve-order", action="store_true", help="Preserve key order from base file")
    parser.add_argument("--batch-size", type=int, default=50, help="Batch size for translations")
    parser.add_argument("--base-path", type=str, default=PROJECT_PATH, help="Localization base path")
    parser.add_argument("--base-lang", type=str, default=BASE_LANG, help="Base language code")
    return parser.parse_args()


# ---------- MAIN ----------
def main():
    args = parse_cli_arguments()
    
    global PROJECT_PATH, BASE_LANG
    PROJECT_PATH = args.base_path
    BASE_LANG = args.base_lang
    
    base_file = os.path.join(PROJECT_PATH, f"{BASE_LANG}.lproj/{BASE_FILENAME}")
    base_strings = parse_strings(base_file, preserve_order=args.preserve_order)
    if not base_strings:
        print(f"❌ Base file not found or empty: {base_file}")
        return
    
    if args.all:
        selected = list(AVAILABLE_LANGUAGES.keys())
    elif args.langs:
        selected = []
        for token in args.langs:
            token = token.strip()
            if token.isdigit():
                idx = int(token)
                codes = list(AVAILABLE_LANGUAGES.keys())
                if 1 <= idx <= len(codes):
                    selected.append(codes[idx - 1])
            elif token in AVAILABLE_LANGUAGES:
                selected.append(token)
            else:
                selected.append(token)
    else:
        selected = interactive_select_languages()
        if not selected:
            print("No languages selected — exiting.")
            return
    
    selected = [s for s in selected if s != BASE_LANG]
    print(f"\nWill translate to: {selected}\n")
    
    for lang in selected:
        translate_language(lang, base_strings, preserve_order=args.preserve_order)
    
    print("✅ All translations completed successfully!")


if __name__ == "__main__":
    main()

