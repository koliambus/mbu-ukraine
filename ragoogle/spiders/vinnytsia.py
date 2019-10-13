# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest

from ragoogle.items.vinnytsia import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class VinnytsiaSpider(scrapy.Spider):
    location_name = "Вінниця"
    name = "vinnytsia"
    allowed_domains = ["vmr.gov.ua"]
    start_urls = ["https://www.vmr.gov.ua/Executives/SitePages/ArchitectureRegistry.aspx"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["location_name", "number_in_order", "order_no", "decree_no", "order_date", "customer",
                               "obj", "address", "changes", "cancellation"],
    }

    def parse(self, response):
        for row in response.css('table.ms-listviewtable tr[class^=building-registry-row]'):
            self.logger.debug("parse row : {}".format(row.get()))
            l = StripJoinItemLoader(item=MbuItem(), selector=row)
            l.add_css("order_no", "td:nth-child(1)::text")
            l.add_css("number_in_order", "td:nth-child(2)::text")
            l.add_css("order_date", "td:nth-child(3)::text")
            l.add_css("decree_no", "td:nth-child(4)::text")
            l.add_css("customer", "td:nth-child(5) div::text")
            l.add_css("obj", "td:nth-child(6) div::text")
            l.add_css("address", "td:nth-child(7) div::text")
            l.add_css("changes", "td:nth-child(8) div::text")
            l.add_css("cancellation", "td:nth-child(9) div::text")

            url = row.css("td:nth-child(10) a::attr(href)").extract_first()
            if url:
                l.add_value("scan_url", response.urljoin(url))

            yield l.load_item()

        # get next page number href next to current inactive with span tag
        nextPageJs = response.xpath('//table[@class="ms-listviewtable"]//tr[@class="building-registry-pager"]//table/tr/td[.//span]/following-sibling::td[1]/a/@href')
        if len(nextPageJs):
            self.logger.debug("next page action found : {}".format(nextPageJs))
            yield FormRequest.from_response(
                response,
                formname="aspnetForm",
                formxpath="//form[@id='aspnetForm']",
                dont_click=True,
                formdata={
                    '__EVENTARGUMENT': nextPageJs.re('\',\'(.*)\'\)'),
                    '__EVENTTARGET': nextPageJs.re('javascript:__doPostBack\(\'(.*)\',')
                },
                dont_filter=True,
                callback=self.parse
            )