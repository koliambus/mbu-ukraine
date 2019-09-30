# -*- coding: utf-8 -*-
import scrapy
from .base import HashedItem


class MbuItem(HashedItem):
    order_no = scrapy.Field()
    order_date = scrapy.Field()
    customer = scrapy.Field()
    obj = scrapy.Field()
    address = scrapy.Field()
    changes = scrapy.Field()
    cancellation = scrapy.Field()
    status = scrapy.Field()

    def get_dedup_fields(self):
        return ["order_date", "order_no"]