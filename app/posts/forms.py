from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    TextAreaField, 
    SubmitField, 
    SelectField,
    BooleanField,
    DateTimeLocalField,
    SelectMultipleField
)
from wtforms.validators import (
    DataRequired, 
    Length
)
from datetime import datetime
from .models import PostCategory  

class PostForm(FlaskForm):
    # title - StringField, required, max 150 
    title = StringField(
        "Заголовок", 
        validators=[DataRequired(), Length(max=150)]
    )
    # content - TextAreaField, required
    content = TextAreaField(
        "Вміст", 
        validators=[DataRequired()]
    )
    # is_active (boolean) 
    is_active = BooleanField(
        "Активний (відображається на сайті)", 
        default='checked'
    )
    
    # posted (DateTimeLocalField)
    posted = DateTimeLocalField(
        "Дата публікації",
        format='%Y-%m-%dT%H:%M',  
        default=datetime.utcnow,
        validators=[DataRequired()]
    )

    user = SelectField(
        "Автор",
        coerce=int,
        validators=[DataRequired()]
    )
    
    # category (SelectField) 
    category = SelectField(
        "Категорія",
        choices=[(cat.value, cat.name.capitalize()) for cat in PostCategory],
        validators=[DataRequired()]
    )
    
    # submit
    submit = SubmitField("Створити пост")