# -*- coding: utf-8 -*-
import scrapy
from ragoogle.items.khmelnytskyi import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class KhmelnytskyiSpider(scrapy.Spider):
    location_name = "Хмельницький"
    name = "khmelnytskyi"
    allowed_domains = ["mycity.khm.gov.ua"]
    start_urls = ["https://mycity.khm.gov.ua/OpenData/MtoRegister"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["location_name",  "order_no", "order_date", "customer", "obj", "obj_purpose",
                               "address_street", "address_street_number", "cancellation", "scan_url"],
    }

    def parse(self, response):
        for row in response.css("table#tabledataMto tbody tr"):
            self.logger.debug("parse row : {}".format(row.get()))
            l = StripJoinItemLoader(item=MbuItem(), selector=row)
            l.add_css("order_no", "td:nth-child(1)::text")
            l.add_css("order_date", "td:nth-child(4)::text")
            l.add_css("customer", "td:nth-child(5)::text")
            l.add_css("obj", "td:nth-child(6)::text")
            l.add_css("obj_purpose", "td:nth-child(7)::text")
            l.add_css("address_street", "td:nth-child(2)::text")
            l.add_css("address_street_number", "td:nth-child(3)::text")
            l.add_css("address", "td:nth-child(2)::text")
            l.add_css("address", "td:nth-child(3)::text")
            l.add_css("cancellation", "td:nth-child(8)::text")

            url = row.css("td:nth-child(9) a::attr(href)").extract_first()
            if url:
                l.add_value("scan_url", response.urljoin(url))

            yield l.load_item()
