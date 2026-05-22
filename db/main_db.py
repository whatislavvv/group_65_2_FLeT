import sqlite3
from config import path_db
from db import queries

a = ()
b = []
c = {}

def init_db():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.create_tasks_table)
    print('БД подключена!')
    conn.commit()
    conn.close()


# def add_task(task):
#     conn = sqlite3.connect(path_db)
#     cursor = conn.cursor()
#     # cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task, ))
#     cursor.execute(queries.insert_task, (task,))
#     conn.commit()
#     task_id = cursor.lastrowid
#     conn.close()
#     return task_id

def add_task(task):
    with sqlite3.connect(path_db) as conn: 
        cursor = conn.cursor()
        cursor.execute(queries.insert_task, (task, ))
        task_id = cursor.lastrowid
    return task_id


def update_task(task_id, new_task=None, completed=None):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    if new_task is not None:
        cursor.execute(queries.update_task, (new_task, task_id))
    elif completed is not None:
        cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (completed, task_id))
    
    conn.commit()
    conn.close()

def get_tasks(filter_type=None): 
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    if filter_type == 'completed':
        cursor.execute(queries.select_tasks_completed)
    elif filter_type == 'uncompleted':
        cursor.execute(queries.select_tasks_uncompleted)
    else:
        cursor.execute(queries.select_tasks)
    tasks = cursor.fetchall()
    conn.close()
    return tasks  

def delete_all_completed():
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.delete_completed)
        conn.commit()

    tasks = cursor.fetchall()
    conn.close()
    return tasks