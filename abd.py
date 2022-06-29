import sqlite3

with sqlite3.connect('netflix.db') as conn:
    cur = conn.cursor()
    query = """ SELECT *
                    FROM netflix
    """

    cur.execute(query)

    for row in cur.fetchall():
        print(row)
