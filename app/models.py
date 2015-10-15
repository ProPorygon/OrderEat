from app import db

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(1000))
    frequency = db.Column(db.Integer, index=True)
    avg = db.Column(db.Integer, index=True)
    category = db.Column(db.String(64))
    dietaryRestriction = db.Column(db.String(200))
    restaurant = db.Column(db.String(100))
    price = db.Column(db.Integer, index=True)

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True)
    restaurant = db.Column(db.String(100), index=True)
    rating = db.Column(db.Integer)

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    dietary = db.Column(db.String(200))