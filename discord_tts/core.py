"""
TTS 라이브러리의 핵심 기능
"""

import os
import asyncio
import discord
from typing import Optional, Dict, Any
from gtts import gTTS
from .utils import clean_text
from .exceptions import TTSException, TTSGenerationError

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
    
    def __init__(self, temp_dir: str = "temp_tts", default_lang: str = 'ko'):
        """
        TTSManager 초기화
        
        Args:
            temp_dir (str): 임시 파일을 저장할 디렉토리 경로
            default_lang (str): 기본 언어 코드 (기본값: 'ko')
        """
        self.temp_dir = temp_dir
        self.default_lang = default_lang
        os.makedirs(temp_dir, exist_ok=True)
        
    @classmethod
    def get_supported_languages(cls) -> Dict[str, str]:
        """
        지원하는 언어 목록을 반환합니다.
        
        Returns:
            Dict[str, str]: 언어 코드와 언어 이름의 딕셔너리
        """
        return cls.SUPPORTED_LANGUAGES
        
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
        """
        try:
            # 언어 코드 확인
            lang = lang or self.default_lang
            if lang not in self.SUPPORTED_LANGUAGES:
                raise TTSException(f"지원하지 않는 언어입니다: {lang}")
            
            # 텍스트 정제
            cleaned_text = clean_text(text)
            if not cleaned_text:
                raise TTSException("변환할 텍스트가 없습니다.")
                
            # 임시 파일 경로 생성
            temp_file = os.path.join(self.temp_dir, f"tts_{hash(cleaned_text + lang)}.mp3")
            
            # gTTS를 사용하여 음성 생성
            tts = gTTS(text=cleaned_text, lang=lang, slow=slow, **kwargs)
            tts.save(temp_file)
            
            return temp_file
            
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
        try:
            # 음성 파일 생성
            audio_file = await self.generate_tts(text, lang, slow, **kwargs)
            
            # 음성 재생
            voice_client.play(
                discord.FFmpegPCMAudio(audio_file),
                after=lambda e: self._cleanup_file(audio_file)
            )
            
            # 음량 설정
            if hasattr(voice_client, 'source'):
                voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
                voice_client.source.volume = volume
            
            # 재생이 끝날 때까지 대기
            while voice_client.is_playing():
                await asyncio.sleep(0.1)
                
        except Exception as e:
            raise TTSException(f"TTS 재생 중 오류 발생: {str(e)}")
            
    def _cleanup_file(self, file_path: str) -> None:
        """
        임시 파일을 삭제합니다.
        
        Args:
            file_path (str): 삭제할 파일 경로
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass  # 파일 삭제 실패는 무시 