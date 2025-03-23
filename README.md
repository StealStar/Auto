# 게임 오토 프로그램

이 프로그램은 게임 자동화를 위한 기본 프레임워크를 제공합니다.

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

## 주요 기능

- 화면 캡처 및 이미지 인식
- 마우스 자동 제어
- 키보드 입력 감지
- ESC 키를 통한 프로그램 종료
- 화면 모서리 이동 시 안전 정지 기능

## 사용 방법

1. `auto_game.py` 파일의 `game_loop` 메서드에 원하는 게임 자동화 로직을 구현합니다.
2. 프로그램 실행:
```bash
python auto_game.py
```

## 주의사항

- 프로그램 실행 중 ESC 키를 누르면 프로그램이 종료됩니다.
- 마우스를 화면 모서리로 이동하면 프로그램이 자동으로 종료됩니다 (안전 기능).
- 게임 클라이언트가 관리자 권한으로 실행되는 경우, 이 프로그램도 관리자 권한으로 실행해야 할 수 있습니다. 