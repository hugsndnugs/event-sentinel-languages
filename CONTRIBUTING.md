# Contributing to Event Sentinel Languages

Thank you for your interest in contributing to Event Sentinel's translations! This guide will help you get started with contributing translations, whether you're adding a new language or improving existing ones.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Translation Workflow](#translation-workflow)
- [Branch Strategy](#branch-strategy)
- [Translation Guidelines](#translation-guidelines)
- [JSON File Structure](#json-file-structure)
- [Quality Standards](#quality-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Adding a New Language

If Event Sentinel doesn't support your language yet, you can add it! Here's how:

1. Copy `en.json` to create a new file named with the appropriate language code (e.g., `it.json` for Italian)
2. Translate all strings while preserving the JSON structure
3. Submit a pull request

### Improving Existing Translations

Even if a language is already supported, there's always room for improvement:

- Fix typos or grammatical errors
- Improve phrasing for better clarity
- Update translations to match Discord's current terminology
- Ensure consistency across all translation keys

### Reporting Translation Issues

If you find an error but don't have time to fix it, please open an issue describing:
- The language file (e.g., `es.json`)
- The translation key path (e.g., `commands.config.title`)
- The current (incorrect) translation
- The suggested correction

## Translation Workflow

### 1. Fork the Repository

Click the "Fork" button on GitHub to create your own copy of the repository.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/event-sentinel-languages.git
cd event-sentinel-languages
```

### 3. Create a Branch

Create a new branch for your work:

```bash
git checkout -b translate/your-language-code
# Example: git checkout -b translate/it
```

### 4. Make Your Changes

- Open the language file you want to work on
- Make your translations following the guidelines below
- Save the file

### 5. Test Your Changes

Before submitting, verify:
- The JSON file is valid (no syntax errors)
- All keys from `en.json` are present
- Placeholders like `{user}` are preserved
- Emojis are preserved
- Markdown formatting is maintained

You can validate JSON using online tools or your text editor.

### 6. Commit Your Changes

Write clear, descriptive commit messages. Good commit messages help maintainers understand your changes quickly.

#### Commit Message Template for New Languages

When adding a new language file, use this template:

```
## Title
Add {Language} translation file {LanguageCode}.json

## Description
Introduces a comprehensive {Language} localization file for all bot events, commands, errors, and common fields. This enables {Language} language support throughout the application.
```

**Example:**
```bash
git add it.json
git commit -m "Add Italian translation file it.json

Introduces a comprehensive Italian localization file for all bot events, commands, errors, and common fields. This enables Italian language support throughout the application."
```

#### Commit Message Guidelines

For other types of changes, follow these patterns:

- **Improving translations**: `"Translate {Language}: {Brief description}"`
  - Example: `"Translate Spanish: Improve moderation event messages"`

- **Fixing errors**: `"Fix {Language}: {Description of fix}"`
  - Example: `"Fix German: Correct typo in member_banned title"`

- **Adding missing keys**: `"Add {Language}: {Missing keys description}"`
  - Example: `"Add French: Add missing modmail translations"`

- **Updating translations**: `"Update {Language}: {What was updated}"`
  - Example: `"Update Japanese: Update command descriptions for clarity"`

**Best Practices:**
- Keep the first line (title) under 72 characters
- Use the imperative mood ("Add" not "Added" or "Adds")
- Be specific about what changed
- Include the language code or name in the message

### 7. Push to Your Fork

```bash
git push origin translate/your-language-code
```

### 8. Create a Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill out the pull request template (if available)
5. Submit the pull request

## Branch Strategy

This project uses a two-branch strategy to manage translation completeness:

- **`main` branch**: Contains **complete** language translations only. All translation keys from `en.json` must be fully translated and verified.
- **`develop` branch**: Contains **incomplete** language translations. This includes work-in-progress translations, partially translated files, and translations that need review or verification.

### `main` Branch

The `main` branch is reserved for:
- **Complete translations**: All translation keys from `en.json` must be translated
- **Verified translations**: Translations that have been reviewed and tested
- **Production-ready content**: Only translations ready for use in the Event Sentinel bot

Only complete, verified translations should be merged to `main`. Maintainers will review and promote translations from `develop` to `main` once they meet the quality standards and are fully complete.

### `develop` Branch

The `develop` branch is used for:
- **Partially translated languages**: Translations that are in progress but not yet complete
- **Unverified translations**: Translations that haven't been reviewed or tested yet
- **Work-in-progress contributions**: Any translation work that needs community review or verification

When submitting a pull request for incomplete or unverified translations, target the `develop` branch. This allows contributors to share their progress and receive feedback before the translation is considered complete.

### How to Choose the Right Branch

When creating your pull request:
- **Target `develop`** if your translation is:
  - Not yet complete (missing some keys)
  - Needs review or verification
  - A work-in-progress update
  
- **Target `main`** if your translation is:
  - 100% complete (all keys translated)
  - Reviewed and verified
  - Ready for production use

If you're unsure which branch to target, default to `develop`. Maintainers can help determine if your translation is ready for `main` during the review process.

## Translation Guidelines

### Essential Rules

1. **Preserve Emojis**: Keep all emojis exactly as they appear in `en.json`. Emojis are universal and should not be translated.

2. **Maintain Formatting**: Preserve all markdown formatting:
   - Bold text: `**text**`
   - Code blocks: `` `text` ``
   - Line breaks: `\n`

3. **Keep Placeholders**: Never translate placeholders like:
   - `{user}`, `{channel}`, `{count}`, `{guild_name}`, etc.
   - These are replaced at runtime by the bot

4. **Respect Character Limits**: Discord has strict limits:
   - Embed title: 256 characters
   - Embed description: 4096 characters
   - Field name: 256 characters
   - Field value: 1024 characters

5. **Use Consistent Terminology**: Maintain consistency throughout:
   - "User" vs "Member" - Use "User" for general references
   - "Server" vs "Guild" - Use "Server" in user-facing text
   - "Channel" vs "Thread" - Be precise

### Translation Best Practices

- **Context Matters**: Consider how the text will appear in Discord embeds
- **Natural Language**: Translate for meaning, not word-for-word
- **Discord Terminology**: Use terms that Discord users in your language would recognize
- **Tone**: Match the tone of the English version (professional but friendly)

## JSON File Structure

All language files follow the same structure as `en.json`:

```json
{
  "events": {
    "moderation": {
      "member_banned": {
        "title": "🚫 Member Banned",
        "user": "User"
      }
    }
  },
  "commands": {
    "help": {
      "title": "📚 Event Sentinel - Command Help"
    }
  }
}
```

### Key Organization

- `events.*` - Event logging messages
- `commands.*` - Command responses
- `errors.*` - Error messages
- `fields.*` - Common field names
- `common.*` - Common strings (yes/no, enabled/disabled)
- `footer.*` - Footer text

**Important**: Every key in `en.json` must exist in your translation file. Missing keys will cause the bot to fall back to English.

## Quality Standards

Before submitting, ensure your translation:

- ✅ Contains all keys from `en.json`
- ✅ Has valid JSON syntax (no trailing commas, proper quotes)
- ✅ Preserves all placeholders (`{variable}`)
- ✅ Preserves all emojis
- ✅ Maintains markdown formatting
- ✅ Uses natural, fluent language
- ✅ Respects Discord character limits
- ✅ Uses consistent terminology

## Submitting Changes

### Pull Request Guidelines

When creating a pull request:

1. **Title**: Be descriptive (e.g., "Add Italian translation" or "Fix Spanish moderation messages")

2. **Description**: Include:
   - What you changed
   - Why you made the changes
   - Any questions or concerns

3. **Scope**: Keep PRs focused:
   - One language per PR (unless fixing multiple small issues)
   - Don't mix unrelated changes

4. **Testing**: Mention if you've tested the translations in Discord

### Review Process

- Maintainers will review your PR for quality and completeness
- You may be asked to make changes
- Once approved, your changes will be merged

## Reporting Issues

### Translation Errors

If you find a translation error:

1. Check if an issue already exists
2. Open a new issue with:
   - Language file affected
   - Translation key path
   - Current incorrect text
   - Suggested correction
   - Context (where it appears)

### Missing Translations

If you notice missing translations:

1. Check if the key exists in `en.json`
2. If it's missing from your language file, you can:
   - Submit a PR to add it
   - Open an issue to report it

### Questions

For questions about:
- Translation guidelines: See [TRANSLATION_TEMPLATE.md](TRANSLATION_TEMPLATE.md)
- Contribution process: Open an issue
- Code of conduct: See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## Getting Help

If you need help:

- Read the [Translation Template](TRANSLATION_TEMPLATE.md) for detailed guidelines
- Look at existing translations for examples
- Open an issue with your question
- Check existing issues and pull requests

## Thank You!

Your contributions help make Event Sentinel accessible to Discord communities worldwide. Every translation, no matter how small, makes a difference. Thank you for taking the time to contribute!
