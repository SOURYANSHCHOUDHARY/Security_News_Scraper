import sqlite3
from config import DATABASE_NAME


def connect():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    # Create Articles table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        title TEXT,
        published TEXT,
        link TEXT UNIQUE
    )
    """)

    # Create IOCs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS iocs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER,
        ioc_type TEXT,
        ioc_value TEXT,
        UNIQUE(article_id, ioc_type, ioc_value),
        FOREIGN KEY(article_id) REFERENCES articles(id)
    )
    """)

    conn.commit()
    conn.close()


def insert_article(source, title, published, link):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO articles
    (source, title, published, link)
    VALUES (?, ?, ?, ?)
    """, (source, title, published, link))

    conn.commit()

    cursor.execute(
        "SELECT id FROM articles WHERE link = ?",
        (link,)
    )

    article_id = cursor.fetchone()[0]

    conn.close()

    return article_id


def insert_ioc(article_id, ioc_type, ioc_value):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO iocs
    (article_id, ioc_type, ioc_value)
    VALUES (?, ?, ?)
    """, (article_id, ioc_type, ioc_value))

    conn.commit()
    conn.close()


def get_articles():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        source,
        title,
        published,
        link
    FROM articles
    ORDER BY published DESC
    """)

    articles = cursor.fetchall()

    conn.close()

    return articles


def get_iocs():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        iocs.id,
        articles.source,
        articles.title,
        iocs.ioc_type,
        iocs.ioc_value
    FROM iocs
    JOIN articles
    ON articles.id = iocs.article_id
    ORDER BY articles.published DESC
    """)

    iocs = cursor.fetchall()

    conn.close()

    return iocs