from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
restaurant = Table('restaurant', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=100)),
    Column('address', String(length=100)),
    Column('rating', Integer),
)

orders = Table('orders', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('time', DATETIME),
    Column('restaurant', VARCHAR(length=100)),
    Column('rating', INTEGER),
)

orders = Table('orders', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('time', DateTime),
    Column('restaurant', String(length=100)),
    Column('restaurant_id', Integer),
    Column('customer_id', Integer),
)

menu_item = Table('menu_item', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('description', VARCHAR(length=1000)),
    Column('frequency', INTEGER),
    Column('avg', INTEGER),
    Column('category', VARCHAR(length=64)),
    Column('dietaryRestriction', VARCHAR(length=200)),
    Column('restaurant', VARCHAR(length=100)),
    Column('price', INTEGER),
)

menu_item = Table('menu_item', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('description', String(length=1000)),
    Column('frequency', Integer),
    Column('rating_sum', Integer),
    Column('category', String(length=64)),
    Column('dietaryRestriction', String(length=200)),
    Column('restaurant_id', Integer),
    Column('price', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['restaurant'].create()
    pre_meta.tables['orders'].columns['rating'].drop()
    post_meta.tables['orders'].columns['customer_id'].create()
    post_meta.tables['orders'].columns['restaurant_id'].create()
    pre_meta.tables['menu_item'].columns['avg'].drop()
    pre_meta.tables['menu_item'].columns['restaurant'].drop()
    post_meta.tables['menu_item'].columns['rating_sum'].create()
    post_meta.tables['menu_item'].columns['restaurant_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['restaurant'].drop()
    pre_meta.tables['orders'].columns['rating'].create()
    post_meta.tables['orders'].columns['customer_id'].drop()
    post_meta.tables['orders'].columns['restaurant_id'].drop()
    pre_meta.tables['menu_item'].columns['avg'].create()
    pre_meta.tables['menu_item'].columns['restaurant'].create()
    post_meta.tables['menu_item'].columns['rating_sum'].drop()
    post_meta.tables['menu_item'].columns['restaurant_id'].drop()
