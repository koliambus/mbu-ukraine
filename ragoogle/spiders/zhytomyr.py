# -*- coding: utf-8 -*-
from collections import defaultdict

import scrapy
import xlrd
import re

from ragoogle.items.zhytomyr import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class ZhytomyrSpider(scrapy.spiders.CSVFeedSpider):
    location_name = "Житомир"
    name = "zhytomyr"
    allowed_domains = ["zt-rada.gov.ua"]
    start_urls = [
        "http://zt-rada.gov.ua/?3398[0]=6281"
    ]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["location_name", "order_no", "order_date", "customer", "obj", "address", "changes",
                               "cancellation", "scan_url"],
    }
    item_loaders = defaultdict(lambda: StripJoinItemLoader(item=MbuItem()))

    def parse_xls_and_flush(self, response):
        sheet = xlrd.open_workbook(file_contents=response.body).sheet_by_index(0)
        for index in range(1, sheet.nrows):
            row = sheet.row(index)

            # if row is not empty
            if row[1].value:
                order_no = row[0].value.replace('№', '').strip()
                l = self.get_item(order_no)

                if not l.get_output_value('order_no'):
                    l.add_value("order_no", order_no)

                l.add_value("order_date", row[1].value)
                l.add_value("customer", row[6].value)
                l.add_value("obj", row[2].value)
                l.add_value("address", row[3].value)
                l.add_value("changes", row[7].value)
                l.add_value("cancellation", row[8].value)
            else:
                self.logger.debug("skipped index : {}, row : {}".format(index, row))

        for item in self.item_loaders.values():
            yield item.load_item()

        # clear in case of several xls files found
        self.item_loaders.clear()

    def parse(self, response):
        for row in response.css(".docrowcontainer"):
            document_url = row.css("div:nth-child(2) a.docdownload::attr(href)").extract_first()

            if document_url.endswith('.xls'):
                self.logger.info("xls document found : {}".format(document_url))
                yield response.follow(document_url, callback=self.parse_xls_and_flush, priority=10)  # big priority to run last
            else:
                continue
                # self.logger.debug("parse site row : {}".format(row.get()))
                # order_no = "".join(row.css("div:nth-child(1)::text").re(r"№ ?(.*)")).strip()
                # l = self.get_item(order_no)
                # l.selector = row

                # l.add_value("order_no", order_no)
                # l.add_xpath("order_date", "./@data-year")

                # l.add_value("scan_url", response.urljoin(document_url))

        next_page_link = response.xpath('//*[@id="tp6"]//ul/li[@class="active"]/following-sibling::li[1]/a/@href').get()
        if next_page_link:
            self.logger.debug("next page link : {}".format(next_page_link))
            yield response.follow(next_page_link, callback=self.parse)

    def get_item(self, order_no):
        # tries to find similar order number with different separating signs
        splitter = '[\.\s/\-\|]+'
        order_id_list = re.split(splitter, order_no.strip())
        filtered_order = list(filter(
            lambda ord: order_id_list == re.split(splitter, ord.strip()),
            self.item_loaders.keys()
        ))

        if len(filtered_order):
            self.logger.debug('similar to order_no : {} found in loaders : {}'.format(order_no, filtered_order))

        return self.item_loaders[filtered_order[0] if len(filtered_order) else order_no]
