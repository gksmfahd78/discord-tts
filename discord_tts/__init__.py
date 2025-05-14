"""
Discord TTS (Text-to-Speech) 라이브러리
이 라이브러리는 Discord 봇을 위한 텍스트 음성 변환 기능을 제공합니다.
"""

from .core import TTSManager
from .utils import clean_text, get_voice_channel
from .exceptions import TTSException, NoVoiceChannelError

__version__ = "0.1.0"

__all__ = [
    'TTSManager',
    'clean_text',
    'get_voice_channel',
    'TTSException',
    'NoVoiceChannelError',
    '__version__'
] 