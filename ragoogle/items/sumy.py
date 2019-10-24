# -*- coding: utf-8 -*-
import scrapy
from .base import HashedItem


class MbuItem(HashedItem):
    address = scrapy.Field()
    cancellation = scrapy.Field()
    cancellation_url = scrapy.Field()
    changes = scrapy.Field()
    customer = scrapy.Field()
    location_name = scrapy.Field()
    obj = scrapy.Field()
    order_date = scrapy.Field()
    order_no = scrapy.Field()
    scan_url = scrapy.Field()

    def get_dedup_fields(self):
        return ["order_date", "order_no", "location_name"]
