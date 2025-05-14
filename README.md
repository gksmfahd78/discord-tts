# Discord TTS

Discord 봇을 위한 다국어 TTS(Text-to-Speech) 라이브러리입니다.

## 설치 방법

```bash
pip install discord-tts
```

## 주요 기능

- 다국어 지원 (한국어, 영어, 일본어, 중국어 등)
- 음성 속도 조절
- 음량 조절
- 고급 텍스트 필터링
  - 특수문자 제거
  - 이모지 제거
  - URL 제거
  - 멘션 제거
  - 연속된 공백 제거
  - 허용 문자 지정
  - 최대 길이 제한
- 임시 파일 자동 관리
- 음성 채널 관리

## 사용 예시

### 기본 사용법

```python
import discord
from discord.ext import commands
from discord_tts import TTSManager

bot = commands.Bot(command_prefix='!')

@bot.command()
async def tts(ctx, *, text):
    # TTS 매니저 초기화
    tts_manager = TTSManager()
    
    # 사용자의 음성 채널 확인
    if not ctx.author.voice:
        await ctx.send("음성 채널에 먼저 입장해주세요!")
        return
        
    # 봇이 음성 채널에 없으면 입장
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
        
    # TTS 재생
    try:
        await tts_manager.play_tts(
            text=text,
            voice_client=ctx.voice_client
        )
    except Exception as e:
        await ctx.send(f"오류가 발생했습니다: {str(e)}")

bot.run('YOUR_BOT_TOKEN')
```

### 다국어 지원

```python
# 영어로 TTS 재생
await tts_manager.play_tts(
    text="Hello, World!",
    voice_client=voice_client,
    lang='en'
)

# 일본어로 TTS 재생
await tts_manager.play_tts(
    text="こんにちは",
    voice_client=voice_client,
    lang='ja'
)
```

### 음성 속도와 음량 조절

```python
# 느린 속도로 재생
await tts_manager.play_tts(
    text="안녕하세요",
    voice_client=voice_client,
    slow=True
)

# 음량 조절 (0.0 ~ 1.0)
await tts_manager.play_tts(
    text="안녕하세요",
    voice_client=voice_client,
    volume=0.5
)
```

### 텍스트 필터링

```python
from discord_tts import clean_text

# 기본 필터링
text = clean_text("안녕하세요! @user https://example.com 😊")

# 특정 문자만 허용
allowed_chars = set("가나다라마바사아자차카타파하")
text = clean_text("안녕하세요!", allowed_chars=allowed_chars)

# URL과 멘션만 제거
text = clean_text(
    "안녕하세요! @user https://example.com",
    remove_special_chars=False,
    remove_emojis=False
)

# 최대 길이 제한
text = clean_text("안녕하세요!", max_length=5)  # "안녕하세"
```

### 지원하는 언어 목록 확인

```python
tts_manager = TTSManager()
supported_languages = tts_manager.get_supported_languages()
print(supported_languages)
```

## 지원하는 언어

- 한국어 (ko)
- 영어 (en)
- 일본어 (ja)
- 중국어 간체 (zh-CN)
- 중국어 번체 (zh-TW)
- 스페인어 (es)
- 프랑스어 (fr)
- 독일어 (de)
- 러시아어 (ru)
- 포르투갈어 (pt)
- 이탈리아어 (it)
- 힌디어 (hi)
- 아랍어 (ar)

## 라이선스

MIT License 