# -*- coding: utf-8 -*-
import scrapy
from ragoogle.items.kga_gov_ua import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class KyivSpider(scrapy.Spider):
    location_name = "Київ"
    name = "kga_gov_ua"
    allowed_domains = ["kga.gov.ua"]
    start_urls = ["http://kga.gov.ua/table/"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["location_name", "order_no", "order_date", "customer", "obj", "address", "changes",
                               "cancellation", "scan_url"],
    }

    def parse(self, response):
        for row in response.css("table#droptablesTbl4 tbody tr"):
            self.logger.debug("parse row : {}".format(row.get()))
            l = StripJoinItemLoader(item=MbuItem(), selector=row)
            l.add_css("order_no", "td:nth-child(2)::text", re=r"([\d]+)$")
            l.add_css("order_date", "td:nth-child(2)::text", re=r"^[\d.]*")
            l.add_css("customer", "td:nth-child(3)::text")
            l.add_css("obj", "td:nth-child(4)::text")
            l.add_css("address", "td:nth-child(5)::text")
            l.add_css("changes", "td:nth-child(6)::text")
            l.add_css("cancellation", "td:nth-child(7)::text")

            url = row.css("td:nth-child(8) a::attr(href)").extract_first()
            if url:
                l.add_value("scan_url", response.urljoin(url))

            yield l.load_item()
