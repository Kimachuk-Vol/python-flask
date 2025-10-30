from flask import Blueprint, url_for, redirect, request, render_template, flash, session, make_response
from ..forms import LoginForm
from app import app

users_bp = Blueprint(
    'users', __name__,
    template_folder='templates',
    static_folder='static'
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
    """
    An admin route that demonstrates a redirect to another route
    within the blueprint, passing parameters.
    """
    # Build an external URL for the 'users.greetings' route
    to_url = url_for(
        "users.greetings", 
        name="administrator", 
        age=45, 
        _external=True
    )
    return redirect(to_url)

@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    """
    Handles the user login page.
    GET: Displays the login form.
    POST: Validates credentials and manages the user session.
    """
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        if username == 'kimachuk' and password == 'volodymyr':
            # Store username in the session
            session['username'] = username
            app.logger.info(f"Successful login for user: {username}")
            
            # Set feedback message based on 'remember me'
            remember_msg = "with 'remember me'" if remember else "without 'remember me'"
            flash(f"Login successful, {username}! ({remember_msg})", 'success')
            
            # Redirect to the user's profile page
            return redirect(url_for('users.profile'))
        else:
            # Failed authentication
            app.logger.warning(f"Failed login attempt for user: {username}")
            flash('Invalid username or password.', 'error') 
            
            # NOTE: Redirecting on a failed login clears the form.
            # It's often better UX to re-render the template:
            # return render_template("users/login.html", title="Login Page", form=form)
            # But sticking to your original logic:
            return redirect(url_for('users.login'))
            
    elif request.method == 'POST':
        # Form validation failed
        app.logger.debug(f"Login form validation failed. Errors: {form.errors}")
        flash("Login failed. Please check the form errors.", "error")
        
    # Render the login page for a GET request or after a failed validation
    return render_template("users/login.html", title="Login Page", form=form)

@users_bp.route("/profile", methods=["GET", "POST"])
def profile():
    """
    Displays the user's profile page, accessible only when logged in.
    Also handles POST requests for managing user preferences (theme)
    and custom cookies.
    """
    username = session.get("username")
    
    # If user is not in session, redirect to login
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
    """
    Logs the user out by clearing the session and 'theme' cookie.
    """
    # Remove the username from the session
    session.pop("username", None)
    flash("You have been logged out.", "success")
    
    # Create a response to redirect and clear cookies
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