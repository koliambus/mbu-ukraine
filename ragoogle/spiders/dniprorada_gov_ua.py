# -*- coding: utf-8 -*-
import scrapy

from ragoogle.items.dniprorada_gov_ua import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class DniproSpider(scrapy.Spider):
    location_name = "Дніпро"
    name = "dniprorada_gov_ua"
    allowed_domains = ["dniprorada.gov.ua"]
    start_urls = ["https://dniprorada.gov.ua/uk/page/reestr-mistobudivnih-umov-ta-obmezhen"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["location_name", "number_in_order", "order_no", "order_date", "customer", "obj",
                               "address", "changes", "cancellation", "scan_url", "scan_no", "scan_date"],
    }

    def parse(self, response):
        for row in response.css("table tbody tr"):
            # first is header, skip
            if row.css("td:nth-child(1)::text").get() == "№ з/п":
                self.logger.debug("skiped row : {}".format(row.get()))
                continue

            self.logger.debug("parse row : {}".format(row.get()))
            l = StripJoinItemLoader(item=MbuItem(), selector=row)
            l.add_css("number_in_order", "td:nth-child(1)::text")
            l.add_css("order_no", "td:nth-child(2) p::text, td:nth-child(2)::text", re=r"№ ?(.*)\s?$")
            l.add_css("order_date", "td:nth-child(2) p:nth-child(1)::text, td:nth-child(2)::text", re=r"^[\d.]*")
            l.add_css("customer", "td:nth-child(3)::text")
            l.add_css("obj", "td:nth-child(4)::text")
            l.add_css("address", "td:nth-child(5)::text")
            l.add_css("changes", "td:nth-child(6)::text")
            l.add_css("cancellation", "td:nth-child(7)::text")

            url = row.css("td:nth-child(8) a::attr(href)").extract_first()
            if url:
                l.add_value("scan_url", response.urljoin(url))

            l.add_css("scan_no", "td:nth-child(8) a::text", re=r"№(.*) ?від")
            l.add_css("scan_date", "td:nth-child(8) a::text", re=r"від ?(.*)")

            yield l.load_item()
