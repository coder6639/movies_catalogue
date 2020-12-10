from flask import Flask, render_template, request
from movies_catalogue import tmdb_client

app = Flask(__name__)


@app.route("/")
def homepage():
    selected_list = request.args.get("list_name", "popular")
    movies = tmdb_client.get_movies(8, list_name=selected_list)
    return render_template("homepage.html", movies=movies, current_list=selected_list)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    people = tmdb_client.get_single_movie_cast(movie_id)
    image_url = tmdb_client.get_poster_url(tmdb_client.get_single_image(movie_id), "w780")
    return render_template("movie_details.html", movie=details, people=people, image=image_url)


if __name__ == "__main__":
    app.run(debug=True)
