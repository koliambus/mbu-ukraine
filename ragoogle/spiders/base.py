# -*- coding: utf-8 -*-
import re
import logging
import scrapy
from random import choice
from scrapy.conf import settings


class ProxyMeshSpiderMixin(object):
    proxies = settings["PROXYMESH_PROXIES"]

    def get_random_proxy(self):
        return choice(self.proxies)

