# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_sqlitem import SqlItem
from scrapy_sqlitem.sqlitem import SqlAlchemyItemMeta
from .database.business import BusinessModel


class BusinessItem(SqlItem, metaclass=SqlAlchemyItemMeta):
    sqlmodel = BusinessModel

    pass
