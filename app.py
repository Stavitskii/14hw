import json

from flask import Flask, jsonify
from utils import *



app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False #Не меняет расположение столбцов, остается как в запросе SELECT
app.config['JSON_AS_ASCII'] = False

@app.route('/movie/<title>')
def get_by_movie_title(title):
    try:
        result = get_by_title(title)
        return result
    except:
        return "Not a video found"


@app.route('/movie/<int:year_first>/to/<int:year_last>')
def get_movie_by_years(year_first, year_last):
    result = get_by_release_year(year_first, year_last)
    if len(result) > 0:
        return jsonify(result)
    else:
        return "Not a video found"


@app.route('/rating/<rating>')
def get_movie_by_rating(rating):
    try:
        result = get_by_rating(rating)
        return jsonify(result)
    except:
        return "Not a video found"

@app.route('/genre/<genre>')
def get_movie_by_genre(genre):
    try:
        result = get_by_genre(genre)
        if len(result) > 0:
            return jsonify(result)
        else:
            return "Not a video found"
    except:
        return "Bad request"






if __name__ == "__main__":
    app.run(debug=True)



