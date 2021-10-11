from django.db import connection


def dict_fetch_all(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_all_ingredient(self, group):
    with connection.cursor() as cursor:
        cursor.execute(f"select id, name from loginApp_pre_ingredient where group = {group}")
        res = dict_fetch_all(cursor)

    return res
