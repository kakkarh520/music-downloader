from flask import Flask, render_template, request
import requests

app = Flask(__name__)

CLIENT_ID = "6ea226f7"  # temporary demo key

@app.route("/", methods=["GET", "POST"])
def home():
    songs = []

    if request.method == "POST":
        query = request.form["song"]

        url = f"https://api.jamendo.com/v3.0/tracks/?client_id={CLIENT_ID}&format=json&limit=10&search={query}"

        response = requests.get(url).json()
        songs = response["results"]

    return render_template("index.html", songs=songs)

if __name__ == "__main__":
    import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
