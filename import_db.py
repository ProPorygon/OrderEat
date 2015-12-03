from app import db
from app.models import MenuItem, Restaurant
import json

with open('menu.json') as data_file:
    data = json.load(data_file)

for item in data["menu"]["menuItems"]:
    name = item["name"]
    description = item["description"]
    category = item["category"]
    price = item["price"]
    restaurant = item['restaurant']
    dietary = item['dietaryRestriction']
    menuItem = MenuItem(name=name, description=description, category=category, price=price, dietaryRestriction=dietary)
    restaraunt_table = Restaurant.query.filter_by(name=restaurant).first()
    db.session.add(menuItem)
    restaraunt_table.items.append(menuItem)
db.session.commit()