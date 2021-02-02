"""Blogly application."""
from flask import Flask, redirect, render_template, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


app.config['SECRET_KEY'] = "turtlesrock"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def users_redirect():
    """Redirect home page to users for now"""
    return redirect("/users")

@app.route("/users")
def show_users():
    """Retrieve all the users from the user table and render them to the page"""
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/users/new")
def add_user_form():
    """Show form to add new user"""
    return render_template("add_user.html")

@app.route("/users/new", methods=["POST"])
def add_user():
    """ Retrieve form data to add a new user and update the database with the new user"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['image_url']
    img_url = img_url if img_url else None

    user = User(first_name=first_name, last_name=last_name, image_url=img_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user_info(user_id):
    """Show user's profile page"""
    user = User.query.get_or_404(user_id)
    return render_template("user_page.html", user=user)

@app.route("/users/<int:users_id>/edit")
def edit_user_form(users_id):
    """Show edit form for a user to edit a profile"""
    user = User.query.get_or_404(users_id)
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:users_id>/edit", methods=["POST"])
def edit_user(users_id):
    """ Retrieve form data for the edit to a users profile and update their profile in the database"""
    user = User.query.get_or_404(users_id)

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['image_url']
    img_url = img_url if img_url else None

    user.update_info(first_name, last_name, img_url)

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route("/users/<int:users_id>/delete", methods=["POST"])
def delete_user(users_id):
    """ Delete a user from the database"""
    user = User.query.get_or_404(users_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")




