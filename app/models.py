from app import db,login_manager
from datetime import datetime
from flask_login import UserMixin




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True,)
    username = db.Column(db.String(15),nullable=False,unique=True)
    email = db.Column(db.String(30),nullable=False,unique=True)
    image_file=db.Column(db.String(20),nullable=False,default='default.png')
    password = db.Column(db.String(10),nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username},{self.email}')"


class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True,)
    title = db.Column(db.String(35),nullable=False,unique=True)
    date_posted = db.Column(db.DateTime(30),nullable=False,default=datetime.utcnow)
    image_file=db.Column(db.String(20),nullable=True)
    content = db.Column(db.Text(10),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)


    def __repr__(self):
        return f"User('{self.title},{self.date_posted}')"







