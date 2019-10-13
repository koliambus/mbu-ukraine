# -*- coding: utf-8 -*-
import scrapy
import re
from ragoogle.items.mkrada_gov_ua import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class MykolaivSpider(scrapy.Spider):
    location_name = "Миколаїв"
    name = "mkrada_gov_ua"
    allowed_domains = ["mkrada.gov.ua"]
    start_urls = ["https://mkrada.gov.ua/content/reestr-mistobudivnih-umov-ta-obmezhen.html"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["location_name", "number_in_order", "order_no", "order_date", "customer", "obj",
                               "address", "changes", "cancellation", "scan_url"],
    }

    def parse(self, response):
        for row in response.css("article table tbody tr:not([align=\"center\"])"):
            l = StripJoinItemLoader(item=MbuItem(), selector=row)

            # skip empty lines
            date_order = ''.join(row.css("td:nth-child(2) p span::text, td:nth-child(2) span::text, td:nth-child(2)::text").getall())
            if not date_order or not date_order.strip():
                self.logger.debug("skipped row : {}".format(row.get()))
                continue

            self.logger.debug("parse row : {}".format(row.get()))
            # number_in_order is unique only per year
            l.add_css("number_in_order", "td:nth-child(1) p span::text, td:nth-child(1) span::text, td:nth-child(1)::text")
            l.add_value("order_no", re.search('^\\s?№? ?(.*)\\s?(в?ід|dsl)', date_order).group(1))
            l.add_css("order_date", "td:nth-child(2) p span::text, td:nth-child(2) span::text, td:nth-child(2)::text",
                      re=r"(\d{1,2}[\. /]?\d{1,2}[\. /]?\d{2,4})\s*$")
            l.add_css("customer", "td:nth-child(3) span::text, td:nth-child(3)::text")
            l.add_css("obj", "td:nth-child(4) span::text, td:nth-child(4)::text")
            l.add_css("address", "td:nth-child(5) span::text, td:nth-child(5) p::text, td:nth-child(5)::text")
            l.add_css("changes", "td:nth-child(6) span::text, td:nth-child(6)::text")
            l.add_css("cancellation", "td:nth-child(7) span::text, td:nth-child(7)::text")

            url = row.css("td:nth-child(8) a::attr(href)").extract_first()
            if url:
                l.add_value("scan_url", response.urljoin(url))

            yield l.load_item()
