import sqlite3

from db.database import get_db
from db.queries import INSERT_TASK, GET_ALL_TASKS_BY_TG_ID, GET_TAKS_BY_ID, UPDATE_TASK_IS_DONE, GET_TASKS_STATS

def create_task(user_id: int, task_name: str, is_done: bool):
    conn = get_db()
    conn.execute(INSERT_TASK, (user_id, task_name, is_done))
    conn.commit()
    conn.close()

def get_all_tasks(telegram_id: int):
    conn = get_db()
    rows = conn.execute(GET_ALL_TASKS_BY_TG_ID, (telegram_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_task(id: int, telegram_id: int):
    conn = get_db()
    row = conn.execute(GET_TAKS_BY_ID, (id, telegram_id)).fetchone()
    conn.close()
    return dict(row) if row else None

def update_task_is_done(is_done: int, id: int, telegram_id: int):
    conn = get_db()
    conn.execute(UPDATE_TASK_IS_DONE, (is_done, id, telegram_id))
    conn.commit()
    conn.close()
    return get_task(id, telegram_id)

def get_stats(telegram_id: int):
    conn = get_db()
    rows = conn.execute(GET_TASKS_STATS, (telegram_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]