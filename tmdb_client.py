import requests
import random


def get_popular_movies():
    endpoint = "https://api.themoviedb.org/3/movie/popular"
    api_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0ZDkwYmFjYTJlMmExMDZjNWExODc1NDM0YmM1NGM3ZSIsInN1YiI6IjVmZDBkMmViOGU4NzAyMDA0MGQ2MzcxYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Ix5Fbko9r_sERcW0Z7C1A6NrqxGZ29ozxs03TirquLI"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()


def get_poster_url(path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    total_url = base_url + size + path
    return total_url


def get_movies(how_many):
    selection = get_popular_movies()["results"]
    movies = []
    while len(movies) != how_many:
        lucky_guess = random.randint(1, len(selection) - 1)
        if selection[lucky_guess] not in movies:
            movies.append(selection[lucky_guess])
    return movies


