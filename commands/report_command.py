import json
import collections
import os

from pocket_tags_types import tag_types

class Report():
    def __init__(self):
        self.total_items = 0
        self.tagged_items = 0
        self.count_by_tags = {}

    def print_tag(self, tag):
        print "\t ", tag, ": ", self.count_by_tags[tag]

    def my_print(self):
        print "Total items: ", self.total_items
        print "Tagged items: ", self.tagged_items
        print "Counts by tags:"
        map(lambda tag: self.print_tag(tag), self.count_by_tags.keys())


def handle(pocket_items_file):
    report = Report()
    items = [json.loads(line) for line in open(pocket_items_file, 'r').readlines()]
    report.total_items = len(items)
    tagged_items = filter(lambda item: item.has_key('tags'), items)
    report.tagged_items = len(tagged_items)
    tags = list()
    map(lambda item: tags.extend(item['tags']), tagged_items)
    decorated_tags = [tag_types[tag]+":"+tag for tag in tags if tag_types.has_key(tag)]
    decorated_tags.extend(["unknown:"+tag for tag in tags if not tag_types.has_key(tag)])
    report.count_by_tags = collections.Counter(decorated_tags)
    report.my_print()


class ReportCommand(object):
    def execute(self, options):
        if os.path.isdir(options.pocket_items_path):
            for f in os.listdir(options.pocket_items_path):
                handle(os.path.join(options.pocket_items_path, f))
        else:
            handle(options.pocket_items_path)



