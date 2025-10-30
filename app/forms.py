from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    TextAreaField, 
    SubmitField, 
    SelectField, 
    EmailField,
    BooleanField,  
    PasswordField,  
)
from wtforms.validators import (
    DataRequired, 
    Length, 
    Email, 
    Regexp
)

class ContactForm(FlaskForm):
    """
    A form for users to send a contact message.
    It includes fields for name, email, phone, subject, and a message.
    """
    
    """User's full name."""
    name = StringField(
        "Name", 
        validators=[
            DataRequired(message="This field is required."), 
            Length(min=4, max=10, message="Name must be between 4 and 10 characters.") 
        ]
    )
    
    """User's email address for reply."""
    email = EmailField(
        "Email", 
        validators=[
            DataRequired(message="This field is required."), 
            Email(message="Invalid email address.")
        ]
    )
    
    """User's phone number in Ukrainian format (+380xxxxxxxxx)."""
    phone = StringField(
        "Phone", 
        validators=[
            DataRequired(message="This field is required."), 
            Regexp(
                r'^\+380\d{9}$', 
                message="Phone must be in the format +380xxxxxxxxx"
            )
        ]
    )
    
    """A dropdown to select the purpose of the contact message."""
    subject = SelectField(
        "Subject", 
        choices=[
            ('general_question', 'General Question'),
            ('job_offer', 'Job Offer'),
            ('cooperation', 'Cooperation Request'),
            ('feedback', 'Project Feedback'),
            ('other', 'Other')
        ],
        validators=[DataRequired(message="Please select a subject.")]
    )
    
    """The main content of the user's message."""
    message = TextAreaField(
        "Message", 
        render_kw={"rows": 5, "cols": 40}, 
        validators=[
            DataRequired(message="This field is required."), 
            Length(max=500, message="Message cannot exceed 500 characters.")
        ]
    )
    
    """The button to submit the contact form."""
    submit = SubmitField("Send Message")

class LoginForm(FlaskForm):
    """
    A form for users to log in to their account.
    It includes fields for username/email, password, and a 'remember me' checkbox.
    """
    
    """The user's registered username or email address."""
    username = StringField(
        "Username or Email", # Made label more descriptive
        validators=[
            DataRequired(message="Please enter your username or email.")
        ]
    )
    
    """The user's password."""
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Please enter your password."),
            Length(min=6, message="Password must be at least 6 characters.") # Removed max length for password
        ]
    )
    
    """A checkbox to keep the user logged in."""
    remember = BooleanField("Remember Me")
    
    """The button to submit the login form."""
    submit = SubmitField("Log In")