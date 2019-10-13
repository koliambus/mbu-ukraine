# -*- coding: utf-8 -*-
import re

import scrapy
from ragoogle.items.sumy import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class SumySpider(scrapy.Spider):
    location_name = "Суми"
    name = "sumy"
    allowed_domains = ["smr.gov.ua"]
    start_urls = ["https://www.smr.gov.ua/uk/dokumenti/mistobudivna-dokumentatsiya/mistobudivni-umovy-ta-obmezhennia.html"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["location_name", "order_no", "order_date", "customer", "obj", "address", "changes_text",
                               "changes_date", "changes_order_no", "cancellation", "cancellation_url", "scan_url"],
    }

    def parse(self, response):
        for i, row in enumerate(response.css("table tbody tr")):
            # skip styled as header
            if row.css("td:nth-child(1) p strong").get():
                self.logger.debug("skipped row : {}".format(row))
                continue

            self.logger.debug("parsed row : {}".format(row))
            l = StripJoinItemLoader(item=MbuItem(), selector=row)
            l.add_css("order_no", "td:nth-child(1) a.add-google-doc::text", re=r"№\s?(.+)$")
            l.add_css("order_date", "td:nth-child(1) a.add-google-doc::text", re=r"([\d\.]*) №")
            l.add_css("customer", "td:nth-child(2)::text")
            l.add_css("obj", "td:nth-child(3)::text")
            l.add_css("address", "td:nth-child(4)::text")
            l.add_css("changes", "td:nth-child(5)::text")
            l.add_css("cancellation", "td:nth-child(6)::text")

            cancellation_url = row.css("td:nth-child(6) a.add-google-doc::attr(href)").getall()
            if len(cancellation_url):
                l.add_value("cancellation_url", [response.urljoin(url) for url in cancellation_url])

            url = row.css("td:nth-child(1) a.add-google-doc::attr(href)").extract_first()
            if url:
                l.add_value("scan_url", response.urljoin(url))

            yield l.load_item()
