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

itemsInOrders = db.Table('items_in_orders',
                         db.Column('order_id', db.Integer, db.ForeignKey('menu_item.id')),
                         db.Column('item_id', db.Integer, db.ForeignKey('orders.id')))

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True)
    restaurant = db.Column(db.String(100), index=True)
    rating = db.Column(db.Integer)
    items = db.relationship('MenuItem', secondary=itemsInOrders, lazy='dynamic', backref=db.backref('orders', lazy='dynamic'))

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    dietary = db.Column(db.String(200))
