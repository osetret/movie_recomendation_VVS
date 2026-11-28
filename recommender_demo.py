# first version for recommendation system

import sqlite3
from math import sqrt

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

def build_film_vector(film):
    vector = {}
    for genre in film['genres']:
        vector[genre] = 1
    return vector 

def build_taste_vector(liked_genres):
    taste_vector = {}
    for genre in liked_genres:
        taste_vector[genre] = 1
    return taste_vector

def vector_length(weights):
    square_sum = 0
    for weight in weights.values():
        square_sum += weight**2
    return sqrt(square_sum)
    
def cosine_similarity(vector, taste_vector):
    cosine_sum = 0
    for genre_name, film_rating in vector.items():
        viewer_rating = taste_vector.get(genre_name, 0)
        cosine_sum += film_rating * viewer_rating
    length_for_vector = vector_length(vector)
    length_for_taste_vector = vector_length(taste_vector)
    if length_for_vector == 0 or length_for_taste_vector == 0:
        return 0
    return cosine_sum/(length_for_taste_vector * length_for_vector)

def score_for_film(film_vector, picked_genres):
    taste_vector = build_taste_vector(picked_genres)
    return cosine_similarity(film_vector, taste_vector)

def score_for_group(film, friends):
    scores = {}
    film_vector = build_film_vector(film)
    for name, liked_genres in friends.items():
        score_count = score_for_film(film_vector, liked_genres)
        scores[name] = score_count
    return scores

def match_moods(film, moods):
    picked_moods = film['moods']
    moods_similarity = []
    for mood in moods:
        if mood in picked_moods:
            moods_similarity.append(mood)
    return moods_similarity

def search_by_mood(films, moods):
    results = []
    for film in films:
        matches = match_moods(film, moods)
        if len(matches) != 0:
            results.append({'film': film, 'matched_moods': matches})
    results.sort(key=lambda result: len(result['matched_moods']), reverse=True)
    return results

def search_by_genre(films, genres):
    results = []
    for film in films:
        film_vector = build_film_vector(film)
        score = score_for_film(film_vector, genres)
        if score > 0:
            results.append({'film': film, 'score': score})
    results.sort(key=lambda result: result['score'], reverse=True)
    return results

def pick_film(films, friends):
    if len(films) == 0 or len(friends) == 0:
        return None
    else:
        best_film = None
        film_score = None
        for film in films:
            scores = score_for_group(film, friends)
            worst = min(scores.values())
            total = sum(scores.values())
            current_score = (worst, total)
            if film_score == None:
                film_score = current_score
                best_film = film
            elif film_score < current_score:
                film_score = current_score
                best_film = film
        return best_film











# тестовые данные для вывода просто в терминал
films = load_films('/Users/nv1a/Downloads/movies.db')

friends = {
    'Аня': ['action', 'comedy'],
    'Борис': ['drama'],
}

wanted_moods = ['динамичный']
selected_film = pick_film(films, friends)
vector = build_film_vector(selected_film)
friend = build_taste_vector(friends['Аня'])
similarity = cosine_similarity(vector, friend)
mood_results = search_by_mood(films, ['dark', 'funny'])
if len(mood_results[:3]) == 0:
    print('Ничего не найднено')
else:
    for result in mood_results[:3]:
        movie = result['film']
        title = movie['title']
        matches = result['matched_moods']
        print(title, matches)
genre_results = search_by_genre(films, ['comedy'])
if len(genre_results[:3]) == 0:
    print('Ничего не найднено')
else:
    for result in genre_results[:3]:
        movie = result['film']
        title = movie['title']
        score = result['score']
        print(title, score)

print(selected_film, round(similarity, 3))