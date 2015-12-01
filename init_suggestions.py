from app import db
from app.models import MenuItem, Suggestions

items = MenuItem.query.all()
for item1 in items:
    for item2 in items:
        if item1 != item2:
            suggestion = Suggestions(current_id=item1.id, next_id=item2.id)
            db.session.add(suggestion)
db.session.commit()