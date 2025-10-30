from . import app
from .forms import ContactForm
from flask import render_template, flash, redirect, url_for, request

@app.route('/')
def resume():
    """
    Renders the main resume page.
    This is the homepage of the site.
    """
    return render_template('resume.html', title="My Resume")

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    """
    Handles the contact page logic.

    For GET requests, it displays the contact form.
    For POST requests, it validates the form data. If valid, it logs
    the submission, flashes a success message, and redirects. If invalid,
    it flashes an error message and re-renders the form with errors.
    """
    form = ContactForm()
    # This block executes on a POST request with valid data
    if form.validate_on_submit():
        # Retrieve data from the validated form
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data

        # Log the received message for administrative purposes
        log_message = (
            f"CONTACT_FORM: Name={name}, Email={email}, Phone={phone}, "
            f"Subject={subject}, Message={message}"
        )
        app.logger.info(log_message)
        
        # Flash a success message to the user
        flash(
            f"Thank you, {name}! Your message has been successfully submitted.",
            "success"
        )
        
        # Redirect to the same page to prevent form re-submission on refresh
        return redirect(url_for('contacts'))
    
    # This block executes on a POST request if validation fails
    if request.method == 'POST':
        flash("Submission error! Please check the highlighted fields and try again.", "error")
    
    # This renders the template for a GET request or after a failed POST
    return render_template('contacts.html', title="Contact Form", form=form)