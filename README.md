# Discord TTS

Discord 봇을 위한 다국어 TTS(Text-to-Speech) 라이브러리입니다.

## 설치 방법

```bash
pip install discord-tts
```

### 필수 요구사항

이 라이브러리는 **FFmpeg**가 필요합니다. 시스템에 FFmpeg를 먼저 설치해주세요:

- **Windows**: [FFmpeg 다운로드](https://ffmpeg.org/download.html)에서 다운로드 후 PATH 추가
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) 또는 `sudo yum install ffmpeg` (CentOS/RHEL)

## 주요 기능

- 다국어 지원 (한국어, 영어, 일본어, 중국어 등 13개 언어)
- 음성 속도 조절
- 음량 조절
- 고급 텍스트 필터링
  - 정규식 기반 패턴 매칭
  - 기본 패턴 지원 (한글, 영문, 숫자, 특수문자, URL, 멘션, 이모지)
  - 사용자 정의 패턴 추가
  - 패턴 제거/유지 옵션
  - 최대 길이 제한
  - **기본 필터링**: URL, 멘션, 이모지 자동 제거
- 임시 파일 자동 관리
  - 오래된 파일 자동 정리 (기본: 1시간)
  - 디스크 공간 효율적 관리
- 음성 채널 관리
- FFmpeg 자동 검사
- 향상된 에러 처리 및 네트워크 오류 감지

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

# 기본 필터링 (URL, 멘션, 이모지 자동 제거)
text = clean_text("안녕하세요! @user https://example.com 😊")
# 결과: "안녕하세요!"

# 한글만 유지
text = clean_text(
    "안녕하세요! Hello World! 123",
    keep_patterns=['korean']
)
# 결과: "안녕하세요"

# 숫자만 유지
text = clean_text(
    "전화번호는 010-1234-5678입니다",
    keep_patterns=['numbers']
)
# 결과: "01012345678"

# URL과 멘션 제거
text = clean_text(
    "안녕하세요! @user https://example.com",
    remove_patterns=['url', 'mention']
)
# 결과: "안녕하세요!"

# 사용자 정의 패턴 추가
custom_patterns = {
    'phone': r'\d{3}-\d{4}-\d{4}',  # 전화번호 패턴
    'email': r'[\w\.-]+@[\w\.-]+'   # 이메일 패턴
}
text = clean_text(
    "연락처: 010-1234-5678, 이메일: test@example.com",
    patterns=custom_patterns,
    keep_patterns=['phone', 'email']
)
# 결과: "010-1234-5678 test@example.com"

# 최대 길이 제한
text = clean_text("안녕하세요!", max_length=5)
# 결과: "안녕하세"
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

## 버전 히스토리

### v0.2.0 (2025-01-25) - 안정성 개선 업데이트

#### 주요 버그 수정
- ✅ **음량 조절 기능 수정**: `PCMVolumeTransformer`를 올바르게 적용하여 volume 매개변수가 정상 작동
- ✅ **파일 정리 타이밍 수정**: 재생 완료 후에만 임시 파일 삭제 (재생 중 파일 삭제 방지)
- ✅ **파일명 충돌 방지**: 마이크로초 단위 타임스탬프 추가로 동시 요청 처리 개선

#### 새로운 기능
- ⭐ **FFmpeg 자동 검사**: 라이브러리 초기화 시 FFmpeg 설치 여부 확인 및 안내
- ⭐ **자동 파일 정리**: 오래된 임시 TTS 파일 자동 삭제 (max_cache_age 옵션)
- ⭐ **기본 텍스트 필터링**: clean_text() 호출 시 URL, 멘션, 이모지 기본 제거
- ⭐ **동시 재생 방지**: 여러 TTS 요청 순차 처리로 안정성 향상
- ⭐ **새로운 예외 클래스**: `FFmpegNotFoundError`, `NetworkError` 추가

#### 성능 개선
- 🚀 **비동기 I/O 개선**: gTTS 파일 저장을 executor로 실행하여 블로킹 방지
- 🚀 **네트워크 오류 처리**: gTTS API 호출 실패 시 명확한 에러 메시지
- 🚀 **향상된 타입 힌트**: 모든 공개 API에 완전한 타입 힌트 적용

자세한 변경사항은 [CHANGELOG.md](CHANGELOG.md)를 참고하세요.

### v0.1.0 (2025-05-15) - 초기 릴리스
- 기본 TTS 기능
- 다국어 지원
- 텍스트 필터링

## 라이선스

MIT License 