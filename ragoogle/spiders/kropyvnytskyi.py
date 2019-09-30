# -*- coding: utf-8 -*-
import scrapy
from ragoogle.items.kropyvnytskyi import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class KropyvnytskyiSpider(scrapy.Spider):
    name = "kropyvnytskyi"
    allowed_domains = ["kr-rada.gov.ua"]
    start_urls = ["http://www.kr-rada.gov.ua/upravlinnya-arhitekturi/restr-mistobudivnih-umov-ta-obmezhen-dlya-proektuvannya-obkta-budivnitstva/"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["number_in_order", "order_no", "order_date", "customer", "obj", "address", "remarks",
                               "changes", "cancellation", "changes_url", "cancellation_url", "scan_url"],
    }

    def parse(self, response):
        for row in response.xpath('//table/tbody/tr[count(td)=8 and not(./td//span/strong)]'):
            l = StripJoinItemLoader(item=MbuItem(), selector=row)
            l.add_css("number_in_order", "td:nth-child(1) p::text, td:nth-child(1)::text")
            l.add_css("order_no", "td:nth-child(2) p:nth-child(1)::text, td:nth-child(2) p:nth-child(1) span::text", re=r"№\s?(\d+)")
            l.add_css("order_date", "td:nth-child(2) p:nth-child(1)::text, td:nth-child(2) p:nth-child(1) span::text", re=r"(\d{1,2}[\. /]?\d{1,2}[\. /]?\d{2,4})")
            l.add_css("remarks", "td:nth-child(2) p:nth-child(2)::text")
            l.add_css("customer", "td:nth-child(3) p::text")
            l.add_css("obj", "td:nth-child(4) p::text")
            l.add_css("address", "td:nth-child(5) p::text")
            l.add_css("changes", "td:nth-child(6) p::text, td:nth-child(6) a::text")
            l.add_css("cancellation", "td:nth-child(7) p::text, td:nth-child(7) a::text")
            l.add_css("scan_text", "td:nth-child(8) a::text, td:nth-child(8) p::text")

            l.add_css("changes_url", "td:nth-child(6) a::attr(href)")
            l.add_css("cancellation_url", "td:nth-child(7) a::attr(href)")
            l.add_css("scan_url", "td:nth-child(8) a::attr(href)")
            yield l.load_item()
