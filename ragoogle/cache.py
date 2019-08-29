from scrapy import Selector
from scrapy.http import HtmlResponse
from scrapy.utils.gz import gunzip
from scrapy.extensions.httpcache import DummyPolicy


class MetaDummyPolicy(DummyPolicy):
    def is_cached_response_fresh(self, response, request):
        return not request.meta.get("invalidate_cache", False)


class DabiGovUaMetaDummyPolicy(MetaDummyPolicy):
    def is_cached_response_fresh(self, response, request):
        if super().is_cached_response_fresh(
                response, request):

            body = gunzip(response.body)

            h = HtmlResponse(url=response.url, body=body)
            s = Selector(h)
            return len(s.xpath("//table[contains(@class, 'listTable')]"
                               "//tr[not(@class)][not(@id)]")) == 50
        else:
            return False


class OrJusticeCzMetaDummyPolicy(MetaDummyPolicy):
    def is_cached_response_fresh(self, response, request):
        if super().is_cached_response_fresh(
                response, request):

            try:
                body = gunzip(response.body)
            except OSError:
                body = response.body

            h = HtmlResponse(url=response.url, body=body)
            s = Selector(h)
            company_name = s.css("h2 > span:first-child::text").extract()
            return company_name and company_name[0].strip()
        else:
            return False
