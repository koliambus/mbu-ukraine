# -*- coding: utf-8 -*-
import scrapy
from ragoogle.items.poltava import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class PoltavaSpider(scrapy.Spider):
    name = "poltava"
    allowed_domains = ["mistobud.pythonanywhere.com"]
    start_urls = ["http://mistobud.pythonanywhere.com/list"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["order_no", "order_date", "customer", "obj", "address", "changes", "cancellation",
                               "scan_url"],
    }

    def parse(self, response):
        for i, row in enumerate(response.css("table tr")):
            # skip first as header
            if i == 0: continue
            l = StripJoinItemLoader(item=MbuItem(), selector=row)
            l.add_css("order_no", "td:nth-child(1)::text", re=r" (.*)$")
            l.add_css("order_date", "td:nth-child(1)::text", re=r"^[\d-]*")
            l.add_css("customer", "td:nth-child(2)::text")
            l.add_css("obj", "td:nth-child(3)::text")
            l.add_css("address", "td:nth-child(4)::text")
            l.add_css("changes", "td:nth-child(5)::text")
            l.add_css("cancellation", "td:nth-child(6)::text")
            l.add_css("scan_url", "td:nth-child(7) a::attr(href)")
            yield l.load_item()
