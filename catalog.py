import sqlite3

def load_films(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.execute('''
        SELECT id, title, genres FROM movies
        ORDER BY id
    ''').fetchall()
    tag_rows = connection.execute('''
        SELECT movieId, tag FROM tags
    ''').fetchall()
    connection.close()
    tags_by_film = {}
    loaded_films = []
    for movie_id, tag in tag_rows:
        if len(tag) == 0:
            continue
        else:
            tag = tag.lower().strip()
            if movie_id not in tags_by_film:
                tags_by_film[movie_id] = []    
            tags_by_film[movie_id].append(tag)
    for id, title, genres in cursor:
        if len(genres) == 0 or genres == '(no genres listed)':
            genres = []
        else:
            genres = genres.lower()
            genres = genres.split('|')
        film_card = {'id': id, 'title': title, 'genres': genres, 'moods': tags_by_film.get(id, [])}
        loaded_films.append(film_card)
    return loaded_films