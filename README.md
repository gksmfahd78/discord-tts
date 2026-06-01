# Discord TTS

Python TTS helper library for Discord bots. It handles multilingual playback, text filtering, temporary audio files, FFmpeg checks, and common voice-channel workflows.

## Features

- Multilingual TTS playback
- Voice speed and volume controls
- Discord voice-channel integration helpers
- URL, mention, emoji, and custom text filtering
- Temporary audio file cleanup
- FFmpeg availability checks
- Network and playback error handling

## Installation

```bash
pip install discord-tts
```

FFmpeg is required:

- Windows: install FFmpeg and add it to `PATH`
- macOS: `brew install ffmpeg`
- Ubuntu/Debian: `sudo apt install ffmpeg`
- CentOS/RHEL: `sudo yum install ffmpeg`

## Basic Usage

```python
import discord
from discord.ext import commands
from discord_tts import TTSManager

bot = commands.Bot(command_prefix="!")

@bot.command()
async def tts(ctx, *, text):
    tts_manager = TTSManager()

    if not ctx.author.voice:
        await ctx.send("Join a voice channel first.")
        return

    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()

    try:
        await tts_manager.play_tts(
            text=text,
            voice_client=ctx.voice_client,
        )
    except Exception as error:
        await ctx.send(f"TTS failed: {error}")

bot.run("YOUR_BOT_TOKEN")
```

## Language Examples

```python
await tts_manager.play_tts(
    text="Hello, World!",
    voice_client=voice_client,
    lang="en",
)

await tts_manager.play_tts(
    text="こんにちは",
    voice_client=voice_client,
    lang="ja",
)
```

## Playback Controls

```python
await tts_manager.play_tts(
    text="안녕하세요",
    voice_client=voice_client,
    slow=True,
)

await tts_manager.play_tts(
    text="안녕하세요",
    voice_client=voice_client,
    volume=0.5,
)
```

## Text Filtering

```python
from discord_tts import clean_text

text = clean_text("안녕하세요! @user https://example.com")

text = clean_text(
    "안녕하세요! Hello World! 123",
    keep_patterns=["korean"],
)

custom_patterns = {
    "phone": r"\\d{3}-\\d{4}-\\d{4}",
    "email": r"[\\w\\.-]+@[\\w\\.-]+",
}

text = clean_text(
    "연락처: 010-1234-5678, email: test@example.com",
    patterns=custom_patterns,
    keep_patterns=["phone", "email"],
)
```

## Supported Languages

- Korean (`ko`)
- English (`en`)
- Japanese (`ja`)
- Chinese Simplified (`zh-CN`)
- Chinese Traditional (`zh-TW`)
- Spanish (`es`)
- French (`fr`)
- German (`de`)
- Russian (`ru`)
- Portuguese (`pt`)
- Italian (`it`)
- Hindi (`hi`)
- Arabic (`ar`)

## Version Notes

### v0.2.0

- Improved volume handling
- Temporary file cleanup after playback
- FFmpeg detection
- Better default text filtering
- Custom error classes for FFmpeg and network failures

### v0.1.0

- Initial TTS playback
- Multilingual support
- Text filtering

## License

MIT License.
