import sqlite3
from sqlite3 import Error

def create_connection(db_file):

    # creates a connection to the db 
    """ create a database connection to a SQLite Database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE STATEMENT
    :return: 
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def inset_data(conn, data):
    # temp information will not be used later. 
    sql = '''INSERT INTO project(time_started, time_recorded, amount_sent, amount_recv) VALUES (?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql,data)
    conn.commit()
    return cur.lastrowid
def get_all(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM project")
    rows = cur.fetchall()
    for row in rows:
        print(row)
def get_item(conn):
    # get items from db where time == current session 
    value = "'21342'"
    sql = "SELECT * from project WHERE time_started = " + value 
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)

def main():
    database = 'database.db'
    sql_create_project_table = """ CREATE TABLE IF NOT EXISTS project (
        id integer PRIMARY KEY AUTOINCREMENT,
        time_started integer NOT NULL,
        time_recorded integer NOT NULL,
        amount_sent integer NOT NULL,
        amount_recv integer NOT NULL);"""
    conn = create_connection(database)
    if conn is not None:
        create_table(conn,sql_create_project_table)
    else:
        print("Error! Cannot create the database connection.")
    with conn:
        task_1 = (21342,21320,132200,1213)
        #inset_data(conn,task_1)
        get_all(conn)
        get_item(conn)

if __name__ == '__main__':
    main()