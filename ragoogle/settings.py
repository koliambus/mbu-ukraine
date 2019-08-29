import os
import os.path

try:
    # Python 3.x
    from urllib.parse import quote_plus
except ImportError:
    # Python 2.x
    from urllib import quote_plus


def get_env_str(k, default):
    return os.environ.get(k, default)


def get_env_str_list(k, default=""):
    if os.environ.get(k) is not None:
        return os.environ.get(k).strip().split(" ")
    return default


def get_env_bool(k, default):
    return str(get_env_str(k, default)).lower() in ["1", "y", "yes", "true"]


def get_env_int(k, default):
    return int(get_env_str(k, default))


BOT_NAME = "ragoogle"

SPIDER_MODULES = ["ragoogle.spiders"]
NEWSPIDER_MODULE = "ragoogle.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "ragoogle (+https://ring.org.ua)"
ROBOTSTXT_OBEY = False

PROXYMESH_PROXIES = get_env_str_list(
    "PROXYMESH_PROXIES",
    [
        "http://uk.proxymesh.com:31280",
        "http://us-wa.proxymesh.com:31280",
        "http://jp.proxymesh.com:31280",
        "http://au.proxymesh.com:31280",
        "http://open.proxymesh.com:31280",
    ],
)

# Some sane defaults
CONCURRENT_REQUESTS = 32
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 3
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 15
RETRY_ENABLED = True
RETRY_TIMES = 15
RETRY_HTTP_CODES = [403, 404, 429, 502, 408]
DUPEFILTER_DEBUG = False


# All set but disabled
HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = [403, 404, 429, 502, 408, 503, 301, 302, 500]

MONGODB_HOST = quote_plus(get_env_str("MONGODB_HOST", "cluster0-shard-00-00-cl2ou.mongodb.net"))
MONGODB_PORT = get_env_int("MONGODB_PORT", 27017)
MONGODB_USERNAME = quote_plus(get_env_str("MONGODB_USERNAME", "scrapy"))
MONGODB_PASSWORD = quote_plus(get_env_str("MONGODB_PASSWORD", "scrapy"))
MONGODB_AUTH_DB = get_env_str("MONGODB_AUTH_DB", "admin")
MONGODB_DB = get_env_str("MONGODB_DB", "test")
MONGODB_URI = get_env_str("MONGODB_URI", "mongodb+srv://scrapy:scrapy@cluster0-cl2ou.mongodb.net/test?retryWrites=true&w=majority")
MONGODB_CONNECTION_POOL_KWARGS = {}

HTTPCACHE_STORAGE = "scrapy_httpcache.extensions.httpcache_storage.MongoDBCacheStorage"
HTTPCACHE_MONGODB_HOST = MONGODB_HOST
HTTPCACHE_MONGODB_PORT = MONGODB_PORT
HTTPCACHE_MONGODB_USERNAME = MONGODB_USERNAME
HTTPCACHE_MONGODB_PASSWORD = MONGODB_PASSWORD
HTTPCACHE_MONGODB_CONNECTION_POOL_KWARGS = MONGODB_CONNECTION_POOL_KWARGS
HTTPCACHE_MONGODB_AUTH_DB = MONGODB_AUTH_DB
HTTPCACHE_MONGODB_DB = MONGODB_DB
HTTPCACHE_MONGODB_URI = MONGODB_URI
HTTPCACHE_MONGODB_COLL = get_env_str("HTTPCACHE_MONGODB_COLL", "cache")


ITEM_PIPELINES = {"ragoogle.pipelines.MongoDBPipeline": 9000}

EXTENSIONS = {
    "ragoogle.extensions.save_stats.SpiderSaveStatsOnFinish": 600,
}

DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware": None,
    "scrapy_httpcache.downloadermiddlewares.httpcache.AsyncHttpCacheMiddleware": 900,
}

PROMETHEUS_ENABLED = get_env_bool("PROMETHEUS_ENABLED", False)
PROMETHEUS_HOST = get_env_str("PROMETHEUS_HOST", "0.0.0.0")
PROMETHEUS_PORT = [get_env_int("PROMETHEUS_PORT", 9410)]

SCRAPY_JOB = get_env_str("SCRAPY_JOB", None)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRAPY_STATS_DIR = get_env_str("SCRAPY_STATS_DIR", os.path.join(BASE_DIR, "stats"))
