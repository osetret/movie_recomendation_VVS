from math import sqrt

def build_film_vector(film):
    vector = {}
    # все 1 - жанр есть у фильма, остальные не хранятся в словаре (вес 0)
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
    # функция вернет 0, если хотя бы один вектор нулевой (предотвращение ошибки деления на 0)
    if length_for_vector == 0 or length_for_taste_vector == 0:
        return 0
    return cosine_sum/(length_for_taste_vector * length_for_vector)

def score_for_film(film_vector, picked_genres):
    taste_vector = build_taste_vector(picked_genres)
    return cosine_similarity(film_vector, taste_vector)

def score_for_group(film, friends):
    scores = {}
    # вектор фильма - одинаков для всех, предпочтения у каждого свои 
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
    # теги также сохраняются для пояснения выбора
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
            # принцип наименьшего недовольства, сначала ориентируемся на худшую оценку, а затем только на сумму
            current_score = (worst, total)
            if film_score == None:
                film_score = current_score
                best_film = film
            elif film_score < current_score:
                film_score = current_score
                best_film = film
        return best_film