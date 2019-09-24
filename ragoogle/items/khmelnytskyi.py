# -*- coding: utf-8 -*-
import scrapy
from .base import HashedItem


class MbuItem(HashedItem):
    order_no = scrapy.Field()
    order_date = scrapy.Field()
    customer = scrapy.Field()
    obj = scrapy.Field()
    obj_purpose = scrapy.Field()
    address_street = scrapy.Field()
    address_street_number = scrapy.Field()
    cancellation = scrapy.Field()
    scan_url = scrapy.Field()

    def get_dedup_fields(self):
        return ["order_date", "order_no"]
