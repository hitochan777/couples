# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import the database object from the main app module
from app import db

# Import module models (i.e. User)
from app.model.users import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_users = Blueprint('users', __name__, url_prefix='/users')

# Set the route and accepted methods
@mod_users.route('/api/all', methods=['GET'])
def get_all():
    users = User.query.all()
    return

@mod_users.route('/', methods=["GET"])
def index():
    users = User.query.all()
    return render_template("users/index.html", users=users) 

@mod_users.route('/add', methods=["GET", "POST"])
def add():
    form = AddRecipeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            filename = images.save(request.files['user_image'])
            url = images.url(filename)
            new_user = User(form.recipe_title.data, form.recipe_description.data, current_user.id, True, filename, url)
            db.session.add(new_recipe)
            db.session.commit()
        else:
            flash_errors(form)
            flash("入力内容が間違っているため、ユーザー登録できませんでした。")

        return redirect(url_for('recipes.user_recipes'))

    return render_template("users/index.html", users=users) 
