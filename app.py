from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import requests

app = Flask(__name__)
app.secret_key = "harshmusic"

CLIENT_ID = "YOUR_JAMENDO_CLIENT_ID"


# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS playlist (username TEXT, title TEXT, audio TEXT)")

    conn.commit()
    conn.close()

init_db()


# ---------- LOGIN ----------
@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form["username"]
        p=request.form["password"]

        conn=sqlite3.connect("users.db")
        c=conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p))
        user=c.fetchone()

        if user:
            session["user"]=u
            return redirect("/home")

        c.execute("INSERT INTO users VALUES (?,?)",(u,p))
        conn.commit()
        session["user"]=u
        return redirect("/home")

    return render_template("login.html")


# ---------- HOME ----------
@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/")
    return render_template("index.html",user=session["user"])


# ---------- SONG API ----------
@app.route("/songs")
def songs():
    url=f"https://api.jamendo.com/v3.0/tracks/?client_id={CLIENT_ID}&format=json&limit=12"
    data=requests.get(url).json()

    tracks=[]
    for t in data["results"]:
        tracks.append({
            "title":t["name"],
            "artist":t["artist_name"],
            "audio":t["audio"],
            "image":t["album_image"]
        })

    return jsonify(tracks)


# ---------- SAVE PLAYLIST ----------
@app.route("/save",methods=["POST"])
def save():
    user=session["user"]
    title=request.form["title"]
    audio=request.form["audio"]

    conn=sqlite3.connect("users.db")
    c=conn.cursor()
    c.execute("INSERT INTO playlist VALUES (?,?,?)",(user,title,audio))
    conn.commit()
    conn.close()

    return "saved"


# ---------- GET PLAYLIST ----------
@app.route("/playlist")
def playlist():
    user=session["user"]

    conn=sqlite3.connect("users.db")
    c=conn.cursor()
    c.execute("SELECT title,audio FROM playlist WHERE username=?",(user,))
    data=c.fetchall()

    songs=[{"title":i[0],"audio":i[1]} for i in data]
    return jsonify(songs)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)