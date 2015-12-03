from flask import render_template, request, jsonify, abort, redirect, url_for, session
import datetime
from app import app, db
from app.models import MenuItem, Orders, Restaurant, Suggestions, Customers

@app.route('/')
@app.route('/index')
def index():
    rlist = Restaurant.query.order_by(Restaurant.name)
    menu = MenuItem.query.all()
    return render_template('index.html',
                           title='Home',
                           rlist=rlist,
                           menu=menu)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logged_in')
def logged_in():
    email = request.args.get('email')
    user = Customers.query.get(email)
    if user is None:
        session['uemail'] = email
        return redirect(url_for('dietary'))
    else:
        session['username'] = user.username
        session['uemail'] = user.id
        session['udietary'] = user.dietary
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session['username'] = None
    session['uemail'] = None
    session['dietary'] = None
    return index()

@app.route('/dietary')
def dietary():
    return render_template('user.html')

@app.route('/submit_dietary')
def submit_dietary():
    user = Customers()
    user.name = request.args.get('name')
    user.dietary = request.args.get('dietary')
    user.email = session['uemail']
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/submit_order')
def submit_order():
    order = Orders()
    order.time = datetime.datetime.now()
    restaurant_id = session['restaurant_id']
    for item in request.args.getlist('array[]'):
        menuItem = MenuItem.query.filter_by(name=item).first()
        freq = menuItem.frequency
        if freq is None:
            menuItem.frequency = 1
        else:
            menuItem.frequency += 1
        item_id = menuItem.id
        for paired_item in request.args.getlist('array[]'):
            if item != paired_item:
                paired_item_id = MenuItem.query.filter_by(name=paired_item).first().id
                suggestionPair = Suggestions.query.filter_by(current_id=item_id, next_id=paired_item_id).first()
                if suggestionPair is not None:
                    new_weight = suggestionPair.weight + 1
                    suggestionPair.weight = new_weight
        order.items.append(menuItem)
    db.session.add(order)
    restaurant = Restaurant.query.get(restaurant_id)
    restaurant.orders.append(order)
    db.session.commit()
    return jsonify({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/view_orders')
def view_orders():
    restaurant = {'name': 'MIGA'}
    orders = Orders.query.all()
    return render_template('orders.html',
                           orders=orders,
                           restaurant=restaurant)

# Orders.query.get(id) should return a order object
# which should then get deleted upon the .delete()
@app.route('/del_orderItem')
def del_orderItem():
    id = request.args.get('id')
    delItem = Orders.query.get(id)
    db.session.delete(delItem)
    db.session.commit()
    return view_orders()

@app.route('/update_order')
def update_order():
    orderid = request.args.get('id')
    currOrder = Orders.query.get(orderid)
    for item in request.args.getlist('array[]'):
        menuitem = MenuItem.query.filter_by(name=item).first()
        currOrder.items.append(menuitem)
    db.session.commit()
    return index()
    # get orderr
    # add items like the other one adds items to a new order

@app.route('/dashboard')
def dash():
    rlist = Restaurant.query.order_by(Restaurant.name)
    menu = MenuItem.query.all()
    return render_template('merchSide.html',
                           rlist=rlist,
                           menu=menu)

@app.route('/dashboard/<restaurant_id>')
def dashboard(restaurant_id):
    session['restaurant_id'] = restaurant_id
    rest = Restaurant.query.get(restaurant_id)
    items = rest.items.order_by(MenuItem.frequency.desc())
    return render_template('dashboard.html',
                           restaurant=rest,
                           rid=restaurant_id,
                           common_items=items)

@app.route('/menu')
def menu():
    user = {'nickname': 'Saurabh Sinha'}  # fake user, 411 prof.
    restaurant = {'name': 'MIGA'}
    menu = MenuItem.query.all()
    return render_template('menu.html',
                           title='Home',
                           user=user,
                           restaurant=restaurant,
                           menu=menu)

@app.route('/restaurant/<restaurant_id>')
def restaurant(restaurant_id):
    session['restaurant_id'] = restaurant_id
    rest = Restaurant.query.get(restaurant_id)
    itemlist = rest.items
    return render_template('menu.html',
                           restaurant=rest,
                           rid=restaurant_id,
                           items=itemlist)

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/get_suggestions')
def get_suggetions():
    limit = 4 #Change number of items returned

    item_name = request.args.get('item_name')
    print(item_name)
    item_id = MenuItem.query.filter_by(name=item_name).first().id
    if not item_id:
        abort(422)
    menu_suggestions = db.session.query(MenuItem, Suggestions).join(Suggestions, Suggestions.next_id==MenuItem.id).filter(Suggestions.current_id==item_id).order_by(Suggestions.weight.desc()).limit(limit).all()
    return_list = list()
    for item in menu_suggestions:
        return_list.append(item.MenuItem.name)

    return_item = {'items': return_list}
    return jsonify(return_item)

@app.route('/order/<order_id>')
def user_order(order_id):
    print(order_id)
    order = Orders.query.get(order_id)
    return render_template('view_order.html',
                           order=order)

app.secret_key = "wM'P\xf2H\x99Vc\x1d-\xc0\x1a\x9c!\xcb\xc94\x8f\xac\x01*\x8c\x89"