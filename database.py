
import sqlite3
from datetime import datetime
from logging import getLogger
from log_scripts.set_logger import set_logger

logger = getLogger(__name__)
logger = set_logger(logger)
def create_db():
    logger.info("creating db")
    conn = sqlite3.connect('chatgpt_cache.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS cache
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     question TEXT,
     answer TEXT,
     time TEXT,
     fast_model BOOLEAN)
    ''')
    conn.commit()
    conn.close()
    
def cache_answer(question, answer, model):
    logger.info(f"question: {question}, answer: {answer}, model: {model}")
    conn = sqlite3.connect('chatgpt_cache.db')
    c = conn.cursor()
    time_now = datetime.now().isoformat()
    c.execute('''
    INSERT INTO cache (question, answer, time, fast_model) 
    VALUES (?, ?, ?, ?)
    ''', (question, answer, time_now, model))
    conn.commit()
    conn.close()    

def get_cached_answer(question, model):
    logger.info(f"question: {question}, model: {model}")
    conn = sqlite3.connect('chatgpt_cache.db')
    c = conn.cursor()
    c.execute('''
    SELECT answer FROM cache WHERE question = ? AND fast_model = ?
    ''', (question, model))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

if __name__ == '__main__':
    create_db()
    