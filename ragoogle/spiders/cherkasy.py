# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import FormRequest, Selector

from ragoogle.items.cherkasy import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class CherkasySpider(scrapy.Spider):
    name = "cherkasy"
    allowed_domains = ["rada.ck.ua"]
    start_urls = ["http://rada.ck.ua/reestrmuo/"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["order_no", "order_date", "customer", "obj", "address", "changes", "cancellation",
                               "scan_url"],
    }

    def parse(self, response):
        url = 'http://rada.ck.ua/reestrmuo/site/ajax'
        headers = {
            'Cookie': '; '.join([str(item, 'utf-8') for item in response.headers.getlist('Set-Cookie')]),
            'Origin': 'http://rada.ck.ua',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8,uk;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'http://rada.ck.ua/reestrmuo/',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive'
        }
        search_object = json.loads(response.css('script::text').re('Core.searchQuery = (.*);')[0])
        self.logger.debug("search object = {}".format(search_object))
        for page in range(1, search_object['totalPages'] + 1):
            body_fields = [
                'method=doSearch',
                'searchQuery%5BdateNumber%5D=',
                'searchQuery%5BcategoryID%5D=-1',
                'searchQuery%5Bclient%5D=',
                'searchQuery%5Bname%5D=',
                'searchQuery%5Baddress%5D=',
                'searchQuery%5BdateFrom%5D=',
                'searchQuery%5BdateTo%5D={}'.format(search_object['dateTo']),
                'searchQuery%5BcurrentPage%5D={}'.format(page),
                'searchQuery%5BtotalPages%5D={}'.format(search_object['totalPages']),
                'searchQuery%5BtotalCount%5D={}'.format(search_object['totalCount']),
                'searchQuery%5Bsort%5D%5Bregistry.date%5D=3',
                'searchQuery%5Bsort%5D%5Bcategory.name%5D=0',
                'searchQuery%5Bsort%5D%5Bregistry.client%5D=0',
                'searchQuery%5Bsort%5D%5Bregistry.name%5D=0',
                'searchQuery%5Bsort%5D%5Bstreet.name%5D=0',
                'searchQuery%5Bsort%5D%5Bregistry.created_at%5D=0'
            ]
            yield FormRequest(
                url=url,
                headers=headers,
                body='&'.join(body_fields),
                callback=self.parse_filtered
            )

    def parse_filtered(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        table = Selector(text=jsonresponse['table'])

        for row in table.css("tr"):
            self.logger.debug("parse row : {}".format(row.get()))
            l = StripJoinItemLoader(item=MbuItem(), selector=row)
            l.add_css("order_no", "td:nth-child(1) strong::text")
            l.add_css("order_date", "td:nth-child(1)::text", re=r"([\d\.])+\s*№")
            l.add_css("customer", "td:nth-child(2)::text")
            l.add_css("obj", "td:nth-child(3) small::text")
            l.add_css("address", "td:nth-child(4)::text")

            changes_url = row.xpath("./td[position()=5]//a[.//span[contains(@class, 'glyphicon glyphicon-edit')]]/@href").extract_first()
            if changes_url:
                l.add_value("changes", response.urljoin(changes_url))

            cancellation_url = row.xpath("./td[position()=5]//a[.//span[contains(@class, 'glyphicon glyphicon-ban-circle')]]/@href").extract_first()
            if cancellation_url:
                l.add_value("cancellation", response.urljoin(cancellation_url))

            scan_url = row.xpath("./td[position()=5]//a[.//span[contains(@class, 'glyphicon glyphicon-info-sign')]]/@href").extract_first()
            if scan_url:
                l.add_value("scan_url", response.urljoin(scan_url))

            yield l.load_item()
