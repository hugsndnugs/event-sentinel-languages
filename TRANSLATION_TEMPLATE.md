# Translation Template and Guidelines

This document provides guidelines for translators working on Event Sentinel bot translations.

## Language Files Structure

All language files follow the same JSON structure as `en.json`. The English file (`en.json`) serves as the base template and reference.

## Translation Keys

Translation keys use dot notation to organize content hierarchically:

- `events.*` - Event logging messages (embeds for moderation, voice, message, channel, role, server events)
- `commands.*` - Command responses and help text
- `errors.*` - Error messages
- `fields.*` - Common field names used across embeds
- `common.*` - Common strings (yes/no, enabled/disabled, etc.)
- `footer.*` - Footer text

## Guidelines

1. **Preserve Emojis**: Keep all emojis exactly as they appear in the English version. Emojis are language-agnostic.

2. **Preserve Formatting**: Maintain markdown formatting (bold `**text**`, code blocks `` `text` ``, etc.)

3. **Placeholders**: Preserve placeholder syntax like `{user}`, `{channel}`, `{count}`, etc. These are replaced at runtime.

4. **Context**: When translating, consider the Discord context:
   - Field names should be concise (Discord has character limits)
   - Descriptions can be more detailed
   - Titles should be clear and action-oriented

5. **Consistency**: Use consistent terminology throughout:
   - "User" vs "Member" - Use "User" for general references, "Member" when specifically referring to server membership
   - "Channel" vs "Thread" - Be precise
   - "Server" vs "Guild" - Use "Server" in user-facing text

6. **Character Limits**: Be aware of Discord's limits:
   - Embed title: 256 characters
   - Embed description: 4096 characters
   - Field name: 256 characters
   - Field value: 1024 characters

## Example Translation

English:
```json
{
  "events": {
    "moderation": {
      "member_banned": {
        "title": "🚫 Member Banned",
        "user": "User"
      }
    }
  }
}
```

Spanish:
```json
{
  "events": {
    "moderation": {
      "member_banned": {
        "title": "🚫 Miembro Baneado",
        "user": "Usuario"
      }
    }
  }
}
```

## Missing Translations

If a translation key is missing in a language file, the system will:
1. Try the requested language
2. Fall back to English (default)
3. Fall back to the key itself if all else fails

## Testing

After translating, test the bot with the new language to ensure:
- All text displays correctly
- No formatting is broken
- Placeholders work correctly
- Text fits within Discord's character limits

## Supported Languages

- `en` - English (base)
- `es` - Spanish (Español)
- `fr` - French (Français)
- `de` - German (Deutsch)
- `ja` - Japanese (日本語)
- `ko` - Korean (한국어)
- `pt` - Portuguese (Português)
