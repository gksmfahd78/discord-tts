# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-01-25

### Added
- **FFmpeg 자동 검사**: 초기화 시 FFmpeg 설치 여부를 확인하여 명확한 에러 메시지 제공
- **자동 파일 정리**: 오래된 임시 TTS 파일 자동 삭제 기능 (`max_cache_age` 옵션, 기본값: 1시간)
- **새로운 예외 클래스**: `FFmpegNotFoundError`, `NetworkError` 추가
- **기본 텍스트 필터링**: `clean_text()` 함수가 인자 없이 호출되면 URL, 멘션, 이모지를 기본으로 제거
- **동시 재생 방지**: 여러 TTS 요청이 동시에 들어올 때 순차 처리
- **향상된 타입 힌트**: 모든 공개 API에 완전한 타입 힌트 적용
- **메타데이터 개선**: setup.py에 더 많은 PyPI 분류자 및 프로젝트 URL 추가

### Fixed
- **음량 조절 버그 수정**: `PCMVolumeTransformer`를 재생 전에 올바르게 적용하도록 수정
  - 이전: 재생 후 `voice_client.source`에 접근 시도 (작동 안 함)
  - 현재: 오디오 소스 생성 시 `PCMVolumeTransformer`로 래핑
- **파일 정리 타이밍 문제 해결**:
  - 재생이 완료된 후에만 임시 파일 삭제
  - 비동기 이벤트 기반 파일 정리로 안전성 향상
- **파일명 충돌 방지**:
  - 마이크로초 단위 타임스탬프를 파일명에 추가
  - 동시 요청 시 고유한 파일명 보장
- **네트워크 오류 처리**: gTTS API 호출 실패 시 명확한 `NetworkError` 예외 발생
- **블로킹 I/O 개선**: gTTS 파일 저장을 executor로 실행하여 이벤트 루프 블로킹 방지

### Changed
- **버전 업데이트**: 0.1.0 → 0.2.0
- **TTSManager 생성자**: `max_cache_age` 매개변수 추가
- **clean_text 동작 변경**: 기본적으로 URL, 멘션, 이모지 제거 (이전: 아무것도 제거 안 함)
- **예외 처리 강화**: 더 세밀한 예외 타입으로 에러 상황 구분

### Internal
- **코드 품질 개선**: 일관된 코드 포맷팅 및 docstring 개선
- **리소스 관리 개선**: 파일 핸들 및 임시 파일 관리 개선

## [0.1.0] - 2025-05-15

### Added
- 초기 릴리스
- 기본 TTS 기능 (gTTS 기반)
- 다국어 지원 (한국어, 영어, 일본어, 중국어 등 13개 언어)
- 텍스트 필터링 기능
- 음성 속도 조절
- 음량 조절 (기능 버그 있음, 0.2.0에서 수정)
- Discord.py 통합

---

## 주요 개선사항 요약 (v0.2.0)

### 🔧 핵심 버그 수정
1. **음량 조절 완전 수정**: 이제 volume 매개변수가 실제로 작동합니다
2. **파일 정리 안전성**: 재생 중 파일 삭제 방지
3. **동시성 문제 해결**: 파일명 충돌 및 재생 충돌 방지

### ✨ 새로운 기능
1. **자동 파일 정리**: 디스크 공간 자동 관리
2. **FFmpeg 검사**: 설치 여부를 즉시 확인하고 안내
3. **스마트 필터링**: 기본적으로 불필요한 텍스트 제거

### 🛡️ 안정성 향상
1. **향상된 에러 처리**: 명확한 에러 메시지와 예외 타입
2. **네트워크 오류 대응**: 인터넷 연결 문제 감지
3. **비동기 개선**: 블로킹 작업을 executor로 처리

이 업데이트는 프로덕션 환경에서 안정적으로 사용할 수 있도록 다양한 버그 수정과 개선사항을 포함합니다.
