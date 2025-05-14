"""
TTS 라이브러리의 유틸리티 함수들
"""

import re
import discord
from typing import Optional, Tuple, List, Set, Dict, Union, Pattern
from .exceptions import NoVoiceChannelError

class TextFilter:
    """텍스트 필터링을 위한 클래스"""
    
    # 기본 정규식 패턴들
    DEFAULT_PATTERNS = {
        'korean': r'[가-힣]',  # 한글
        'english': r'[a-zA-Z]',  # 영문
        'numbers': r'[0-9]',  # 숫자
        'spaces': r'\s',  # 공백
        'special': r'[^\w\s가-힣]',  # 특수문자
        'url': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',  # URL
        'mention': r'<@!?\d+>',  # 멘션
        'emoji': r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]'  # 이모지
    }
    
    def __init__(self, 
                 patterns: Optional[Dict[str, str]] = None,
                 remove_patterns: Optional[List[str]] = None,
                 keep_patterns: Optional[List[str]] = None,
                 max_length: Optional[int] = None):
        """
        TextFilter 초기화
        
        Args:
            patterns (Dict[str, str], optional): 추가할 정규식 패턴들
            remove_patterns (List[str], optional): 제거할 패턴 이름들
            keep_patterns (List[str], optional): 유지할 패턴 이름들
            max_length (int, optional): 최대 텍스트 길이
        """
        # 기본 패턴과 사용자 정의 패턴 합치기
        self.patterns = {**self.DEFAULT_PATTERNS, **(patterns or {})}
        
        # 제거할 패턴 컴파일
        self.remove_patterns = []
        if remove_patterns:
            for pattern_name in remove_patterns:
                if pattern_name in self.patterns:
                    self.remove_patterns.append(re.compile(self.patterns[pattern_name]))
                    
        # 유지할 패턴 컴파일
        self.keep_patterns = []
        if keep_patterns:
            for pattern_name in keep_patterns:
                if pattern_name in self.patterns:
                    self.keep_patterns.append(re.compile(self.patterns[pattern_name]))
                    
        self.max_length = max_length
        
    def clean(self, text: str) -> str:
        """
        텍스트를 정제합니다.
        
        Args:
            text (str): 원본 텍스트
            
        Returns:
            str: 정제된 텍스트
        """
        if not text:
            return ""
            
        # 제거할 패턴 적용
        for pattern in self.remove_patterns:
            text = pattern.sub('', text)
            
        # 유지할 패턴이 있는 경우, 해당 패턴과 일치하는 부분만 남김
        if self.keep_patterns:
            matches = []
            for pattern in self.keep_patterns:
                matches.extend(pattern.findall(text))
            text = ''.join(matches)
            
        # 연속된 공백 제거
        text = re.sub(r'\s+', ' ', text)
        
        # 앞뒤 공백 제거
        text = text.strip()
        
        # 최대 길이 제한
        if self.max_length and len(text) > self.max_length:
            text = text[:self.max_length]
            
        return text

def clean_text(text: str, 
               patterns: Optional[Dict[str, str]] = None,
               remove_patterns: Optional[List[str]] = None,
               keep_patterns: Optional[List[str]] = None,
               max_length: Optional[int] = None) -> str:
    """
    텍스트를 정제합니다.
    
    Args:
        text (str): 원본 텍스트
        patterns (Dict[str, str], optional): 추가할 정규식 패턴들
        remove_patterns (List[str], optional): 제거할 패턴 이름들
        keep_patterns (List[str], optional): 유지할 패턴 이름들
        max_length (int, optional): 최대 텍스트 길이
        
    Returns:
        str: 정제된 텍스트
    """
    filter = TextFilter(
        patterns=patterns,
        remove_patterns=remove_patterns,
        keep_patterns=keep_patterns,
        max_length=max_length
    )
    return filter.clean(text)

def get_voice_channel(member: discord.Member) -> Tuple[discord.VoiceChannel, discord.VoiceClient]:
    """
    사용자의 현재 음성 채널과 봇의 음성 클라이언트를 반환합니다.
    
    Args:
        member (discord.Member): 음성 채널을 확인할 사용자
        
    Returns:
        Tuple[discord.VoiceChannel, discord.VoiceClient]: 음성 채널과 음성 클라이언트
        
    Raises:
        NoVoiceChannelError: 사용자가 음성 채널에 없을 때
    """
    if not member.voice:
        raise NoVoiceChannelError("사용자가 음성 채널에 없습니다.")
        
    voice_channel = member.voice.channel
    voice_client = discord.utils.get(member.guild.voice_clients, guild=member.guild)
    
    return voice_channel, voice_client 