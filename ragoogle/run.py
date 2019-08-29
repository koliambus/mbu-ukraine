import scrapy
from scrapy.crawler import CrawlerProcess

from ragoogle.spiders.geo_lutskarada_gov_ua import LutskSpider
from ragoogle.spiders.mbk_city_adm_lviv_ua import LvivSpider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(LutskSpider)
process.start()