# -*- coding: utf-8 -*-
import json
import re

import cssselect
import scrapy
from scrapy import Selector

from ragoogle.items.registry_uga_kharkov_ua import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class KharkivSpider(scrapy.Spider):
    name = "registry_uga_kharkov_ua"
    allowed_domains = ["registry.uga.kharkov.ua"]
    start_urls = ["http://registry.uga.kharkov.ua/server-response.php?_=1567368281378"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["number_in_order", "order_no", "order_date", "customer", "obj", "address", "changes",
                               "cancellation", "scan_url"],
    }

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        for row in jsonresponse["aaData"]:
            self.logger.debug("parsed row : {}".format(row))
            l = StripJoinItemLoader(item=MbuItem())
            l.add_value("number_in_order", row[0])
            l.add_value("order_no", re.search("№ ?(.*) ?(ві|от)", row[1]).group(1) if row[1] else None)
            l.add_value("order_date", re.search("([0-9]{1,2}\.[0-9]{1,2}\. ?[0-9]{1,4})", row[1]).group(1) if row[1] else None)
            l.add_value("customer", row[2])
            l.add_value("obj", row[3])
            l.add_value("address", row[4])
            l.add_value("changes", row[5])
            l.add_value("cancellation", row[6])
            l.add_value("scan_url", Selector(text=row[7]).css("a::attr(href)").extract_first() if row[7] else None)

            yield l.load_item()
