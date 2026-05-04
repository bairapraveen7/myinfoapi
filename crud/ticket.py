from db.session import get_db_connection
from fastapi import Depends

def create_todo_db(title, description):
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO todo (title, description) VALUES (?, ?)", (title, description))
        db.commit()
    except Exception as e:
        db.rollback()
        cursor.close()
        raise e

def view_todo_db(id):
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM todo WHERE id = ?", (id,))
        todo = cursor.fetchone()
        if not todo:
            return None
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, todo))
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

def get_all_todos_db():
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM todo")
        columns = [col[0] for col in cursor.description]
        todos = cursor.fetchall()
        return [dict(zip(columns, todo)) for todo in todos]
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()



