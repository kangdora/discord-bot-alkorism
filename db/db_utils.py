import sqlite3
from datetime import datetime, timedelta, timezone

def upsert_user_items(boj_id, rating, tier, solved_count, conn: sqlite3.Connection):
    """user_items 테이블에 사용자 정보를 삽입 또는 업데이트"""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_items (USER_BOJ_ID, SOLVED_COUNT, TIER, RATING, UPDATED_AT)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(USER_BOJ_ID) DO UPDATE SET
            SOLVED_COUNT=excluded.SOLVED_COUNT,
            TIER=excluded.TIER,
            RATING=excluded.RATING,
            UPDATED_AT=excluded.UPDATED_AT;
    """, (boj_id, solved_count, tier, rating, datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

def insert_user_if_not_exists(discord_id, boj_id, rating, conn: sqlite3.Connection):
    """user 테이블에 처음 가입하는 사용자를 추가 (중복 무시)"""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO user (
            USER_ID, JOIN_DATE, RATING_AT_JOINED, NUMBER_PER_WEEK, LACK_NOTICE, USER_BOJ_ID
        ) VALUES (?, DATE('now'), ?, ?, ?, ?);
    """, (discord_id, rating, 5, False, boj_id))
    conn.commit()

def save_new_user(discord_id, boj_id, rating, tier, solved_count, conn: sqlite3.Connection):
    """처음 등록하는 사용자일 경우 두 테이블 모두 처리"""
    insert_user_if_not_exists(discord_id, boj_id, rating, conn)
    upsert_user_items(boj_id, rating, tier, solved_count, conn)

def get_user_info(discord_id: str, conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user.USER_BOJ_ID, user_items.RATING, user_items.TIER, user_items.SOLVED_COUNT, user_items.UPDATED_AT, user.NUMBER_PER_WEEK
        FROM user
        LEFT JOIN user_items ON user.USER_BOJ_ID = user_items.USER_BOJ_ID
        WHERE user.USER_ID = ?
    """, (discord_id,))

    row = cursor.fetchone()
    if row is None:
        return None

    return {
        "boj_id": row[0],
        "rating": row[1],
        "tier": row[2],
        "solved_count": row[3],
        "updated_at": row[4],
        "number_per_week": row[5]
    }

def delete_user(boj_id: str, conn: sqlite3.Connection):
    cursor = conn.cursor()

    cursor.execute("SELECT USER_ID FROM user WHERE USER_BOJ_ID = ?", (boj_id,))
    row = cursor.fetchone()

    if not row:
        print(f"❌ 해당 BOJ ID '{boj_id}'와 매핑된 유저 없음")
        return

    discord_id = row[0]

    # 삭제
    cursor.execute("DELETE FROM user WHERE USER_ID = ?", (discord_id,))
    cursor.execute("DELETE FROM user_items WHERE USER_BOJ_ID = ?", (boj_id,))
    conn.commit()
    print(f"✅ 유저 삭제 완료: Discord ID {discord_id}, BOJ ID {boj_id}")