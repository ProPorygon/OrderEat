from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Saurabh Sinha'}  # fake user, 411 prof.
    restaurant = {'name': 'Mia Za\'s'}
    return render_template('index.html',
                           title='Home',
                           user=user,
                           restaurant=restaurant)