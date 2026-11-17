CREATE_USERS_TABLE = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL UNIQUE
    )
'''

CREATE_TASKS_TABLE = '''
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        task_name TEXT NOT NULL,
        is_done BOOL NOT NULL DEFAULT 0,

        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
'''

# __________________________________________

INSERT_USER = '''
    INSERT OR IGNORE INTO users (telegram_id)
    VALUES (?)
'''

INSERT_TASK = '''
    INSERT INTO tasks (user_id, task_name, is_done)
    VALUES (?, ?, ?)
'''

# __________________________________________

GET_USER_BY_TG_ID = '''
    SELECT * FROM users
    WHERE telegram_id = ?
'''

GET_ALL_TASKS_BY_TG_ID = '''
    SELECT * FROM tasks
    INNER JOIN users
        ON users.id = tasks.user_id
    WHERE users.telegram_id = ?
'''

GET_TAKS_BY_ID = '''
    SELECT t.id, t.user_id, t.task_name, t.is_done 
    FROM tasks AS t
    INNER JOIN users
        ON users.id = t.user_id
    WHERE t.id = ?
    AND users.telegram_id = ?
'''

GET_TASKS_STATS = '''
    SELECT t.is_done, COUNT(*) AS count
    FROM tasks AS t
    INNER JOIN users
        ON users.id = t.user_id
    WHERE users.telegram_id = ?
    GROUP BY t.is_done
'''

# __________________________________________

UPDATE_TASK_IS_DONE = '''
    UPDATE tasks
    SET is_done = ?
    WHERE id = ?
    AND user_id = (SELECT id FROM users WHERE telegram_id = ?)
'''
