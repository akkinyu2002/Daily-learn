from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"

# 🔗 MongoDB connection
# IMPORTANT: Replace the string below with your actual connection string
client = MongoClient(os.getenv("MONGO_URI"))
db = client.notes_app
users = db.users
notes = db.notes


# ---------- AUTH ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = users.find_one({"username": request.form["username"]})
        if user and check_password_hash(user["password"], request.form["password"]):
            session["user"] = user["username"]
            return redirect("/notes")
        return "Invalid credentials"
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if users.find_one({"username": request.form["username"]}):
            return "User already exists"

        users.insert_one({
            "username": request.form["username"],
            "password": generate_password_hash(request.form["password"])
        })
        return redirect("/")
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------- NOTES ----------
@app.route("/notes", methods=["GET", "POST"])
def user_notes():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        notes.insert_one({
            "username": session["user"],
            "text": request.form["note"]
        })

    user_notes = notes.find({"username": session["user"]})
    return render_template("notes.html", notes=user_notes)


@app.route("/delete/<id>")
def delete_note(id):
    # Ensure ObjectId is imported and used correctly
    try:
        notes.delete_one({"_id": ObjectId(id)})
    except:
        pass # Handle invalid ID gracefully or just ignore for MVP
    return redirect("/notes")


if __name__ == "__main__":
    app.run(debug=True)
