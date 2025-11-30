from flask import Blueprint, url_for, redirect, request, render_template, flash, session, make_response, current_app
from .forms import LoginForm, RegistrationForm, UpdateAccountForm, ChangePasswordForm
from .. import db
from .models import User
from flask_login import login_user, login_required, current_user, logout_user

import os
import secrets
from PIL import Image

from datetime import datetime

users_bp = Blueprint(
    'users', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/users/static'
)

@users_bp.route("/hi/<string:name>")
def greetings(name):
    age = request.args.get("age", None, int)
    return render_template(
        "users/hi.html",
        name=name.upper(), 
        age=age, 
        title="Greeting Page" 
    )

@users_bp.route("/admin")
def admin():
    to_url = url_for(
        "users.greetings", 
        name="administrator", 
        age=45, 
        _external=True
    )
    return redirect(to_url)

@users_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))

    if form.validate_on_submit():
        
        hashed_password = User.hash_password(form.password.data)

        user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()
        
        flash("Your account has been created! You can now log in.", "success")
        
        return redirect(url_for('users.login')) 

    return render_template("users/register.html", title="Registration", form=form)


@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username_or_email = form.username.data  
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(username=username_or_email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id  
            session['username'] = user.username 

            login_user(user, remember=form.remember.data)
            
            current_app.logger.info(f"Successful login for user: {user.username}")
            
            remember_msg = "with 'remember me'" if remember else "without 'remember me'"
            flash(f"Login successful, {username_or_email}! ({remember_msg})", 'success')
            
            return redirect(url_for('users.account'))
        else:
            current_app.logger.warning(f"Failed login attempt for user: {username_or_email}")
            flash('Invalid username or password.', 'error') 
            return redirect(url_for('users.login'))
            
    elif request.method == 'POST':
        current_app.logger.debug(f"Login form validation failed. Errors: {form.errors}")
        flash("Login failed. Please check the form errors.", "error")
        
    return render_template("users/login.html", title="Login Page", form=form)

@users_bp.route("/profile", methods=["GET", "POST"])
def profile():
    username = session.get("username")
    
    if not username:
        flash("Please log in to view this page.", "warning")
        return redirect(url_for("users.login"))

    # Handle form submissions on the profile page
    if request.method == "POST":
        # Create a response object to modify cookies before sending
        response = make_response(redirect(url_for("users.profile")))
        
        action = request.form.get("action")

        if action == "set_theme":
            theme = request.form.get("theme_choice", "light")
            response.set_cookie("theme", theme, max_age=365*24*60*60) # Add max_age
            flash(f"Theme changed to {'dark' if theme == 'dark' else 'light'}", "success")

        elif action == "add_cookie":
            key = request.form.get("cookie_key")
            value = request.form.get("cookie_value")
            expiry = request.form.get("cookie_expiry") # In days

            if not key or not value:
                flash("Key and Value are required.", "error")
            elif key in ["session", "theme", "csrf_token"]: # Added csrf_token
                flash("This key is reserved by the system.", "error")
            else:
                max_age = None
                if expiry and expiry.isdigit():
                    max_age = int(expiry) * 24 * 60 * 60  # Convert days to seconds
                
                response.set_cookie(key, value, max_age=max_age)
                flash(f"Cookie '{key}' was successfully added.", "success")

        elif action == "delete_cookie":
            key = request.form.get("cookie_key_delete")
            if not key:
                flash("A key must be specified.", "error")
            elif key in ["session", "csrf_token"]:
                flash("Cannot delete a protected cookie.", "error")
            else:
                response.delete_cookie(key)
                flash(f"Cookie '{key}' has been deleted.", "success")

        elif action == "delete_all":
            deleted_count = 0
            for key in request.cookies:
                if key not in ["session", "csrf_token"]:
                    response.delete_cookie(key)
                    deleted_count += 1
            flash(f"Successfully deleted {deleted_count} cookie(s).", "success")
            
        return response

    # For a GET request, just render the profile page
    return render_template(
        "users/profile.html",
        title="Profile",
        username=username,
    )

@users_bp.route("/logout")
def logout():
    session.pop("username", None)
    logout_user()

    flash("You have been logged out.", "success")

    response = make_response(redirect(url_for("users.login")))
    response.delete_cookie("theme")
    return response

@users_bp.route("/set-theme/<theme_name>")
def set_theme(theme_name):
    """
    A simple GET route to quickly set the theme cookie.
    Redirects the user back to the page they came from.
    """
    if theme_name not in ("light", "dark"):
        theme_name = "light"  # Default to light theme
    
    # Redirect back to the previous page, or to profile as a fallback
    redirect_to = request.referrer or url_for("users.profile")
    resp = make_response(redirect(redirect_to))
    
    # Set the cookie to expire in 1 year
    max_age_seconds = 365 * 24 * 60 * 60
    resp.set_cookie("theme", theme_name, max_age=max_age_seconds)
    
    flash(f"Theme changed to {theme_name}.", "info")
    return resp

@users_bp.route("/users")
@login_required
def list_users():
    users = User.query.order_by(User.username).all()

    user_count = len(users)

    return render_template(
        "users/list_users.html",
        title="User List",
        users=users,
        user_count=user_count
    )

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    images_folder = os.path.join(current_app.blueprints['users'].root_path, 'static/images')
    original_path = os.path.join(images_folder, picture_fn)
    thumb_path = os.path.join(images_folder, 'thumb_' + picture_fn)

    i = Image.open(form_picture)

    i.save(original_path)

    i.thumbnail((128, 128))
    i.save(thumb_path)

    return picture_fn

@users_bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@users_bp.route("/account", methods=["GET","POST"])
@login_required
def account():
    form = UpdateAccountForm()
    pwd_form = ChangePasswordForm()

    if form.submit.data and form.validate():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        
        db.session.commit()
        flash('Ваш акаунт успішно оновлено!', 'success')
        return redirect(url_for('users.account'))
    
    if pwd_form.submit_pass.data and pwd_form.validate():
        if current_user.check_password(pwd_form.old_password.data):
            hashed_password = User.hash_password(pwd_form.new_password.data)
            current_user.password = hashed_password
            
            db.session.commit()
            flash('Ваш пароль успішно змінено!', 'success')
            return redirect(url_for('users.account'))
        else:
            flash('Старий пароль введено невірно.', 'error')

    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    image_file = url_for('users.static', filename='images/' + (current_user.image or 'profile_default.jpg'))

    return render_template(
            "users/account.html", 
            title="Мій акаунт", 
            user=current_user, 
            form=form, 
            pwd_form=pwd_form, 
            image_file=image_file
        )