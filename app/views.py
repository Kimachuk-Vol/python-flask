from . import app
from flask import render_template

@app.route('/')
def resume():
    return render_template('resume.html', title="Моє Резюме")

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Контактна Форма")