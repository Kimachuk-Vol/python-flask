from flask import Blueprint,flash, url_for, redirect, request, render_template, session, make_response

users_bp = Blueprint(
    'users', __name__,
    template_folder='templates',
    static_folder='static'
)

@users_bp.route("/hi/<string:name>") #/hi/ivan?age=45
def greetings (name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("users/hi.html",name=name, age=age, title="Greating Page")

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True,title="Greating Page")
    print(to_url)
    return redirect(to_url)

@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != 'kimachuk' or \
                request.form['password'] != 'volodymyr':
            flash('Invalid credentials','error')
        else:
            session['username'] = request.form['username']
            flash('You were successfully logged in','success')
            return redirect(url_for('users.profile'))
    return render_template("users/login.html",title="Login")

@users_bp.route("/profile", methods=["GET", "POST"])
def profile():
    username = session.get("username")
    if not username:
        flash("Please log in to view this page.", "warning")
        return redirect(url_for("users.login"))
    return render_template(
        "users/profile.html", title="Profile", username=username
    )