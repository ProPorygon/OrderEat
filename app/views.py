from flask import render_template, request
from app import app
from app.models import MenuItem, Orders

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Saurabh Sinha'}  # fake user, 411 prof.
    restaurant = {'name': 'Mia Za\'s'}
    menu = MenuItem.query.all()
    return render_template('index.html',
                           title='Home',
                           user=user,
                           restaurant=restaurant,
                           menu=menu)

@app.route('/submit_order')
def submit_order():
    print(request.args)
    for value in request.args.listvalues():
        print(value)
    return index()