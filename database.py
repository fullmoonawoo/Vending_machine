import mysql.connector as mysql


vending_db = mysql.connect(
    host="localhost",
    user="root",
    password="SLUMerican44",
    database="vending_db"
)

my_crsr = vending_db.cursor()


def create_table(machine, columns, primary_key=None):
    if primary_key:
        command = f'CREATE TABLE {str(machine)} ({columns}, PRIMARY KEY ({primary_key}))'
        my_crsr.execute(command)
    else:
        command = f'CREATE TABLE {str(machine)} {columns}'
        my_crsr.execute(command)


def make_sum(what, where):
    command = f'SELECT SUM({what}) FROM {where}'
    my_crsr.execute(command)
    summa = my_crsr.fetchall()
    return summa


def refresh_db(parameter, where, item=None):
    if parameter and where and item:
        command = f'SELECT {parameter} FROM {where} WHERE {item}'
        my_crsr.execute(command)
        db_results = my_crsr.fetchall()
        return db_results
    elif parameter and where:
        command = f'SELECT {parameter} FROM {where}'
        my_crsr.execute(command)
        db_results = my_crsr.fetchall()
        return db_results


def insert_db(where, titles, what, col_for_update=None):
    if where and col_for_update:
        command = f'INSERT INTO {where} {titles} VALUES {what} ON DUPLICATE KEY UPDATE {col_for_update}'
        my_crsr.execute(command)
        vending_db.commit()
    else:
        command = f'INSERT INTO {where} {titles} VALUES {what}'
        my_crsr.execute(command)
        vending_db.commit()


def update_db(where, title, result1, what, price=None):
    if price:
        command = f'UPDATE {where} SET {title} = {result1} WHERE tovar = {what} and cena_s_dph between {price - 0.01} and {price + 0.01}'
        my_crsr.execute(command)
        vending_db.commit()
    else:
        command = f'UPDATE {where} SET {title} = {result1} WHERE tovar = {what}'
        my_crsr.execute(command)
        vending_db.commit()


def remove_from_db(where, what):
    command = f'DELETE FROM {where} WHERE {what}'
    my_crsr.execute(command)
    vending_db.commit()
