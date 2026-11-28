# first version for recommendation system
import sys
from catalog import load_films
from recommender import pick_film, build_film_vector, build_taste_vector, cosine_similarity, search_by_mood, search_by_genre

# тестовые данные для вывода просто в терминал
if len(sys.argv) < 2:
    print('Надо указать путь к БД')
    sys.exit()
else:
    db_path = sys.argv[1]
films = load_films(db_path)

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