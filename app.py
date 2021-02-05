"""Blogly application."""
from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post, Tag, PostTag
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

###### USER ROUTES ######

@app.route("/")
def index():
    """Redirect home page to users for now"""
    top_5_posts = []
    posts = Post.query.all()

    for p in posts[::-1]:
        if len(top_5_posts) >= 5:
            break
        else:
            top_5_posts.append(p)
    
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


######## ROUTES FOR BLOG POSTS ######## 

@app.route("/users/<int:users_id>/posts/new")
def show_post_form(users_id):
    """ Show form for a user to add a post"""
    user = User.query.get_or_404(users_id)
    tags = Tag.query.all()
    return render_template("add_post.html", user=user, tags=tags)


@app.route("/users/<int:users_id>/posts/new", methods=["POST"])
def add_post(users_id):
    """ Retrieve form data from a user and update the database with their new post."""

    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tags')

    post = Post(title=title, content=content, user_id=users_id)

    for t in tags:
        tag = Tag.query.get(t)
        tag.posts.append(post)
    
    db.session.add(post)
    db.session.commit()


    return redirect(f"/users/{users_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """ Show a users Post"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    tags = post.tags
    return render_template("post_page.html", post=post, user=user, tags=tags)


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

######## ROUTES FOR TAGS ########

@app.route("/tags")
def show_tags():
    """ Show a list of the tags that have been created"""
    tags= Tag.query.all()
    return render_template("tags.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def show_tag_post(tag_id):
    """ Show a list of the posts that have a certain tag"""
    tag = Tag.query.get_or_404(tag_id)
    tagged_posts = tag.posts
    return render_template("tag_page.html", tag=tag, tagged_posts=tagged_posts)


@app.route("/tags/new")
def show_add_tag():
    """ Show add tag form """
    return render_template("add_tag.html")


@app.route("/tags/new", methods=["POST"])
def add_tag():
    """ Add a tag to the database and redirect to the tag list """
    name = request.form["name"]

    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def show_tag_edit(tag_id):
    """ Show edit form for a tag """
    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """ Update the tag in the database"""
    tag = Tag.query.get_or_404(tag_id)
    name = request.form["name"]

    tag.name = name

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags/<int:tag_id>")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """ Delete a tag"""
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")