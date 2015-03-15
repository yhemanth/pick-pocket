import json
import collections


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


class ReportCommand(object):
    def execute(self, options):
        report = Report()
        items = [json.loads(line) for line in open(options.pocket_items_file, 'r').readlines()]
        report.total_items = len(items)
        tagged_items = filter(lambda item: item.has_key('tags'), items)
        report.tagged_items = len(tagged_items)
        tags = list()
        map(lambda item: tags.extend(item['tags']), tagged_items)
        report.count_by_tags = collections.Counter(tags)
        report.my_print()



