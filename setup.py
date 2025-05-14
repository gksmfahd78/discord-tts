from setuptools import setup, find_packages

setup(
    name="discord-tts",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "discord.py>=2.0.0",
        "gTTS>=2.3.1",
        "PyNaCl>=1.4.0"
    ],
    author="gksmfahd78",
    author_email="leedonghyun@kakao.com",  
    description="Discord 봇을 위한 TTS(Text-to-Speech) 라이브러리",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gksmfahd78/discord-tts", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 