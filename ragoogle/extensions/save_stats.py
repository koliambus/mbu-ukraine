import os
import os.path
import logging
import json
from scrapy import signals
from scrapy.conf import settings
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)


class SpiderSaveStatsOnFinish(object):
    def __init__(self, stats, scrapy_job_id):
        self.stats = stats
        self.scrapy_job_id = scrapy_job_id

    @classmethod
    def from_crawler(cls, crawler):
        scrapy_job_id = crawler.settings.get("SCRAPY_JOB", None)
        if scrapy_job_id is None:
            raise NotConfigured

        # instantiate the extension object
        ext = cls(crawler.stats, scrapy_job_id)

        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)

        # return the extension object
        return ext

    def spider_closed(self, spider):
        out_dir = os.path.join(settings["SCRAPY_STATS_DIR"], spider.name)

        try:
            os.makedirs(out_dir)
        except FileExistsError:
            pass
        except Exception as e:
            logger.error(e)

        with open(os.path.join(out_dir, self.scrapy_job_id + ".json"), "w") as fp:
            json.dump(self.stats.get_stats(), fp, default=str)

