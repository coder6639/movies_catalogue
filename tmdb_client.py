import requests
import random


API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0ZDkwYmFjYTJlMmExMDZjNWExODc1NDM0YmM1NGM3ZSIsInN1YiI6IjVmZDBkMmViOGU4NzAyMDA0MGQ2MzcxYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Ix5Fbko9r_sERcW0Z7C1A6NrqxGZ29ozxs03TirquLI"


def get_popular_movies():
    endpoint = "https://api.themoviedb.org/3/movie/popular"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_movies_list(list_name):
    endpoint = f"https://api.themoviedb.org/3/movie/{list_name}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json()


def get_poster_url(path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    if path:
        total_url = base_url + size + path
        return total_url
    else:
        return "https://upload.wikimedia.org/wikipedia/commons/f/fc/No_picture_available.png"


def get_movies(how_many, list_name="popular"):
    selection = get_movies_list(list_name)["results"]
    movies = []
    while len(movies) != how_many:
        lucky_guess = random.randint(1, len(selection) - 1)
        if selection[lucky_guess] not in movies:
            movies.append(selection[lucky_guess])
    return movies


def get_single_movie(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_single_movie_cast(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()["cast"]


def get_single_image(movie_id):
    image_list = []
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)

    if response.json()["backdrops"]:
        for item in response.json()["backdrops"]:
            image_list.append(item["file_path"])

        chosen_image = image_list[random.randint(1, len(response.json()["backdrops"]) - 1)]
        return chosen_image
    else:
        return "https://upload.wikimedia.org/wikipedia/commons/f/fc/No_picture_available.png"


def search_movie(search_query):
    endpoint = f"https://api.themoviedb.org/3/search/movie?query={search_query}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    response = response.json()

    return response["results"]


def airing_today():
    endpoint = "https://api.themoviedb.org/3/tv/airing_today"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json()["results"]