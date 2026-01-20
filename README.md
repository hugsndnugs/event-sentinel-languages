# Event Sentinel Languages

This repository contains the language files used by the [Event Sentinel](https://github.com/hugsndnugs/event-sentinel) Discord bot. Event Sentinel is a comprehensive Discord moderation and logging bot that tracks server events and provides detailed logging capabilities.

## Overview

Event Sentinel supports multiple languages to make the bot accessible to Discord communities worldwide. This repository manages all translation files in JSON format, making it easy for contributors to add new languages or improve existing translations.

## Supported Languages

The following languages are currently supported:

- 🇺🇸 **English (en)** - Base language (complete)
- 🇪🇸 **Spanish (es)** - Español
- 🇫🇷 **French (fr)** - Français
- 🇩🇪 **German (de)** - Deutsch
- 🇯🇵 **Japanese (ja)** - 日本語
- 🇰🇷 **Korean (ko)** - 한국어
- 🇵🇹 **Portuguese (pt)** - Português

## Visualization Dashboard

🌐 **[View the Interactive Language Dashboard](https://hugsndnugs.github.io/event-sentinel-languages/)**

Explore all translations with our interactive GitHub Pages dashboard featuring:

- **📊 Statistics Dashboard** - View translation completeness percentages, key counts, and visual progress indicators for each language
- **🔍 Comparison Tool** - Compare translations side-by-side across multiple languages with a tree view of the nested JSON structure
- **🔎 Search & Filter** - Search by key path or translation text, filter by language or category (events, commands, errors, etc.)
- **⚠️ Missing Keys Report** - Identify missing translations per language and export reports as JSON

The dashboard automatically loads all language files and provides real-time analysis of translation coverage.

## Quick Start for Translators

If you're fluent in another language and want to help improve Event Sentinel's translations:

1. **Fork this repository** to your GitHub account
2. **Choose a language file** to work on (or create a new one)
3. **Read the [Translation Guidelines](TRANSLATION_TEMPLATE.md)** for detailed instructions
4. **Make your translations** following the JSON structure in `en.json`
5. **Submit a Pull Request** with your changes

For detailed contribution instructions, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Project Structure

```
event-sentinel-languages/
├── index.html       # GitHub Pages visualization dashboard
├── en.json          # English (base language)
├── de.json          # German
├── es.json          # Spanish
├── fr.json          # French
├── ja.json          # Japanese
├── ko.json          # Korean
├── pt.json          # Portuguese
└── TRANSLATION_TEMPLATE.md  # Translation guidelines
```

## Translation Guidelines

All translations must follow these key principles:

- **Preserve emojis** exactly as they appear in the English version
- **Maintain markdown formatting** (bold, code blocks, etc.)
- **Keep placeholders** like `{user}`, `{channel}`, `{count}` unchanged
- **Respect Discord's character limits** (titles: 256 chars, descriptions: 4096 chars)
- **Use consistent terminology** throughout the translation

For complete guidelines, see [TRANSLATION_TEMPLATE.md](TRANSLATION_TEMPLATE.md).

## Contributing

We welcome contributions from translators of all skill levels! Whether you want to:
- Add a new language
- Improve existing translations
- Fix errors or typos
- Suggest better phrasing

Your help makes Event Sentinel more accessible to Discord communities worldwide.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions on how to contribute.

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## Security

If you discover a security vulnerability, please review our [SECURITY.md](SECURITY.md) policy for responsible disclosure.

## License

This project is dedicated to the public domain under the [CC0 1.0 Universal](LICENSE) license. You are free to use, modify, and distribute these translations without restrictions.

## Questions?

If you have questions about translations or need help getting started:
- Open an issue in this repository
- Check the [Translation Template](TRANSLATION_TEMPLATE.md) for guidelines
- Review existing translations for examples

## Acknowledgments

Thank you to all the translators who have contributed their time and expertise to make Event Sentinel accessible in multiple languages. Your contributions help Discord communities around the world!
