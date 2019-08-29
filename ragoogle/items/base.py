import scrapy
import json
from copy import copy
from hashlib import sha1
from collections import OrderedDict
import jmespath


class HashedItem(scrapy.Item):
    def __init__(self, *args, **kwargs):
        self._pathes = {}

        for k in self.get_dedup_fields():
            self._pathes[k] = jmespath.compile(k)

        return super().__init__(*args, **kwargs)

    def get_dedup_fields(self):
        raise NotImplementedError

    def get_doc_hash(self):
        doc = dict(self)
        if "_id" in doc:
            return doc["_id"]

        dedup_fields = sorted(self.get_dedup_fields())

        def get_value(pth, expression):
            if not (("." in pth) or ("[" in pth) or ("]" in pth)):
                return doc[pth]

            val = expression.search(doc)

            # Evaluate if we need code below
            if isinstance(val, list):
                if len(val) == 1:
                    return v[0]
                elif len(val) == 0:
                    return None
            return val

        dct = OrderedDict((k, get_value(k, self._pathes[k])) for k in dedup_fields)

        return sha1(json.dumps(dct).encode("utf-8")).hexdigest()

    def get_update_clause(self):
        return {"$set": dict(self)}

class RawHashedItem(HashedItem):
    def __setitem__(self, key, value):
        self._values[key] = value
