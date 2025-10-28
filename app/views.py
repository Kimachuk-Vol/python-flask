from . import app
from .forms import ContactForm
from flask import render_template, flash, redirect, url_for, request

@app.route('/')
def resume():
    return render_template('resume.html', title="Моє Резюме")

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data
        log_message = (
            f"CONTACT_FORM: Name={name}, Email={email}, "
            f"Subject={subject}, Message={message}"
        )
        app.logger.info(log_message)
        flash(
            f"Thank you, {name}! Your message ({email}) has been successfully submitted.",
            "success"
        )
        return redirect(url_for('contacts'))
    if request.method == 'POST':
        flash("Submission error! Please check the highlighted fields.", "error")
    return render_template('contacts.html', title="Контактна Форма", form=form)