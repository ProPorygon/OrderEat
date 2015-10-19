from scrapy.item import Item, Field


class Website(Item):

    name = Field()
    descrip = Field()
    # category = Field()
    price = Field()