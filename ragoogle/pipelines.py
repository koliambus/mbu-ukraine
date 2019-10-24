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
                settings["MONGODB_PORT"],
            )
        else:
            uri = "mongodb://{}:{}".format(
                settings["MONGODB_HOST"], settings["MONGODB_PORT"]
            )

        self.connection = pymongo.MongoClient(
            uri,
            authSource=settings["MONGODB_AUTH_DB"],
            **settings["MONGODB_CONNECTION_POOL_KWARGS"]
        )
        self.db = self.connection[settings["MONGODB_DB"]]

    def process_item(self, item, spider):
        collection_name = getattr(spider, "mongo_collection", spider.name)
        collection = self.db[collection_name]

        collection.update_one(
            {"_id": item.get_doc_hash()}, item.get_update_clause(), upsert=True
        )

        return item


class AddLocationNamePipeline(object):
    def process_item(self, item, spider):
        if (
            getattr(spider, "location_name", None) is not None
            and item.fields.get("location_name") is not None
            and len(item.values())
        ):
            item["location_name"] = spider.location_name

        return item
