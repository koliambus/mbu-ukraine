# -*- coding: utf-8 -*-
import scrapy
from ragoogle.items.mbk_city_adm_lviv_ua import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class LvivSpider(scrapy.Spider):
    name = "mbk_city_adm_lviv_ua"
    allowed_domains = ["mbk.city-adm.lviv.ua"]
    start_urls = ["https://mbk.city-adm.lviv.ua/ua/register_mc"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["order_no", "order_date", "customer", "obj", "address", "changes", "cancellation",
                               "scan_url"],
    }

    def parse(self, response):
        for row in response.css("table.table.table-bordered tbody tr"):
            l = StripJoinItemLoader(item=MbuItem(), selector=row)
            l.add_css("order_date", "td:nth-child(1)::text")
            l.add_css("order_no", "td:nth-child(2)::text")
            l.add_css("customer", "td:nth-child(3)::text")
            l.add_css("obj", "td:nth-child(4)::text")
            l.add_css("address", "td:nth-child(5) p::text")
            l.add_css("changes", "td:nth-child(6)::text")
            l.add_css("cancellation", "td:nth-child(7)::text")

            url = row.css("td:nth-child(8) a::attr(href)").extract_first()
            l.add_value("scan_url", response.urljoin(url))
            yield l.load_item()

