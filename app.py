from flask import Flask, render_template

app = Flask(__name__)
    
@app.route('/')
def resume():
    return render_template('resume.html', title="Моє Резюме")

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Контактна Форма")

if __name__ == '__main__':
    app.run() # Launch built-in web server and run this Flask webapp, debug=True