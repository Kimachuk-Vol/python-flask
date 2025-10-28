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
    name = StringField(
        "Ім'я", 
        validators=[
            DataRequired(message="Це поле обов'язкове."), 
            Length(min=4, max=10, message="Ім'я повинно бути від 4 до 10 символів.")
        ]
    )
    email = EmailField(
        "Email", 
        validators=[
            DataRequired(message="Це поле обов'язкове."), 
            Email(message="Некоректний email-адрес.")
        ]
    )
    phone = StringField(
        "Телефон", 
        validators=[
            DataRequired(message="Це поле обов'язкове."), 
            Regexp(
                r'^\+380\d{9}$', 
                message="Телефон має бути у форматі +380xxxxxxxxx"
            )
        ]
    )
    subject = SelectField(
        "Тема", 
        choices=[
            ('job_offer', 'Пропозиція роботи'),
            ('cooperation', 'Запит на співпрацю'),
            ('feedback', 'Відгук про проєкт'),
            ('question', 'Загальне питання'),
            ('other', 'Інше')
        ],
        validators=[DataRequired(message="Будь ласка, оберіть тему.")]
    )
    message = TextAreaField(
        "Повідомлення", 
        render_kw={"rows": 5, "cols": 40}, 
        validators=[
            DataRequired(message="Це поле обов'язкове."), 
            Length(max=500, message="Повідомлення не може перевищувати 500 символів.")
        ]
    )
    submit = SubmitField("Надіслати")

class LoginForm(FlaskForm):
    username = StringField(
        "Ім'я користувача",
        validators=[
            DataRequired(message="Будь ла ласка, введіть логін або email.")
        ]
    )
    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(message="Будь ласка, введіть пароль."),
            Length(min=4, max=10, message="Пароль має бути від 4 до 10 символів.")
        ]
    )
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField("Увійти")