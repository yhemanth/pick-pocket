import collections
import os

from commands.pocket_items_parser import PocketItemsParser


class Report():
    def __init__(self):
        self.total_items = 0
        self.tagged_items = 0
        self.count_by_tags = {}

    def __print_tag(self, tag):
        print "\t ", tag, ": ", self.count_by_tags[tag]

    def __print_report(self):
        print "Total items: ", self.total_items
        print "Tagged items: ", self.tagged_items
        print "Counts by tags:"
        map(lambda tag: self.__print_tag(tag), self.count_by_tags.keys())

    def handle(self, pocket_items_file):
        parser = PocketItemsParser(pocket_items_file)
        self.total_items = parser.num_items()
        self.tagged_items = parser.num_tagged_items()
        self.count_by_tags = collections.Counter(parser.extract_tags())
        self.__print_report()

class TimeSeries():
    def __init__(self, name):
        self.name = name
        self.values = dict()

    def size(self):
        return len(self.values)

    def incr(self, time_stamp):
        count = self.values.get(time_stamp) if self.values.has_key(time_stamp) else 0
        self.values[time_stamp] = count+1

    def __str__(self):
        time_sorted_values = collections.OrderedDict(sorted(self.values.items()))
        time_series_string = ", ".join([x+": "+str(time_sorted_values[x]) for x in time_sorted_values.keys()])
        return self.name + ": " + "["+time_series_string+"]"


class TimeSeriesReport():
    def __init__(self):
        self.time_series_groups_map = dict()

    def handle(self, pocket_items_file):
        parser = PocketItemsParser(pocket_items_file)
        time_stamp = parser.time_stamp()
        tags = parser.extract_tags()
        for (tag_group, tags) in tags.items():
            time_series_map = self.time_series_groups_map[tag_group] if self.time_series_groups_map.has_key(tag_group) else dict()
            for tag in tags:
                time_series = time_series_map[tag] if time_series_map.has_key(tag) else TimeSeries(tag)
                time_series.incr(time_stamp)
                time_series_map[tag] = time_series
            self.time_series_groups_map[tag_group] = time_series_map

    def print_report(self):
        tag_groups = sorted(self.time_series_groups_map.keys())
        for tag_type in tag_groups:
            print tag_type+":"
            time_series_map = self.time_series_groups_map[tag_type]
            time_series_with_counts = map(lambda ts: (ts.size(), ts), time_series_map.values())
            for (count, time_series) in sorted(time_series_with_counts, reverse=True):
                print "\t"+str(time_series)


class ReportCommand(object):
    def __do_regular_reporting(self, options):
        report = Report()
        if os.path.isdir(options.pocket_items_path):
            for f in os.listdir(options.pocket_items_path):
                report.handle(os.path.join(options.pocket_items_path, f))
        else:
            report.handle(options.pocket_items_path)

    def __do_time_series_reporting(self, options):
        if os.path.isdir(options.pocket_items_path) != True:
            print "Error: Time series reporting can only be done on a set of files in a directory path."
            return
        time_series_report = TimeSeriesReport()
        for f in os.listdir(options.pocket_items_path):
            time_series_report.handle(os.path.join(options.pocket_items_path, f))
        time_series_report.print_report()

    def execute(self, options):
        if (options.time_series != True):
            self.__do_regular_reporting(options)
        else:
            self.__do_time_series_reporting(options)




