from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search():
    query = request.args.get("q")

    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch6:{query}", download=False)

    songs = []

    for v in result["entries"]:
        songs.append({
            "title": v["title"],
            "id": v["id"],
            "thumbnail": f"https://img.youtube.com/vi/{v['id']}/hqdefault.jpg",
            "url": f"https://www.youtube.com/watch?v={v['id']}"
        })

    return jsonify(songs)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
