from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from sqlalchemy.testing import db
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    date = db.Column(db.DateTime, index=True, unique=True)
    description = db.Column(db.String(120), index=True, unique=True)
    a2s = db.relationship('ActorToShow', backref='Show', lazy='dynamic')
    p2s = db.relationship('ProducerToShow', backref='Show', lazy='dynamic')

class ActorToShow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("actor.id"), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey("show.id"), nullable=False)

class ProducerToShow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producer_id = db.Column(db.Integer, db.ForeignKey("producer.id"), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey("show.id"), nullable=False)

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120), index=True)
    lastname = db.Column(db.String(120), index=True)
    age = db.Column(db.DateTime)
    a2s = db.relationship('ActorToShow', backref='Actor', lazy='dynamic')

class Producer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120), index=True)
    lastname = db.Column(db.String(120), index=True)
    age = db.Column(db.DateTime)
    p2s = db.relationship('ProducerToShow', backref='Producer', lazy='dynamic')

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

