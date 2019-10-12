# -*- coding: utf-8 -*-
import scrapy
from ragoogle.items.chernihiv import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class ChernihivSpider(scrapy.Spider):
    name = "chernihiv"
    allowed_domains = ["old.chernigiv-rada.gov.ua"]
    start_urls = ["http://old.chernigiv-rada.gov.ua/project/gorstroydoc/13287",
                  "http://old.chernigiv-rada.gov.ua/project/gorstroydoc/20089"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["decree", "order_no", "order_date", "customer", "obj", "address", "changes",
                               "cancellation", "cancellation_url", "scan_url"],
    }

    def parse(self, response):
        for index, row in enumerate(response.css("table>tbody>tr")):

            # skip headers and rows with empty lines
            if index < 5 and not "".join(row.css("td::text, td span::text").getall()).strip():
                self.logger.debug("skipped index : {}, row : {}".format(index, row.get()))
                continue

            self.logger.debug("parse index : {}, row : {}".format(index, row.get()))

            l = StripJoinItemLoader(item=MbuItem(), selector=row)
            l.add_css("decree", "td:nth-child(1)::text")
            l.add_css("order_no", "td:nth-child(2)::text, td:nth-child(2) span::text", re=r"^\s?(.*)від")
            l.add_css("order_date", "td:nth-child(2)::text, td:nth-child(2) span::text", re=r"від\s?([\d\.]*)\s*$")
            l.add_css("customer", "td:nth-child(3)::text, td:nth-child(3) span::text")
            l.add_css("obj", "td:nth-child(4)::text, td:nth-child(4) span::text")
            l.add_css("address", "td:nth-child(5)::text, td:nth-child(5) span::text")
            l.add_css("changes", "td:nth-child(6)::text, td:nth-child(6) span::text")
            l.add_css("cancellation", "td:nth-child(7)::text, td:nth-child(7) a::text, td:nth-child(7) span::text")

            cancellation_url = row.css("td:nth-child(7) a::attr(href)").extract_first()
            if cancellation_url:
                l.add_value("cancellation_url", response.urljoin(cancellation_url))

            scan_url = row.css("td:nth-child(8) a::attr(href)").extract_first()
            if scan_url:
                l.add_value("scan_url", response.urljoin(scan_url))

            yield l.load_item()
