import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem


class MongoDBPipeline(object):
    def __init__(self):
        if settings["MONGODB_USERNAME"]:
            uri = "mongodb://{}:{}@{}:{}".format(
                settings["MONGODB_USERNAME"],
                settings["MONGODB_PASSWORD"],
                settings["MONGODB_HOST"],
                settings["MONGODB_PORT"]
            )
        else:
            uri = "mongodb://{}:{}".format(
                settings["MONGODB_HOST"],
                settings["MONGODB_PORT"]
            )

        self.connection = pymongo.MongoClient(
            uri,
            authSource=settings["MONGODB_AUTH_DB"],
            **settings["MONGODB_CONNECTION_POOL_KWARGS"]
        )
        self.db = self.connection[settings["MONGODB_DB"]]

    def process_item(self, item, spider):
        collection = self.db[spider.name]

        collection.update_one({"_id": item.get_doc_hash()}, item.get_update_clause(), upsert=True)

        return item


class AddLocationNamePipeline(object):
    def process_item(self, item, spider):
        if spider.location_name and item.fields.get('location_name') is not None:
            item['location_name'] = spider.location_name

        return item
