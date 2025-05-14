"""
TTS 라이브러리의 유틸리티 함수들
"""

import re
import discord
from typing import Optional, Tuple, List, Set, Dict, Union
from .exceptions import NoVoiceChannelError

class TextFilter:
    """텍스트 필터링을 위한 클래스"""
    
    def __init__(self, 
                 remove_special_chars: bool = True,
                 remove_emojis: bool = True,
                 remove_urls: bool = True,
                 remove_mentions: bool = True,
                 remove_extra_spaces: bool = True,
                 allowed_chars: Optional[Set[str]] = None,
                 max_length: Optional[int] = None):
        """
        TextFilter 초기화
        
        Args:
            remove_special_chars (bool): 특수문자 제거 여부
            remove_emojis (bool): 이모지 제거 여부
            remove_urls (bool): URL 제거 여부
            remove_mentions (bool): 멘션 제거 여부
            remove_extra_spaces (bool): 연속된 공백 제거 여부
            allowed_chars (Set[str], optional): 허용할 문자 집합
            max_length (int, optional): 최대 텍스트 길이
        """
        self.remove_special_chars = remove_special_chars
        self.remove_emojis = remove_emojis
        self.remove_urls = remove_urls
        self.remove_mentions = remove_mentions
        self.remove_extra_spaces = remove_extra_spaces
        self.allowed_chars = allowed_chars
        self.max_length = max_length
        
        # 이모지 패턴
        self.emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
            
        # URL 패턴
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        
        # 멘션 패턴
        self.mention_pattern = re.compile(r'<@!?\d+>')
        
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
            
        # URL 제거
        if self.remove_urls:
            text = self.url_pattern.sub('', text)
            
        # 멘션 제거
        if self.remove_mentions:
            text = self.mention_pattern.sub('', text)
            
        # 이모지 제거
        if self.remove_emojis:
            text = self.emoji_pattern.sub('', text)
            
        # 특수문자 제거
        if self.remove_special_chars:
            if self.allowed_chars:
                # 허용된 문자만 남기기
                text = ''.join(c for c in text if c in self.allowed_chars)
            else:
                # 기본 특수문자 제거 (한글, 영문, 숫자, 공백만 남김)
                text = re.sub(r'[^\w\s가-힣]', '', text)
                
        # 연속된 공백 제거
        if self.remove_extra_spaces:
            text = re.sub(r'\s+', ' ', text)
            
        # 앞뒤 공백 제거
        text = text.strip()
        
        # 최대 길이 제한
        if self.max_length and len(text) > self.max_length:
            text = text[:self.max_length]
            
        return text

def clean_text(text: str, 
               remove_special_chars: bool = True,
               remove_emojis: bool = True,
               remove_urls: bool = True,
               remove_mentions: bool = True,
               remove_extra_spaces: bool = True,
               allowed_chars: Optional[Set[str]] = None,
               max_length: Optional[int] = None) -> str:
    """
    텍스트를 정제합니다.
    
    Args:
        text (str): 원본 텍스트
        remove_special_chars (bool): 특수문자 제거 여부
        remove_emojis (bool): 이모지 제거 여부
        remove_urls (bool): URL 제거 여부
        remove_mentions (bool): 멘션 제거 여부
        remove_extra_spaces (bool): 연속된 공백 제거 여부
        allowed_chars (Set[str], optional): 허용할 문자 집합
        max_length (int, optional): 최대 텍스트 길이
        
    Returns:
        str: 정제된 텍스트
    """
    filter = TextFilter(
        remove_special_chars=remove_special_chars,
        remove_emojis=remove_emojis,
        remove_urls=remove_urls,
        remove_mentions=remove_mentions,
        remove_extra_spaces=remove_extra_spaces,
        allowed_chars=allowed_chars,
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