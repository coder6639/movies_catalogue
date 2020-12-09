from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def homepage():
    movies = []
    for i in range(20):
        title = "tytuł" + str(i)
        movies.append(title)
    return render_template("homepage.html", movies=movies)


if __name__ == "__main__":
    app.run(debug=True)