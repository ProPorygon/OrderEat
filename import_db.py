from app import db
from app.models import MenuItem, Restaurant
import json
import sys

with open('menu.json') as data_file:
    data = json.load(data_file)

for item in data["menu"]["menuItems"]:
    name = item["name"]
    description = item["descrip"]
    category = item["category"]
    price = item["price"]
    restaurant = 'Sakanaya'
    menuItem = MenuItem(name=name, description=description, category=category, price=price)
    restaraunt_table = Restaurant.query.filter_by(name=restaurant).first()
    db.session.add(menuItem)
    restaraunt_table.items.append(menuItem)
db.session.commit()