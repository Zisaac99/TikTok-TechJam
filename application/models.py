from application import db, login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__='user'

    # User table columns

    # Primary Key
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(1000))
    email = db.Column(db.String(1000))
    username = db.Column(db.String(1000))
    password = db.Column(db.String(1000))

    def get_id(self):
        return (self.user_id)

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
