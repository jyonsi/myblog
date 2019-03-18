import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    account = db.Column(db.String(10),unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    arts = db.relationship('Article',backref='u')
    def save(self):
        db.session.add(self)
        db.session.commit()


class ArticleType(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    type = db.Column(db.String(10),unique=True,nullable=False)
    arts = db.relationship('Article',backref='tp')

    __tablename__ = 'art_type'


class Article(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(30),unique=True,nullable=False)
    desc = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    # titleimg = db.Column(db.String(10),unique='False')
    views_count = db.Column(db.Integer,default=0)
    type = db.Column(db.Integer,db.ForeignKey('art_type.id'),nullable=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    comments = db.relationship('Comment',backref='com_art')

class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    owner = db.Column(db.String(10))
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now())
    article = db.Column(db.Integer,db.ForeignKey('article.id'),nullable=True)

