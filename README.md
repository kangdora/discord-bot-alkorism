# 💻 한기대 알고리즘 스터디 디스코드 인증/관리 봇 - Alkorism Bot

**백준 solved.ac 데이터를 기반으로 사용자 역할을 자동으로 부여하고, 서버 참여 조건을 관리하는 디스코드 봇**

---

## 📌 주요 기능

- ✅ 디스코드 유저와 백준 ID 연동 (`!인증 <백준ID>`)
- ✅ solved.ac API를 통한 레이팅/티어/푼 문제 수 조회
- ✅ 역할 자동 분류: 입문 / 초보 / 레귤러 / 멘토 등
- ✅ 규칙 메시지에 리액션 시 자동 역할 부여
- ✅ 주간 목표 문제 수 설정 및 부족 시 알림
- ✅ 유저 정보 DB에 자동 저장 및 주기적 업데이트

---

## ⚙️ 사용 기술

- **Python 3.9+**
- `discord.py`
- `sqlite3` (경량 로컬 DB)
- solved.ac API v3

---

## 🛠 기본 명령어(추가 예정)

| 명령어 | 설명 |
|--------|------|
| `!인증 <백준ID>` | 디스코드 계정과 백준 ID를 연결합니다 |
| `!프로필 [백준ID]` | 해당 유저의 solved.ac 프로필을 조회합니다 |
| `!목표 <숫자>` | 주간 목표 문제 수를 설정합니다 |
| `!유저삭제 <백준ID>` | 관리자 전용. 유저 데이터를 삭제합니다 |
| `!유저갱신전체` | 관리자 전용. 모든 유저 solved.ac 정보를 갱신합니다 |
| `!로드 / !리로드 / !언로드` | Cog 확장 관리용 명령어 (관리자 전용) |

---

## 🗃 DB 구조

### 📍 user 테이블
| 컬럼명 | 설명 |
|--------|------|
| `USER_ID` | 디스코드 고유 ID (PK) |
| `JOIN_DATE` | 가입 일자 |
| `RATING_AT_JOINED` | 가입 당시 solved.ac 레이팅 |
| `NUMBER_PER_WEEK` | 주간 목표 문제 수 |
| `LACK_NOTICE` | 주간 풀이 문제 부족 시 알림 여부 |
| `USER_BOJ_ID` | 연결된 백준 ID (FK → user_items) |

### 📍 user_items 테이블
| 컬럼명 | 설명 |
|--------|------|
| `USER_BOJ_ID` | 백준 ID (PK) |
| `SOLVED_COUNT` | 총 푼 문제 수 |
| `TIER` | solved.ac 티어 |
| `RATING` | solved.ac 레이팅 |
| `UPDATED_AT` | 마지막 갱신 시각 (KST 기준) |

---

## 🚀 실행 방법

1. `.env` 또는 `config.py`에 디스코드 봇 토큰 설정
2. `python main.py` 실행
3. 최초 실행 시 DB(`data.db`) 자동 생성됨

```bash
pip install -r requirements.txt
python main.py
```
