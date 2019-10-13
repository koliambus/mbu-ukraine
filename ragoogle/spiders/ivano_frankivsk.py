# -*- coding: utf-8 -*-
import scrapy
from ragoogle.items.ivano_frankivsk import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class IvanoFrankivskSpider(scrapy.Spider):
    location_name = "Івано-Франківськ"
    name = "ivano_frankivsk"
    allowed_domains = ["dma.if.ua"]
    start_urls = ["http://dma.if.ua/department/registries/mbuio/page/1/"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["location_name",  "order_no", "order_date", "prescript_no", "prescript_date", "customer",
                               "obj", "address", "changes", "cancellation", "scan_url"],
    }

    def parse(self, response):
        for row in response.css("table.table-registry tbody tr"):
            self.logger.debug("parse row : {}".format(row.get()))
            l = StripJoinItemLoader(item=MbuItem(), selector=row)
            l.add_css("order_no", "td:nth-child(1) strong::text")
            l.add_css("order_date", "td:nth-child(1)::text")
            l.add_css("prescript_no", "td:nth-child(2) strong::text")
            l.add_css("prescript_date", "td:nth-child(2)::text")
            l.add_css("customer", "td:nth-child(5)::text")
            l.add_css("obj", "td:nth-child(3)::text")
            l.add_css("address", "td:nth-child(4)::text")
            l.add_css("changes", "td:nth-child(6)::text")
            l.add_css("cancellation", "td:nth-child(7)::text")

            url = row.css("td:nth-child(8) a::attr(href)").extract_first()
            if url:
                l.add_value("scan_url", response.urljoin(url))

            yield l.load_item()

        next_page = response.css('a.next.page-numbers::attr(href)').extract_first()
        if next_page:
            self.logger.debug("follow next page : {}".format(next_page))
            yield response.follow(next_page)
