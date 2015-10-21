from flask import render_template, request
import datetime
from app import app, db
from app.models import MenuItem, Orders

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Saurabh Sinha'}  # fake user, 411 prof.
    restaurant = {'name': 'Sakanaya'}
    menu = MenuItem.query.all()
    return render_template('index.html',
                           title='Home',
                           user=user,
                           restaurant=restaurant,
                           menu=menu)

@app.route('/submit_order')
def submit_order():
    order = Orders()
    order.time = datetime.datetime.now()
    for item in request.args.getlist('array[]'):
        menuItem = MenuItem.query.filter_by(name=item).first()
        print(menuItem.name)
        order.items.append(menuItem)
    db.session.add(order)
    db.session.commit()
    return index()

@app.route('/view_orders')
def view_orders():
    restaurant = {'name': 'Sakanaya'}
    orders = Orders.query.all()
    return render_template('orders.html',
                           orders=orders,
                           restaurant=restaurant)
