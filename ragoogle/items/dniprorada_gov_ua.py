# -*- coding: utf-8 -*-
import scrapy
from .base import HashedItem


class MbuItem(HashedItem):
    location_name = scrapy.Field()
    number_in_order = scrapy.Field()
    order_no = scrapy.Field()
    order_date = scrapy.Field()
    customer = scrapy.Field()
    obj = scrapy.Field()
    address = scrapy.Field()
    changes = scrapy.Field()
    cancellation = scrapy.Field()
    scan_url = scrapy.Field()
    scan_no = scrapy.Field()
    scan_date = scrapy.Field()

    def get_dedup_fields(self):
        return ["order_date", "order_no"]
