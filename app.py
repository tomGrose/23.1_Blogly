"""Blogly application."""
from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post
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
    top_5_posts = Post.query.limit(5)
    return render_template("home.html", posts=top_5_posts)

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
    posts = user.posts
    return render_template("user_page.html", user=user, posts=posts)


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


@app.route("/users/<int:users_id>/posts/new")
def show_post_form(users_id):
    """ Show form for a user to add a post"""
    user = User.query.get_or_404(users_id)
    return render_template("add_post.html", user=user)


@app.route("/users/<int:users_id>/posts/new", methods=["POST"])
def add_post(users_id):
    """ Retrieve form data from a user and update the database with their new post."""

    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id=users_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{users_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """ Show a users Post"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    return render_template("post_page.html", post=post, user=user)


@app.route("/posts/<int:post_id>/edit")
def show_edit_post(post_id):
    """Show the edit post form to update a post"""
    post = Post.query.get_or_404(post_id)

    return render_template("edit_post.html", post=post)



@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """ Delete a user's post from the database"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """ Retrieve form data for the edit to a users post and update their post in the database"""
    post = Post.query.get_or_404(post_id)

    title = request.form['title']
    content = request.form['content']

    post.update_post(title, content)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")