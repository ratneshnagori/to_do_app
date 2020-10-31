import sqlite3

DB_PATH = 'to_do.db'
PENDING = 'Pending'
COMPLETED = 'Completed'
SUCCESS='Success'
FAILURE = 'Failure'

def get_all_tasks():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('select * from to_do')
        rows = c.fetchall()
        return rows
    except Exception as e:
        print('Error: ', e)
        return None

def get_all_tasks_sorted(sort_status):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        if sort_status == 0:
            c.execute('select * from to_do order by duedate asc')
        else:
            c.execute('select * from to_do order by duedate desc')
            
        rows = c.fetchall()
        return rows
    except Exception as e:
        print('Error: ', e)
        return None
        
def add_a_task(name, details, duedate):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('insert into to_do(name, details, duedate, status) values(?,?,?,?)', (name, details, duedate, PENDING))

        conn.commit()
        return {"Result": SUCCESS, "Remark": "Task added in to-do list"}
    except Exception as e:
        print('Error: ', e)
        return {"Result": FAILURE, "Remark": str(e)}
        
def update_task_status(name, status):
    # Check if the passed status is a valid value
    if (status.lower().strip() == 'pending'):
        status = PENDING
    elif (status.lower().strip() == 'completed'):
        status = COMPLETED
    else:
        print("Invalid Status: " + status)
        return {"Result": FAILURE, "Remark": "Task status is not correct"}

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('update to_do set status=? where name=?', (status, name))
        conn.commit()
        return {"Result": SUCCESS, "Remark": "Task updated in to-do list"}
    except Exception as e:
        print('Error: ', e)
        return {"Result": FAILURE, "Remark": str(e)}

def update_task(name, details, duedate, status):
    # Check if the passed status is a valid value
    if (status.lower().strip() == 'pending'):
        status = PENDING
    elif (status.lower().strip() == 'completed'):
        status = COMPLETED
    else:
        print("Invalid Status: " + status)
        return {"Result": FAILURE, "Remark": "Task status is not correct"}

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('update to_do set details=?, status=?, duedate=?  where name=?', (details, status, duedate, name))
        conn.commit()
        return {"Result": SUCCESS, "Remark": "Task updated in to-do list"}
    except Exception as e:
        print('Error: ', e)
        return {"Result": FAILURE, "Remark": str(e)}

def delete_item(name):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('delete from to_do where name=?', (name,))
        conn.commit()
        return {"Result": SUCCESS, "Remark": "Task deleted from the to-do list"}
    except Exception as e:
        print('Error: ', e)
        return {"Result": FAILURE, "Remark": str(e)}