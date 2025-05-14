"""
TTS 라이브러리에서 사용되는 예외 클래스들
"""

class TTSException(Exception):
    """TTS 관련 기본 예외 클래스"""
    pass

class NoVoiceChannelError(TTSException):
    """사용자가 음성 채널에 없을 때 발생하는 예외"""
    pass

class TTSGenerationError(TTSException):
    """TTS 생성 중 오류가 발생했을 때 발생하는 예외"""
    pass

class InvalidTextError(TTSException):
    """유효하지 않은 텍스트가 입력되었을 때 발생하는 예외"""
    pass 