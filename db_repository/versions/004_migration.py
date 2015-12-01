from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
item_in_order = Table('item_in_order', pre_meta,
    Column('itemID', INTEGER, primary_key=True, nullable=False),
    Column('orderID', INTEGER, primary_key=True, nullable=False),
)

items_in_orders = Table('items_in_orders', post_meta,
    Column('order_id', Integer),
    Column('item_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['item_in_order'].drop()
    post_meta.tables['items_in_orders'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['item_in_order'].create()
    post_meta.tables['items_in_orders'].drop()
