# import necessary pacakges
import os
import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import ivySchedule, standings
from helpers import ivyTeams, getNews

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///ncaa.db")

currentYear = datetime.now().year + 1


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# homepage route
@app.route("/")
def home():
    # call standings function to get current season's standings
    standings(currentYear)
    # initialize dynamic name for each year's ranking
    word = "ranking" + str(currentYear)
    # query database to access standing for select year
    schools = db.execute(
        f"SELECT Rank, School, ConfWin, ConfLoss, OvWin,OvLoss FROM {word}"
    )
    # drop the table after its used
    db.execute("DROP TABLE IF EXISTS {}".format(schools))
    # call getNews function to get recent news
    getNews()
    # query database to access recent news articles, dynamically update
    news = db.execute("SELECT * FROM articles")
    # drop the table after its used
    db.execute("DROP TABLE IF EXISTS {}".format(news))
    # call ivySchedule function to load this season's schedule
    ivySchedule(currentYear)
    # initialize dynamic name for each year's schedule
    schedule_cur_year = "schedule" + str(currentYear)
    # query database to acess schedule for select year
    schedule = db.execute(
        'SELECT Date, "Visitor/Neutral", "Home/Neutral" FROM {} '.format(
            schedule_cur_year
        )
    )
    # drop the table after its used
    db.execute("DROP TABLE IF EXISTS {}".format(schedule_cur_year))
    return render_template(
        "home.html",
        currentYear=currentYear,
        schools=schools,
        news=news,
        schedule=schedule,
    )

# login route
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username") or not request.form.get("password"):
            flash("Please fill in all fields.")
            return render_template("login.html")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
            flash("Invalid Username and/or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html" , currentYear=currentYear)


# register route
@app.route("/register", methods=["GET", "POST"])
def register():
    # user reached route via POST
    if request.method == "POST":
        # Get the username, password, and confirmation password from the user and return apology if they don't exist
        if not (username := request.form.get("username")):
            flash("Please enter a username.")
            return render_template("register.html")

        if not (password := request.form.get("password")):
            flash("Please enter a password")
            return render_template("register.html")

        if not (confirmation := request.form.get("confirmation")):
            flash("Please enter a confirmation password")
            return render_template("register.html")

        # Check if the username exists and return apology if it doesn't work
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 0:
            flash("Sorry, username already exists.")
            return render_template("register.html")

        # If the passwords don't match, return apology
        if password != confirmation:
            flash("The passwords don't match.")
            return render_template("register.html")

        # Insert the hashed password and username into the table
        user_id = db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?);",
            username,
            generate_password_hash(password),
        )

        # Store the user id in the session
        session["user_id"] = user_id

        # Flash registration
        flash("You are registered!")

        return redirect("/")

    # If the request method is get, render the register template
    if request.method == "GET":
        return render_template("register.html", currentYear=currentYear)


# route to logout
@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


# route to standings (post)
@app.route("/standingsMain/<int:year>")
def standingsIvy(year):
    """Return standings for a given year"""
    standings(year)
    # intialize dynamic name for certain school's standing
    # schools = "team" + str(year)
    ranking_cur_year = "ranking" + str(year)
    schools = db.execute("SELECT * FROM {}".format(ranking_cur_year))
    db.execute("DROP TABLE IF EXISTS {}".format(ranking_cur_year))
    return render_template(
        "standingsMain.html", schools=schools, currentYear=currentYear, year=year
    )


# route to schedule (post)
@app.route("/scheduleMain")
# route to teams (post)
def schedule():
    year = datetime.now().year + 1
    currentYear = str(datetime.now().year + 1)
    ivySchedule(year)
    schedule_cur_year = "schedule" + currentYear
    schedule = db.execute("SELECT * FROM {}".format(schedule_cur_year))
    db.execute("DROP TABLE IF EXISTS {}".format(schedule_cur_year))
    return render_template(
        "scheduleMain.html", schedule=schedule, year=year, currentYear=currentYear
    )


@app.route("/roster/<school>/<year>")
# this is hard coded though for rankings2023
def roster(school, year):
    """Get roster information for an year"""
    currentYear = datetime.now().year + 1
    ivyTeams(school, year)
    tableName = "team" + school + str(year)
    team = db.execute(f"SELECT * FROM {tableName}")
    db.execute(f"DROP TABLE IF EXISTS {tableName}")
    return render_template("roster.html", team=team, currentYear=currentYear, year=year, school = school)


@app.route("/team")
def team():
    # Retrieve user_id from the session
        user_id = session.get("user_id")

        # Fetch the followed teams for the user from the database
        followed_teams = db.execute("SELECT followed_team FROM user_followed_teams WHERE user_id = ?", user_id)
        followed_teams = [row['followed_team'] for row in followed_teams]

        return render_template("team.html", followed_teams=followed_teams, currentYear = currentYear)

@app.route("/newsMain")
def news():
    getNews()
    news = db.execute("SELECT * FROM articles")
    db.execute("DROP TABLE IF EXISTS articles")
    return render_template("newsMain.html", news=news, currentYear=currentYear)


# route to tickets (post, get)
@app.route("/tickets")
# route to teams (post)
def tickets():
    return render_template("tickets.html", currentYear=currentYear)


@app.route("/covid")
def covid():
    return render_template("covid.html", currentYear = currentYear)


@app.route("/following")
def yourTeams():
    # Check if user is logged in
    if "user_id" in session:
        # Retrieve user_id from session
        user_id = session["user_id"]

        ivySchedule(2024)

        followed_teams = db.execute("SELECT followed_team FROM user_followed_teams WHERE user_id = :user_id", user_id=user_id)

        games_by_team = {}

        for team in followed_teams:
            team_name = team['followed_team']

            games = db.execute(
    "SELECT * FROM schedule2024 WHERE LOWER([Home/Neutral]) = LOWER(:team) OR LOWER([Visitor/Neutral]) = LOWER(:team)",
    team=team_name.lower()
)


            games_by_team[team_name] = games

        return render_template('following.html', games_by_team=games_by_team, currentYear=currentYear)
    else:
        # Redirect to login page if user is not logged in
        return redirect("/login")


@app.route("/follow_team/<team_name>", methods=["POST"])
def follow_team(team_name):
    # Retrieve user_id from the session (you might need to adapt this based on your authentication mechanism)
    if "user_id" in session:
        user_id = session.get("user_id")
    # Continue with the rest of the code
        db.execute(
            "INSERT INTO user_followed_teams (user_id, followed_team) VALUES (?, ?)",
            user_id,
            team_name,
        )
        return {"success": True}, 200
    else:
        # Respond with an error (user not logged in)
        return {"success": False, "error": "User not logged in"}, 401

@app.route("/unfollow_team/<team_name>", methods=["POST"])
def unfollow_team(team_name):
    # Retrieve user_id from the session (you might need to adapt this based on your authentication mechanism)
    user_id = session.get("user_id")

    if user_id:
        # Delete the team from the user's followed teams
        # Adjust your database interaction based on your database model
        db.execute(
            "DELETE FROM user_followed_teams WHERE user_id = ? AND followed_team = ?",
            user_id,
            team_name,
        )
        return {"success": True}, 200
    else:
        # Respond with an error (user not logged in)
        return {"success": False, "error": "User not logged in"}, 401


app.run(host="0.0.0.0", port=8080)
