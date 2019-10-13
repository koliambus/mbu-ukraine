# -*- coding: utf-8 -*-
import scrapy
import re

from ragoogle.items.ternopil import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class TernopilSpider(scrapy.Spider):
    location_name = "Тернопіль"
    name = "ternopil"
    allowed_domains = ["tmrada.gov.ua"]
    start_urls = ["https://tmrada.gov.ua/normative-documents/mistobudivni-umovi-y-obmegennya-pasporti-privyazki/4361.html"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["location_name", "number_in_order", "order_no", "order_date", "customer", "obj",
                               "address", "changes", "cancellation", "scan_url"],
    }

    def parse(self, response):
        # only first table with data
        for index, row in enumerate(response.css("div.post-body>table:first-of-type>tbody>tr")):

            # first two are headers, skip
            if index < 2:
                self.logger.debug("skipped row : {}".format(row))
                continue

            self.logger.debug("parse row : {}".format(row))
            l = StripJoinItemLoader(item=MbuItem(), selector=row)
            # because of errors in html, get td from current root only
            l.add_xpath("number_in_order", "./td[position()=1]/span/text()|./td[position()=1]/p/span/text()", re=r"(\d+)\s?")
            l.add_css("order_no", "td:nth-child(2) p span::text, td:nth-child(2) span::text", re=r"^\s*№ ?(.*)\s?від")
            l.add_css("order_date", "td:nth-child(2) p span::text, td:nth-child(2) span::text", re=r"(\d{1,2}[\. /]?\d{1,2}[\. /]?\d{2,4})[\sр\.]*$")
            l.add_css("customer", "td:nth-child(3) p span::text, td:nth-child(3) span::text")
            l.add_css("obj", "td:nth-child(4) p span::text, td:nth-child(4) span::text")
            l.add_css("address", "td:nth-child(5) p span::text, td:nth-child(5) span::text")
            l.add_css("changes", "td:nth-child(6) p span::text, td:nth-child(6) span::text")
            l.add_css("cancellation", "td:nth-child(7) p span::text, td:nth-child(7) span::text")

            url = row.css("td:nth-child(8) p span a::attr(href), td:nth-child(8) span a::attr(href), td:nth-child(8) a::attr(href)").extract_first()
            if url:
                l.add_value("scan_url", response.urljoin(url))

            yield l.load_item()
