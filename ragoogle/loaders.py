# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst


class StripJoinItemLoader(ItemLoader):
    default_output_processor = Join()
    default_input_processor = MapCompose(str.strip)


class TakeFirstItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(str.strip)
