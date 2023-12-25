import pymysql
from config import *

def connect():
    print('#' * 20)
    connection = pymysql.connect(
        host=host,
        user=user,
        port=3306,
        db=db,
        password=password,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("INFO: Connection to RDS MySQL instance succeeded")
    return connection
def disconnect(connection):
    print('#' * 20)
    try:
        connection.close()
        print("INFO: Connection to RDS MySQL instance closed")
    except Exception as e:
        print("ERROR: Unexpected error: Could not connect to MySql instance.")
        print(e)

def create_table(name, params):
    connection = connect()
    print('#' * 20)
    with connection.cursor() as cursor:
        try:
            sql = f"CREATE TABLE {name} ({params})"
            cursor.execute(sql)
            connection.commit()
            print(f"INFO: Table {name} created successfully")
        except:
            print(f"INFO: Table {name} already exists")
        disconnect(connection)


def insert(table, params, values):
        connection = connect()
        print('#' * 20)
        with connection.cursor() as cursor:
            sql = f"INSERT INTO {table} ({params}) VALUES ({values})"
            cursor.execute(sql)
            connection.commit()
            print(f"INFO: Record inserted successfully into {table} table")
            disconnect(connection)
    #except Exception as e:
    #    print("ERROR: Unexpected error: Could not insert record")
    #    print(e)

def select(table, params, where):
    try:
        connection = connect()
        print('#' * 20)
        with connection.cursor() as cursor:
            sql = f"SELECT {params} FROM {table} WHERE {where}"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(f"INFO: Record selected successfully from {table} table")
            return result
        disconnect(connection)
    except Exception as e:
        print("ERROR: Unexpected error: Could not select record")
        print(e)
def select_all(table):
    print('#' * 20)
    try:
        connection = connect()
        print('#' * 20)
        with connection.cursor() as cursor:
            sql = f"SELECT * FROM {table}"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(f"INFO: Record selected successfully from {table} table")
            return result
        disconnect(connection)
    except Exception as e:
        print("ERROR: Unexpected error: Could not select record")
        print(e)

def update(table, set, where):
    connection = connect()
    print('#' * 20)
    try:
        with connection.cursor() as cursor:
            sql = f"UPDATE {table} SET {set} WHERE {where}"
            cursor.execute(sql)
            connection.commit()
            print(f"INFO: Record updated successfully in {table} table")
            disconnect(connection)
    except Exception as e:
        print("ERROR: Unexpected error: Could not update record")
        print(e)

def delete(table, where):
    try:
        connection = connect()
        print('#' * 20)
        with connection.cursor() as cursor:
            sql = f"DELETE FROM {table} WHERE {where}"
            cursor.execute(sql)
            connection.commit()
            print(f"INFO: Record deleted successfully from {table} table")
            disconnect(connection)
    except Exception as e:
        print("ERROR: Unexpected error: Could not delete record")
        print(e)

def drop_table(table):
    try:
        connection = connect()
        print('#' * 20)
        with connection.cursor() as cursor:
            sql = f"DROP TABLE IF EXISTS {table}"
            cursor.execute(sql)
            connection.commit()
            print(f"INFO: Table {table} dropped successfully")
            disconnect(connection)
    except Exception as e:
        print("ERROR: Unexpected error: Could not drop table")
        print(e)
