import requests
import random


API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0ZDkwYmFjYTJlMmExMDZjNWExODc1NDM0YmM1NGM3ZSIsInN1YiI6IjVmZDBkMmViOGU4NzAyMDA0MGQ2MzcxYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Ix5Fbko9r_sERcW0Z7C1A6NrqxGZ29ozxs03TirquLI"


def call_tmdb_api(endpoint):
    full_url = f"https://api.themoviedb.org/3/{endpoint}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(full_url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_popular_movies():
    return call_tmdb_api("movie/popular")


def get_movies_list(list_name):
    return call_tmdb_api(f"movie/{list_name}")


def get_poster_url(path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    if path:
        total_url = base_url + size + path
        return total_url
    else:
        return "https://upload.wikimedia.org/wikipedia/" \
               "commons/f/fc/No_picture_available.png"


def get_movies(how_many, list_name="popular"):
    selection = get_movies_list(list_name)["results"]
    movies = []
    while len(movies) != how_many:
        lucky_guess = random.randint(1, len(selection) - 1)
        if selection[lucky_guess] not in movies:
            movies.append(selection[lucky_guess])
    return movies


def get_single_movie(movie_id):
    return call_tmdb_api(f"movie/{movie_id}")


def get_single_movie_cast(movie_id):
    return call_tmdb_api(f"movie/{movie_id}/credits")["cast"]


def get_single_image(movie_id):
    image_list = []
    response = call_tmdb_api(f"movie/{movie_id}/images")
    if response["backdrops"]:
        for item in response["backdrops"]:
            image_list.append(item["file_path"])

        if len(image_list) == 1:
            chosen_image = image_list[0]
        else:
            chosen_image = image_list[
                random.randint(0, len(image_list) - 1)]

        return chosen_image
    else:
        return "https://upload.wikimedia.org/wikipedia/" \
               "commons/f/fc/No_picture_available.png"


def search_movie(search_query):
    return call_tmdb_api(f"search/movie?query={search_query}")["results"]


def airing_today():
    return call_tmdb_api("tv/airing_today")["results"]
