from app import db

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(1000))
    frequency = db.Column(db.Integer, index=True)
    rating_sum = db.Column(db.Integer, index=True)
    category = db.Column(db.String(64))
    dietaryRestriction = db.Column(db.String(200))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    price = db.Column(db.Integer, index=True)

itemsInOrders = db.Table('items_in_orders',
                         db.Column('order_id', db.Integer, db.ForeignKey('menu_item.id')),
                         db.Column('item_id', db.Integer, db.ForeignKey('orders.id')))

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True)
    restaurant = db.Column(db.String(100), index=True)
    items = db.relationship('MenuItem', secondary=itemsInOrders, lazy='dynamic', backref=db.backref('orders', lazy='dynamic'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    dietary = db.Column(db.String(200))
    orders = db.relationship('Orders', backref='customer', lazy='dynamic')

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    address = db.Column(db.String(100))
    rating = db.Column(db.Integer, index=True)
    items = db.relationship('MenuItem', backref='restaurant', lazy='dynamic')
    orders = db.relationship('Orders', backref='restaurant', lazy='dynamic')
