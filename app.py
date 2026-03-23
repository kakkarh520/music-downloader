from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

CLIENT_ID = "6ea226f7"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/songs")
def songs():
    url = f"https://api.jamendo.com/v3.0/tracks/?client_id={CLIENT_ID}&format=json&limit=12"
    response = requests.get(url)
    data = response.json()

    tracks = []
    for track in data["results"]:
        tracks.append({
            "title": track["name"],
            "artist": track["artist_name"],
            "audio": track["audio"],
            "image": track["album_image"]
        })

    return jsonify(tracks)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
