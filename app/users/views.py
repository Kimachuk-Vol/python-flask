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
            flash('Неправильний пароль або логін!','error')
        else:
            session['username'] = request.form['username']
            flash('Ви успішно залогінені!','success')
            return redirect(url_for('users.profile'))
    return render_template("users/login.html",title="Login")

@users_bp.route("/profile", methods=["GET", "POST"])
def profile():
    username = session.get("username")
    if not username:
        flash("Please log in to view this page.", "warning")
        return redirect(url_for("users.login"))

    # --- ОБРОБКА POST (всіх форм) ---
    if request.method == "POST":
        # Ми створюємо відповідь-редирект.
        # Всі дії з cookies будуть застосовані до *цієї* відповіді.
        response = make_response(redirect(url_for("users.profile")))
        
        # 'action' - це приховане поле, яке каже нам, яка форма була відправлена
        action = request.form.get("action")

        # 3. Вибір теми
        if action == "set_theme":
            theme = request.form.get("theme_choice", "light")
            response.set_cookie("theme", theme)
            flash(f"Тему змінено на {'темну' if theme == 'dark' else 'світлу'}", "success")

        # 5. Додати кукі
        elif action == "add_cookie":
            key = request.form.get("cookie_key")
            value = request.form.get("cookie_value")
            expiry = request.form.get("cookie_expiry")

            if not key or not value:
                flash("Ключ та Значення є обов'язковими.", "error")
            elif key in ["session", "theme"]:
                flash("Цей ключ зарезервовано системою.", "error")
            else:
                max_age = None
                if expiry and expiry.isdigit():
                    max_age = int(expiry) * 24 * 60 * 60  # у секундах
                
                response.set_cookie(key, value, max_age=max_age)
                flash(f"Cookie '{key}' успішно додано.", "success")

        # 6. Видалити кукі за ключем
        elif action == "delete_cookie":
            key = request.form.get("cookie_key_delete")
            if not key:
                flash("Потрібно вказати ключ.", "error")
            elif key in ["session"]:
                flash("Неможливо видалити сесійне cookie.", "error")
            else:
                response.delete_cookie(key)
                flash(f"Cookie '{key}' видалено.", "success")

        # 7. Видалити всі кукі
        elif action == "delete_all":
            deleted_count = 0
            for key in request.cookies:
                if key != "session":
                    response.delete_cookie(key)
                    deleted_count += 1
            flash(f"Успішно видалено {deleted_count} cookie(s).", "success")
        return response
    theme = request.cookies.get("theme", "light")

    return render_template(
        "users/profile.html",
        title="Profile",
        username=username,
    )

@users_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out.", "success")
    # Видаляємо також cookie теми при виході
    response = make_response(redirect(url_for("users.login")))
    response.delete_cookie("theme")
    return response

@users_bp.route("/set-theme/<theme_name>")
def set_theme(theme_name):
    """
    Встановлює кольорову схему, зберігаючи її в кукі.
    """
    if theme_name not in ("light", "dark"):
        theme_name = "light" 
    redirect_to = request.referrer or url_for("users_bp.profile")
    resp = make_response(redirect(redirect_to))
    max_age_seconds = 365 * 24 * 60 * 60
    resp.set_cookie("theme", theme_name, max_age=max_age_seconds)
    flash(f"Тему змінено на {theme_name}.", "info")
    return resp  