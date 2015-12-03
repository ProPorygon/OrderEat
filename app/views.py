from flask import render_template, request, jsonify, abort
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

@app.route('/submit_order')
def submit_order():
    order = Orders()
    order.time = datetime.datetime.now()
    restaurant_name = request.args.get('restaurant') #TODO add restaurant argument in submitted order
    for item in request.args.getlist('array[]'):
        menuItem = MenuItem.query.filter_by(name=item).first()
        freq = menuItem.frequency
        if freq is None:
            menuItem.frequency = 1
        else:
            menuItem.frequency += 1
        # print(menuItem.name)
        # print(menuItem.frequency)
        item_id = menuItem.id
        for paired_item in request.args.getlist('array[]'):
            if item != paired_item:
                paired_item_id = MenuItem.query.filter_by(name=paired_item).first().id
                suggestionPair = Suggestions.query.filter_by(current_id=item_id, next_id=paired_item_id).first()
                new_weight = suggestionPair.weight + 1
                suggestionPair.weight = new_weight
        print(menuItem.name)
        order.items.append(menuItem)
    db.session.add(order)
    restaurant = Restaurant.query.filter_by(name='MIGA').first()
    restaurant.orders.append(order)
    db.session.commit()
    return index()

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
def dashboard():
    restaurant = request.args.get('restaurant')
    common_items = MenuItem.query.order_by(MenuItem.frequency.desc())
        #all()
    #filter_by(name=restaurant).first()
      #.filter_by(restaurant=Restaurant.query.filter_by(name=restaurant).first()).order_by(MenuItem.frequency.desc())
    # popular_items = db.query(db.cast(MenuItem.rating_sum/MenuItem.frequency, db.Integer))
    # popular_items = popular_items.order_by(popular_items.desc())  #Should probably do something like a view or as here
    return render_template('dashboard.html',
                           common_items=common_items)

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

@app.route('/<restaurant_id>')
def restaurant(restaurant_id):
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

    item_id = request.args.get('item_id')
    print(item_id)
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