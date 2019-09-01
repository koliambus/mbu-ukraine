# -*- coding: utf-8 -*-
import scrapy
from ragoogle.items.geo_lutskarada_gov_ua import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class LutskSpider(scrapy.Spider):
    name = "geo_lutskarada_gov_ua"
    allowed_domains = ["geo.lutskrada.gov.ua"]
    start_urls = ["http://geo.lutskrada.gov.ua/ua/register_mc/page=1"]

    def parse(self, response):
        for row in response.css("table.table.table-striped.small tbody tr"):
            l = StripJoinItemLoader(item=MbuItem(), selector=row)
            l.add_css("order_no", "td:nth-child(1)::text")
            l.add_css("order_date", "td:nth-child(2)::text")
            l.add_css("customer", "td:nth-child(3)::text")
            l.add_css("obj", "td:nth-child(4)::text")
            l.add_css("address", "td:nth-child(5)::text")
            l.add_css("cadastre_number", "td:nth-child(6)::text")
            l.add_css("document_status", "td:nth-child(7) span::text")
            l.add_css("changes", "td:nth-child(8)::text")

            document_url = row.css("td:nth-child(9) a::attr(href)").extract_first()
            l.add_value("scan_url", response.urljoin(document_url))

            map_url = row.css("td:nth-child(1) a::attr(href)").extract_first()
            l.add_value("map_url", response.urljoin(map_url))
            yield l.load_item()

        page_selector = "/page="
        current_page = 1
        base_url = response.url
        request_url = response.url

        # first page without "/page="
        if request_url.find(page_selector) != -1:
            current_page = request_url[request_url.find(page_selector) + len(page_selector):]
            base_url = request_url[:request_url.find(page_selector)]

        # if not the last page
        if response.css('ul.pagination li a::attr(aria-label)').getall()[-1] == "Next":
            next_page = base_url + "/page=" + str(int(current_page) + 1)
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
