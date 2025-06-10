import sqlite3
from . import DB_PATH

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

# user 테이블
cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    USER_ID VARCHAR(32) PRIMARY KEY,
    JOIN_DATE DATE,
    RATING_AT_JOINED INT,
    NUMBER_PER_WEEK SMALLINT,
    LACK_NOTICE BOOLEAN,
    USER_BOJ_ID VARCHAR(20),
    FOREIGN KEY (USER_BOJ_ID) REFERENCES user_items(USER_BOJ_ID)
);
""")

# user_items 테이블
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_items (
    USER_BOJ_ID VARCHAR(20) PRIMARY KEY,
    SOLVED_COUNT INT,
    TIER SMALLINT,
    RATING INT,
    UPDATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
conn.close()
