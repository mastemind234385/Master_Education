import sqlite3
import os


DB_PATH = "data/school.db"


def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            question_bn TEXT,
            question_en TEXT,
            answer_bn TEXT,
            answer_en TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_question(
    subject,
    question_bn,
    question_en,
    answer_bn,
    answer_en
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO questions
        (subject, question_bn, question_en, answer_bn, answer_en)
        VALUES (?, ?, ?, ?, ?)
    """, (
        subject,
        question_bn,
        question_en,
        answer_bn,
        answer_en
    ))

    conn.commit()
    conn.close()


def search_question(subject, question):

    conn = get_connection()
    cursor = conn.cursor()

    question = question.lower().strip()

    cursor.execute("""
        SELECT
            question_bn,
            question_en,
            answer_bn,
            answer_en
        FROM questions
        WHERE subject = ?
    """, (subject,))

    results = cursor.fetchall()

    conn.close()

    for row in results:

        question_bn = (row[0] or "").lower()
        question_en = (row[1] or "").lower()

        if question == question_bn or question == question_en:

            return {
                "question_bn": row[0],
                "question_en": row[1],
                "answer_bn": row[2],
                "answer_en": row[3]
            }

    return None