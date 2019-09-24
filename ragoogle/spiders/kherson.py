# -*- coding: utf-8 -*-
import json
import re

import scrapy
from scrapy import Selector

from ragoogle.items.kherson import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class KhersonSpider(scrapy.Spider):
    name = "kherson"
    allowed_domains = ["mvk.kherson.ua"]
    start_urls = ["http://mvk.kherson.ua/scripts/connect.php?sEcho=5&iColumns=9&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=1000000&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=false&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=false&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&mDataProp_7=7&sSearch_7=&bRegex_7=false&bSearchable_7=true&bSortable_7=true&mDataProp_8=8&sSearch_8=&bRegex_8=false&bSearchable_8=false&bSortable_8=true&sSearch=&bRegex=false&iSortCol_0=1&sSortDir_0=desc&iSortCol_1=2&sSortDir_1=desc&iSortingCols=2&_=1569332736190"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["number_in_order", "order_no", "order_date", "customer", "obj", "address", "changes",
                               "cancellation", "scan_url"],
    }

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        for row in jsonresponse["aaData"]:
            l = StripJoinItemLoader(item=MbuItem())
            l.add_value("number_in_order", row[0])
            l.add_value("order_no", row[2])
            l.add_value("order_date", row[1])
            l.add_value("customer", row[7])
            l.add_value("obj", row[3])
            l.add_value("address", row[4])
            l.add_value("changes", row[5])
            l.add_value("cancellation", row[6])
            l.add_value("scan_url", response.urljoin(row[8]) if row[8] else None)

            yield l.load_item()
