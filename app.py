from flask import Flask, render_template, request, url_for, redirect, flash
import tmdb_client
import datetime

app = Flask(__name__)
app.secret_key = b'2MSjdNsi7n@!N@#@$!@#sd'


@app.route("/")
def homepage():
    movie_lists = ["now_playing", "top_rated", "popular", "upcoming"]
    selected_list = request.args.get("list_type", "popular")
    if selected_list not in movie_lists:
        movies = tmdb_client.get_movies(8, list_name="popular")
        return render_template("homepage.html", movies=movies, selected_list="", movie_lists=movie_lists)
    else:
        movies = tmdb_client.get_movies(8, list_name=selected_list)
    return render_template("homepage.html", movies=movies, selected_list=selected_list, movie_lists=movie_lists)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    people = tmdb_client.get_single_movie_cast(movie_id)[:12]
    image_url = tmdb_client.get_poster_url(tmdb_client.get_single_image(movie_id), "w780")
    return render_template("movie_details.html", movie=details, people=people, image=image_url)


@app.route("/search")
def search():
    search_query = request.args.get("q", "")
    if search_query:
        movies = tmdb_client.search_movie(search_query=search_query)
    else:
        movies = []
    return render_template("search.html", movies=movies, search_query=search_query)


@app.route("/airing")
def airing():
    today = datetime.date.today()
    movies = tmdb_client.airing_today()
    return render_template("airing.html", movies=movies, today=today)


FAVORITES = set()


@app.route("/favorites/add", methods=["POST"])
def add_to_favorites():
    data = request.form
    movie_id = data.get("movie_id")
    title = data.get("movie_title")
    if movie_id and title:
        FAVORITES.add(movie_id)
    flash(f"{title} added to favourites")
    return redirect(url_for("homepage"))


@app.route("/favorites")
def favorites():
    movies = []
    if FAVORITES:
        for item in FAVORITES:
            result = tmdb_client.get_single_movie(item)
            movies.append(result)

    return render_template("favorites.html", movies=movies)


if __name__ == "__main__":
    app.run(debug=True)
