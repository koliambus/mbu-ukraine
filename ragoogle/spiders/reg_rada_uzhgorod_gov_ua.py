# -*- coding: utf-8 -*-
import scrapy
from ragoogle.items.reg_rada_uzhgorod_gov_ua import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class UzhorodSpider(scrapy.Spider):
    location_name = "Ужгород"
    name = "reg_rada_uzhgorod_gov_ua"
    allowed_domains = ["reg.rada-uzhgorod.gov.ua/"]
    start_urls = ["http://reg.rada-uzhgorod.gov.ua/"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["location_name", "order_no", "order_date", "customer", "obj", "address", "changes",
                               "cancellation", "scan_url"],
    }

    def parse(self, response):
        for row in response.css("div.table-content-container div#orders div.one_order"):
            self.logger.debug("parsed row : {}".format(row.get()))
            l = StripJoinItemLoader(item=MbuItem(), selector=row)
            l.add_css("order_date", "li.order_date::text")
            l.add_css("order_no", "li.order_number::text")
            l.add_css("customer", "li.cust::text")
            l.add_css("obj", "li.order_name::text")
            l.add_css("address", "li.addr::text")
            l.add_css("changes", "li.changes_info::text")
            l.add_css("cancellation", "li.reason_canc::text")

            url = row.css("li.download a::attr(href)").extract_first()
            if url:
                l.add_value("scan_url", response.urljoin(url))

            yield l.load_item()
