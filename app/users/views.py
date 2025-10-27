from flask import Blueprint, url_for, redirect, request, render_template

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



