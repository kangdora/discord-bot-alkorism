import sqlite3
from datetime import datetime

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
    """, (boj_id, solved_count, tier, rating, datetime.utcnow()))
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