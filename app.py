from flask import Flask, render_template, request
import requests

app = Flask(__name__)

CLIENT_ID = "6ea226f7"  # temporary demo key

@app.route("/", methods=["GET", "POST"])
def home():
    from flask import Flask, render_template, request
import requests

app = Flask(__name__)

CLIENT_ID = "YOUR_CLIENT_ID"   # apni Jamendo key

@app.route("/", methods=["GET", "POST"])
def home():
    songs = []

    # TRENDING SONGS (default)
    url = f"https://api.jamendo.com/v3.0/tracks/?client_id={CLIENT_ID}&format=json&limit=12&order=popularity_total"

    # SEARCH SONGS
    if request.method == "POST":
        query = request.form["song"]
        url = f"https://api.jamendo.com/v3.0/tracks/?client_id={CLIENT_ID}&format=json&limit=12&search={query}"

    response = requests.get(url).json()
    songs = response["results"]

    return render_template("index.html", songs=songs)

if __name__ == "__main__":
    app.run()
