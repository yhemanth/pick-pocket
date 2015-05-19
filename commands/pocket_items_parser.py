import json
import os.path
from pocket_tags_types import tag_types


class PocketItemsParser:

    def __init__(self, pocket_items_file):
        self.__time_stamp = os.path.basename(pocket_items_file).replace('-pocket-items', '')
        self.items = [json.loads(line) for line in open(pocket_items_file, 'r').readlines()]
        self.tagged_items = filter(lambda item: item.has_key('tags'), self.items)

    def extract_tags(self):
        tags = list()
        map(lambda item: tags.extend(item['tags']), self.tagged_items)
        tag_groups = dict()
        for tag in tags:
            tag_type = tag_types.get(tag) if tag_types.has_key(tag) else "unknown"
            tags_for_type = tag_groups[tag_type] if tag_groups.has_key(tag_type) else list()
            tags_for_type.append(tag)
            tag_groups[tag_type] = tags_for_type
        return tag_groups

    def num_items(self):
        return len(self.items)

    def num_tagged_items(self):
        return len(self.tagged_items)

    def time_stamp(self):
        return self.__time_stamp
