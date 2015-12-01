from scrapy.item import Item, Field


class Website(Item):

    name = Field()
    description = Field()
    category = Field()
    price = Field()