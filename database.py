import mysql.connector as mysql
#from collections import deque
#from datetime import *
#from time import strftime


# Queue
def enqueue(queue, value):
    queue.append(value)


def dequeue(queue):
    queue.popleft()


def front(queue):
    return queue[0]


def empty_queue(queue):
    return len(queue) == 0


vending_db = mysql.connect(
    host="localhost",
    user="root",
    password="SLUMerican44",
    database="vending_db"
)

my_crsr = vending_db.cursor()


def create_table(machine):
    command = f'CREATE TABLE {machine} (tovar VARCHAR(20), pred.cena float(4), pocet_kusov int)'
    my_crsr.execute(command)


def refresh_db(parameter, item=None):
    if parameter and item:
        command = f'SELECT {parameter} FROM vending_db.sklad WHERE tovar = {item}'
        my_crsr.execute(command)
        db_results = my_crsr.fetchall()
        return db_results
    elif parameter:
        command = f'SELECT {parameter} FROM vending_db.sklad'
        my_crsr.execute(command)
        db_results = my_crsr.fetchall()
        return db_results


def insert_db(where, titles, what):
    command = f'INSERT INTO {where} {titles} VALUES {what}'
    my_crsr.execute(command)
    vending_db.commit()


def update_db(where, title, result1, what, price):
    command = f'UPDATE {where} SET {title} = {result1} WHERE tovar = {what} and cena_s_dph between {price - 0.01} and {price + 0.01}'
    my_crsr.execute(command)
    vending_db.commit()


def say_hello():
    print("Hello meeeen !")
