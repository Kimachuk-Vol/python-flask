from datetime import datetime
from .. import db
import enum

class PostCategory(enum.Enum):
    news = 'news'
    publication = 'publication'
    tech = 'tech'
    other = 'other'

class Post(db.Model):
    """
    ORM-модель Post
    """
    __tablename__ = 'posts'

    # Поле id (Integer, Primary Key)
    id = db.Column(db.Integer, primary_key=True)
    # Поле title (String(150), Not Null)
    title = db.Column(db.String(150), nullable=False)
    # Поле content (Text, Not Null)
    content = db.Column(db.Text, nullable=False)
    # Поле posted (DateTime, Default = datetime.utcnow)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    # Поле category (Enum)
    category = db.Column(db.Enum(PostCategory))
    #Поле is_active (Boolean, Default = True)
    is_active = db.Column(db.Boolean, default=True)
    # Поле author (String(20), Default = 'Anonymous')
    author = db.Column(db.String(20), default='Anonymous')

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', content='{self.content}', author='{self.author}')>"
