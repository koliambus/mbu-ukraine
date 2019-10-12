# -*- coding: utf-8 -*-
import scrapy

from ragoogle.items.zp_gov_ua import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class ZaporizhiaSpider(scrapy.Spider):
    name = "zp_gov_ua"
    allowed_domains = ["zp.gov.ua"]
    start_urls = ["https://zp.gov.ua/uk/page/reestr-mbutao"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["number_in_order", "order_no", "order_date", "customer", "obj", "address", "changes",
                               "cancellation", "scan_url", "address_assign_date", "address_assign_no",
                               "address_assign_url"],
    }

    def parse(self, response):
        loaded_order_numbers = []
        for index, row in enumerate(response.css("table tbody tr")):
            # first and second are headers, skip
            if index == 0 or index == 1:
                self.logger.debug("skipped index = {}, row : {}".format(index, row))
                continue

            self.logger.debug("parse index = {}, row : {}".format(index, row))
            orders_in_row = len(row.css("td:nth-child(3) p").getall())

            if orders_in_row == 0:
                orders_in_row = len(row.css("td:nth-child(3) span"))

            # each row is sub divided for main order and it's changes
            for order_in_row in range(orders_in_row):
                l = StripJoinItemLoader(item=MbuItem(), selector=row)
                l.add_value("number_in_order",
                            self.get_first_existed(row,
                                                   "td:nth-child(1) p span::text",
                                                   "td:nth-child(1) span::text"))

                l.add_value("order_no",
                            self.get_first_existed(row,
                                                   "td:nth-child(3) p:nth-child(" + str(order_in_row + 1) + ") span::text",
                                                   "td:nth-child(3) p:nth-child(1) span::text",
                                                   "td:nth-child(3) span:nth-child(" + str(order_in_row + 1) + ")::text",
                                                   "td:nth-child(3) span:nth-child(1)::text"))

                l.add_value("order_date",
                            self.get_first_existed(row,
                                                   "td:nth-child(2) p:nth-child(" + str(order_in_row + 1) + ") span::text",
                                                   "td:nth-child(2) p:nth-child(1) span::text",
                                                   "td:nth-child(2) span:nth-child(" + str(order_in_row + 1) + ")::text",
                                                   "td:nth-child(2) span:nth-child(1) span::text"))

                l.add_value("customer",
                            self.get_first_existed(row,
                                                   "td:nth-child(4) p:nth-child(" + str(order_in_row + 1) + ") span::text",
                                                   "td:nth-child(4) p:nth-child(1) span::text",
                                                   "td:nth-child(4) span:nth-child(" + str(order_in_row + 1) + ")::text",
                                                   "td:nth-child(4) span:nth-child(1)::text"))

                l.add_value("obj",
                            self.get_first_existed(row,
                                                   "td:nth-child(5) p:nth-child(" + str(order_in_row + 1) + ") span::text",
                                                   "td:nth-child(5) p:nth-child(1) span::text",
                                                   "td:nth-child(5) span:nth-child(" + str(order_in_row + 1) + ")::text",
                                                   "td:nth-child(5) span:nth-child(1)::text"))

                l.add_value("address",
                            self.get_first_existed(row,
                                                   "td:nth-child(6) p:nth-child(" + str(order_in_row + 1) + ") span::text",
                                                   "td:nth-child(6) p:nth-child(1) span::text",
                                                   "td:nth-child(6) span:nth-child(" + str(order_in_row + 1) + ")::text",
                                                   "td:nth-child(6) span:nth-child(1)::text"))

                l.add_value("changes",
                            self.get_first_existed(row,
                                                   "td:nth-child(7) p:nth-child(" + str(order_in_row + 1) + ") span::text",
                                                   "td:nth-child(7) p:nth-child(1) span::text",
                                                   "td:nth-child(7) span:nth-child(" + str(order_in_row + 1) + ")::text",
                                                   "td:nth-child(7) span:nth-child(1)::text"))
                l.add_value("cancellation",
                            self.get_first_existed(row,
                                                   "td:nth-child(8) p:nth-child(" + str(order_in_row + 1) + ") span::text",
                                                   "td:nth-child(8) p:nth-child(1) span::text",
                                                   "td:nth-child(8) span:nth-child(" + str(order_in_row + 1) + ")::text",
                                                   "td:nth-child(8) span:nth-child(1)::text"))

                url = self.get_first_existed(row,
                                             "td:nth-child(9) p:nth-child(" + str(order_in_row + 1) + ") span a::attr(href)",
                                             "td:nth-child(9) p:nth-child(1) span a::attr(href)",
                                             "td:nth-child(9) a:nth-child(" + str(order_in_row + 1) + ")::attr(href)",
                                             "td:nth-child(9) a:nth-child(1)::attr(href)")

                l.add_value("scan_url", response.urljoin(url))

                address_assign_url = self.get_first_existed(row, "td:nth-child(10) a::attr(href)")

                if address_assign_url:
                    l.add_value("address_assign_url", response.urljoin(address_assign_url))
                    l.add_css("address_assign_no", "td:nth-child(10) a span::text", re=r"№(.*) ?від")
                    l.add_css("address_assign_date", "td:nth-child(10) a span::text", re=r"від ?(.*)$")

                loaded_order_numbers.append(int(l.get_collected_values("number_in_order")[0]))

                yield l.load_item()

        # check if all consecutive orders where loaded
        missed_order_numbers = {*range(1, max(loaded_order_numbers))}.difference(loaded_order_numbers)

        if missed_order_numbers:
            self.logger.warning("Missed order numbers: %s", missed_order_numbers)
        else:
            self.logger.info("All order numbers processed")

    @staticmethod
    def get_first_existed(row, *selectors):
        for selector in selectors:
            value = row.css(selector).get()
            if value is None:
                continue
            else:
                return value
