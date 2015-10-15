from app import db
from app.models import MenuItem
import json
import sys

with open('menu.json') as data_file:
    data = json.load(data_file)

for item in data["menu"]["menuItems"]:
    name = item["name"]
    description = item["descrip"]
    category = item["category"]
    price = item["price"]
    menuItem = MenuItem(name=name, description=description, category=category, price=price)
    db.session.add(menuItem)
db.session.commit()