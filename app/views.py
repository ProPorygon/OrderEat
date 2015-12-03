from flask import render_template, request, jsonify, abort, redirect, url_for, session
from flask.ext.session import Session
import datetime
from app import app, db
from app.models import MenuItem, Orders, Restaurant, Suggestions, Customers
from sqlalchemy import or_, and_

app.secret_key = "wM'P\xf2H\x99Vc\x1d-\xc0\x1a\x9c!\xcb\xc94\x8f\xac\x01*\x8c\x89"
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

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
    user = Customers.query.filter_by(email=email).first()
    if user is None:
        if email is not None:
            session['uemail'] = email
        print(session['uemail'])
        return redirect(url_for('dietary'))
    else:
        session['username'] = user.username
        session['uemail'] = user.id
        session['udietary'] = user.dietary
        return redirect(url_for('index'))

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

@app.route('/restaurant/<restaurant_id>')
def restaurant(restaurant_id):
    try:
        email = session['uemail']
    except:                         #using without accont
        session['restaurant_id'] = restaurant_id
        rest = Restaurant.query.get(restaurant_id)
        itemlist = rest.items
        return render_template('menu.html',
                               restaurant=rest,
                               rid=restaurant_id,
                               items=itemlist)
    else:                           #if account
        cust = Customers.query.get(email)
        newlist = db.session.query(MenuItem.name, MenuItem.price) \
                    .filter(MenuItem.restaurant_id == restaurant_id) \
                    .filter( \
                                or_( \
                                    ~and_((MenuItem.dietaryRestriction % 256 >= 128), (cust.dietary % 256 >= 128)), \
                                    ~and_((MenuItem.dietaryRestriction % 128 >= 64), (cust.dietary % 128 >= 64)), \
                                    ~and_((MenuItem.dietaryRestriction % 64 >= 32), (cust.dietary % 64 >= 32)), \
                                    ~and_((MenuItem.dietaryRestriction % 32 >= 16), (cust.dietary % 32 >= 16)), \
                                    ~and_((MenuItem.dietaryRestriction % 16 >= 8), (cust.dietary % 16 >= 8)), \
                                    ~and_((MenuItem.dietaryRestriction % 8 >= 4), (cust.dietary % 8 >= 4)), \
                                    ~and_((MenuItem.dietaryRestriction % 4 >= 2), (cust.dietary % 4 >= 2)), \
                                    ~and_(MenuItem.dietaryRestriction % 2 == 1, cust.dietary % 2 == 1)) \
                            ) \

                    # .filter( \
                    #             or_( \
                    #                 and_(cust.dietary / 1024 == 0, (MenuItem.dietaryRestriction / 1024 == cust.dietary / 1024)), \
                    #                 and_(cust.dietary % 1024 < 512, (MenuItem.dietaryRestriction % 1024 >= 512) == (cust.dietary % 1024 >= 512)), \
                    #                 and_(cust.dietary % 512 < 256, (MenuItem.dietaryRestriction % 512 >= 256) == (cust.dietary % 512 >= 256)) \
                    #                 ) \
                    #         ) \

                    # .filter(MenuItem.dietaryRestriction / 512 == 1) \
                    # .filter(MenuItem.dietaryRestriction / 256 == 1) \
                    # .filter(MenuItem.dietaryRestriction / 128 == 1) \
                    # .filter(MenuItem.dietaryRestriction / 64 == 1) \
                    # .filter(MenuItem.dietaryRestriction / 32 == 1) \
                    # .filter(MenuItem.dietaryRestriction / 16 == 1) \
                    # .filter(MenuItem.dietaryRestriction / 8 == 1) \
                    # .filter(MenuItem.dietaryRestriction / 4 == 1) \
                    # .filter(MenuItem.dietaryRestriction / 2 == 1) \
                    # .filter(MenuItem.dietaryRestriction / 1 == 1) \

                    #.filter(MenuItem.dietaryRestriction.op('&')(1024) == 1)
#                    .filter(MenuItem.dietaryRestriction.op('&')(1024) == 1024) \
#                    .filter(MenuItem.dietaryRestriction.op('&')(2) != Customers.dietaryRestriction.op('&')(2)) \
 #                   .filter(Restaurant.dietaryRestriction.op('&')(4) != Customers.dietaryRestriction.op('&')(4)) \
  #                  .filter(Restaurant.dietaryRestriction.op('&')(8) != Customers.dietaryRestriction.op('&')(8)) \
   #                 .filter(Restaurant.dietaryRestriction.op('&')(16) != Customers.dietaryRestriction.op('&')(16)) \
    #                .filter(Restaurant.dietaryRestriction.op('&')(32) != Customers.dietaryRestriction.op('&')(32)) \
        for menu in newlist:
            print(menu.name)
        return render_template('menu.html',
                               restaurant=rest,
                               rid=restaurant_id,
                               items=newlist)

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