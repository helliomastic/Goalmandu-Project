from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,LoginManager
from sqlalchemy.exc import IntegrityError


db = SQLAlchemy()
loginM = LoginManager()
loginM.login_view = 'apps.login'

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False,default="User")
    futsals = db.relationship('Futsal', backref='staff', lazy=True)
    bookings = db.relationship('Bookings', backref='user', lazy=True)
    is_admin= db.Column(db.Boolean,default=False)

@loginM.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Futsal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(50))
    laltitude = db.Column(db.String(20))
    longitude = db.Column(db.String(20))
    contacts = db.Column(db.String(100))
    bookings = db.relationship('Bookings', backref='futsal', lazy=True)
    price = db.Column(db.Integer)
    weekend_price = db.Column(db.Integer)

    def get_price(self, is_weekend):
        if is_weekend:
            return self.weekend_price
        else:
            return self.price
class Bookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    futsal_id = db.Column(db.Integer, db.ForeignKey('futsal.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.Time, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def ftime(self):
        return self.time.strftime('%I%p')

    def fday(self):
        return self.date.strftime('%A')

def init_app(app):
    db.init_app(app)
    loginM.init_app(app)

    with app.app_context():
        print("creating tables.....")
        db.create_all()