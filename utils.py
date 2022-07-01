import sqlite3

from collections import Counter


class DbConnect:
    """Создает подключение к базе данных через класс"""
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def __del__(self):
        self.cur.close()
        self.con.close()


def execute_query(query):
    """Создает подключение к базе данных через функцию"""
    with sqlite3.connect('netflix.db') as con:
        cur = con.cursor()
        cur.execute(query)
        result = cur.fetchall()
    return result


def get_by_title(title):
    """Ищет самый новый фильм по названию"""
    db_connect = DbConnect('netflix.db')
    db_connect.cur.execute(
        f"""SELECT title, country, release_year, listed_in, description
            FROM netflix
            WHERE title LIKE '%{title}%'
            ORDER BY release_year DESC
            LIMIT 1
        """)
    result = db_connect.cur.fetchone()
    return {
        "title": result[0],
        "country": result[1],
        "release_year": result[2],
        "genre": result[3],
        "description": result[4]
    }


def get_by_release_year(year_first, year_last):
    """Создает список фильмов в диапазоне двух указанных годов, не более 100 строк"""
    db_connect = DbConnect('netflix.db')
    db_connect.cur.execute(
        f"""SELECT title, release_year
            FROM netflix
            WHERE release_year BETWEEN {year_first} AND {year_last}
            LIMIT 100
        """)
    result = db_connect.cur.fetchall()
    res_list = []
    for i in result:
        res_list.append({
            "title": i[0],
            "release_year": i[1],
        })

    return res_list


def get_by_rating(rating):
    """Фильтрует видео по группам: дети, семья, взрослые"""
    rating_parameters = {
        "children": "'G'",
        "Family": "'G', 'PG', 'PG-13'",
        "adult": "'R', 'NC-17'"
    }
    if rating not in rating_parameters:
        return "The group is undefined"
    db_connect = DbConnect('netflix.db')
    db_connect.cur.execute(
        f"""SELECT title, rating, description
            FROM netflix
            WHERE rating IN ({rating_parameters[rating]})
            """)
    result = db_connect.cur.fetchall()
    res_list = []
    for i in result:
        res_list.append({
            "title": i[0],
            "rating": i[1],
            "description": i[2]
        })
    return res_list


def get_by_genre(genre):
    """Ищет 10 самых свежих фильмов по жанру"""
    db_connect = DbConnect('netflix.db')
    db_connect.cur.execute(
        f"""SELECT title, description
            FROM netflix
            WHERE listed_in LIKE '%{genre}%'
            ORDER BY release_year DESC
            LIMIT 10
        """)
    result = db_connect.cur.fetchall()
    res_list = []
    for i in result:
        res_list.append({
            "title": i[0],
            "description": i[1],
        })
    return result


def cast_partners(actor1, actor2):
    """получает в качестве аргумента имена двух актеров, сохраняет всех актеров
    из колонки cast и возвращает список тех, кто играет с ними в паре больше 2 раз"""
    db_connect = DbConnect('netflix.db')
    db_connect.cur.execute(
        f"""SELECT `cast`
            FROM netflix
            WHERE `cast` LIKE '%{actor1}%' AND `cast` LIKE '%{actor2}%' 
        """)
    result = db_connect.cur.fetchall()
    actors_list = []
    for i in result:
        actors_list.extend(i[0].split(', '))
    counter = Counter(actors_list)
    res_llist = []
    for actor, count in counter.items():
        if actor not in [actor1, actor2] and count > 2:
            res_llist.append(actor)
    return res_llist


def search_by_params(movie_type, release_year, genre):
    """По типу видео (фильм или сериал), году выпуска и жанру выдает
     на выходе список названий видео с описаниями"""
    query = f"""SELECT title, description
            FROM netflix
            WHERE type = '{movie_type}' AND release_year = {release_year} AND listed_in LIKE  '%{genre}%'
        """
    result = execute_query(query)
    res_list = []
    for i in result:
        res_list.append({
            "title": i[0],
            "description": i[1],
        })
    return res_list


