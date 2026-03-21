from flask import Flask, render_template, request, jsonify
import yt_dlp

# IMPORTANT — app first define hota hai
app = Flask(__name__)


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Search Songs
@app.route("/search")
def search():
    query = request.args.get("q")

    ydl_opts = {
        'quiet': True,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch10:{query}", download=False)

    songs = []

    for video in result["entries"]:
        if video.get("availability") == "private":
            continue

        songs.append({
            "title": video["title"],
            "id": video["id"]
        })

    return jsonify(songs[:5])


# Run Server
if __name__ == "__main__":
    app.run(debug=True)