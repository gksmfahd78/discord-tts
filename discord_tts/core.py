"""
TTS 라이브러리의 핵심 기능
"""

import os
import asyncio
import discord
import time
import shutil
from typing import Optional, Dict, Any
from gtts import gTTS
from gtts.tts import gTTSError
from .utils import clean_text
from .exceptions import TTSException, TTSGenerationError, FFmpegNotFoundError, NetworkError

class TTSManager:
    """TTS 기능을 관리하는 클래스"""
    
    # 지원하는 언어 목록
    SUPPORTED_LANGUAGES = {
        'ko': 'Korean',
        'en': 'English',
        'ja': 'Japanese',
        'zh-CN': 'Chinese (Simplified)',
        'zh-TW': 'Chinese (Traditional)',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'ru': 'Russian',
        'pt': 'Portuguese',
        'it': 'Italian',
        'hi': 'Hindi',
        'ar': 'Arabic'
    }
    
    def __init__(self, temp_dir: str = "temp_tts", default_lang: str = 'ko', max_cache_age: int = 3600):
        """
        TTSManager 초기화

        Args:
            temp_dir (str): 임시 파일을 저장할 디렉토리 경로
            default_lang (str): 기본 언어 코드 (기본값: 'ko')
            max_cache_age (int): 임시 파일 최대 보관 시간 (초 단위, 기본값: 3600)
        """
        self.temp_dir = temp_dir
        self.default_lang = default_lang
        self.max_cache_age = max_cache_age
        self._is_playing = False
        os.makedirs(temp_dir, exist_ok=True)
        self._check_ffmpeg()
        
    def _check_ffmpeg(self) -> None:
        """
        FFmpeg 설치 여부를 확인합니다.

        Raises:
            FFmpegNotFoundError: FFmpeg가 설치되지 않았을 때
        """
        if not shutil.which("ffmpeg"):
            raise FFmpegNotFoundError(
                "FFmpeg가 설치되지 않았습니다. "
                "https://ffmpeg.org/download.html 에서 설치해주세요."
            )

    @classmethod
    def get_supported_languages(cls) -> Dict[str, str]:
        """
        지원하는 언어 목록을 반환합니다.

        Returns:
            Dict[str, str]: 언어 코드와 언어 이름의 딕셔너리
        """
        return cls.SUPPORTED_LANGUAGES

    def _cleanup_old_files(self) -> None:
        """
        오래된 임시 파일들을 정리합니다.
        """
        try:
            current_time = time.time()
            for filename in os.listdir(self.temp_dir):
                filepath = os.path.join(self.temp_dir, filename)
                if os.path.isfile(filepath):
                    file_age = current_time - os.path.getmtime(filepath)
                    if file_age > self.max_cache_age:
                        os.remove(filepath)
        except Exception:
            pass  # 파일 정리 실패는 무시
        
    async def generate_tts(self,
                          text: str,
                          lang: Optional[str] = None,
                          slow: bool = False,
                          **kwargs) -> str:
        """
        텍스트를 음성 파일로 변환합니다.

        Args:
            text (str): 변환할 텍스트
            lang (str, optional): 언어 코드. None인 경우 기본 언어 사용
            slow (bool): 음성 속도를 느리게 할지 여부
            **kwargs: gTTS에 전달할 추가 옵션들

        Returns:
            str: 생성된 음성 파일의 경로

        Raises:
            TTSGenerationError: TTS 생성 중 오류 발생 시
            NetworkError: 네트워크 오류 발생 시
        """
        try:
            # 오래된 파일 정리
            self._cleanup_old_files()

            # 언어 코드 확인
            lang = lang or self.default_lang
            if lang not in self.SUPPORTED_LANGUAGES:
                raise TTSException(f"지원하지 않는 언어입니다: {lang}")

            # 텍스트 정제
            cleaned_text = clean_text(text)
            if not cleaned_text:
                raise TTSException("변환할 텍스트가 없습니다.")

            # 임시 파일 경로 생성 (타임스탬프 추가로 동시성 문제 해결)
            timestamp = int(time.time() * 1000000)  # 마이크로초 단위
            temp_file = os.path.join(
                self.temp_dir,
                f"tts_{hash(cleaned_text + lang)}_{timestamp}.mp3"
            )

            # gTTS를 사용하여 음성 생성
            try:
                tts = gTTS(text=cleaned_text, lang=lang, slow=slow, **kwargs)
                await asyncio.get_event_loop().run_in_executor(None, tts.save, temp_file)
            except gTTSError as e:
                raise NetworkError(f"네트워크 오류: {str(e)}")

            return temp_file

        except (TTSException, NetworkError):
            raise
        except Exception as e:
            raise TTSGenerationError(f"TTS 생성 중 오류 발생: {str(e)}")
            
    async def play_tts(self,
                      text: str,
                      voice_client: discord.VoiceClient,
                      lang: Optional[str] = None,
                      slow: bool = False,
                      volume: float = 1.0,
                      **kwargs) -> None:
        """
        텍스트를 음성으로 변환하여 재생합니다.

        Args:
            text (str): 변환할 텍스트
            voice_client (discord.VoiceClient): 음성을 재생할 음성 클라이언트
            lang (str, optional): 언어 코드. None인 경우 기본 언어 사용
            slow (bool): 음성 속도를 느리게 할지 여부
            volume (float): 음량 (0.0 ~ 1.0)
            **kwargs: gTTS에 전달할 추가 옵션들

        Raises:
            TTSException: TTS 생성 또는 재생 중 오류 발생 시
        """
        # 이미 재생 중이면 대기
        while self._is_playing:
            await asyncio.sleep(0.1)

        try:
            self._is_playing = True

            # 음성 파일 생성
            audio_file = await self.generate_tts(text, lang, slow, **kwargs)

            # 음량 변환기를 적용한 오디오 소스 생성
            audio_source = discord.FFmpegPCMAudio(audio_file)
            if volume != 1.0:
                audio_source = discord.PCMVolumeTransformer(audio_source, volume=volume)

            # 재생 완료 후 파일 정리를 위한 이벤트
            playback_finished = asyncio.Event()

            def after_playback(error):
                """재생 완료 후 콜백"""
                if error:
                    print(f"재생 중 오류 발생: {error}")
                # 이벤트 루프에 파일 삭제 예약
                asyncio.run_coroutine_threadsafe(
                    self._async_cleanup_file(audio_file, playback_finished),
                    asyncio.get_event_loop()
                )

            # 음성 재생
            voice_client.play(audio_source, after=after_playback)

            # 재생이 끝날 때까지 대기
            while voice_client.is_playing():
                await asyncio.sleep(0.1)

            # 파일 정리가 완료될 때까지 대기
            await playback_finished.wait()

        except Exception as e:
            raise TTSException(f"TTS 재생 중 오류 발생: {str(e)}")
        finally:
            self._is_playing = False

    async def _async_cleanup_file(self, file_path: str, event: asyncio.Event) -> None:
        """
        비동기로 임시 파일을 삭제합니다.

        Args:
            file_path (str): 삭제할 파일 경로
            event (asyncio.Event): 삭제 완료 시 설정할 이벤트
        """
        try:
            # 파일이 완전히 재생될 때까지 잠시 대기
            await asyncio.sleep(0.5)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass  # 파일 삭제 실패는 무시
        finally:
            event.set() 