# -*- coding: utf-8 -*-
import scrapy
import re
from ragoogle.items.geo_lutskarada_gov_ua import MbuItem
from ragoogle.loaders import StripJoinItemLoader
from .base import ProxyMeshSpiderMixin


class LutskSpider(scrapy.Spider, ProxyMeshSpiderMixin):
    location_name = "Луцьк"
    name = "geo_lutskarada_gov_ua"
    allowed_domains = ["geo.lutskrada.gov.ua"]
    start_urls = ["http://geo.lutskrada.gov.ua/ua/register_mc/page=1"]
    custom_settings = {
        # specifies exported fields and order
        "FEED_EXPORT_FIELDS": [
            "location_name",
            "order_no",
            "order_date",
            "customer",
            "obj",
            "address",
            "changes",
            "cadastre_number",
            "document_status",
            "scan_url",
            "map_url",
        ]
    }

    def parse(self, response):
        for row in response.css("table.table.table-striped.small tbody tr"):
            self.logger.debug("parse row : {}".format(row.get()))
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

        # if 'Next' page label present continue crawling
        if response.css("ul.pagination li a[aria-label=Next]").get():
            yield scrapy.Request(
                self.get_next_page(response),
                callback=self.parse,
                meta={"proxy": self.get_random_proxy()},
            )

    def get_next_page(self, response):
        page_selector = "/page=([0-9].*)"
        current_page = 1
        base_url = response.url
        request_url = response.url

        # first page without "/page="
        selected_pagination = re.search(page_selector, request_url)
        if selected_pagination:
            current_page = selected_pagination.group(1)
            base_url = request_url[: selected_pagination.span()[0]]

        next_page = base_url + "/page=" + str(int(current_page) + 1)
        self.logger.info(
            "Calculated next page : [{}] from current : [{}]".format(
                next_page, response.url
            )
        )
        return response.urljoin(next_page)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                    url,
                    callback=self.parse,
                    meta={"proxy": self.get_random_proxy()},
                )