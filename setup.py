from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="discord-tts",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "discord.py>=2.0.0",
        "gTTS>=2.3.1",
        "PyNaCl>=1.4.0",
    ],
    author="Lee Dong Hyun",
    author_email="leedonghyun@kakao.com",
    description="Multilingual TTS helper library for Discord bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gksmfahd78/discord-tts",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Chat",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
    ],
    python_requires=">=3.8",
    keywords="discord tts text-to-speech voice bot gtts",
    project_urls={
        "Bug Reports": "https://github.com/gksmfahd78/discord-tts/issues",
        "Source": "https://github.com/gksmfahd78/discord-tts",
    },
)
