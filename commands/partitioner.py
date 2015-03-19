from datetime import date
import json
from os import path
import os
import shutil


class Partitioner():

    def __init__(self, pocket_items_directory, overwrite):
        self.pocket_items_directory = pocket_items_directory
        if overwrite and os.path.exists(self.pocket_items_directory):
            shutil.rmtree(self.pocket_items_directory)
        if not os.path.exists(self.pocket_items_directory):
            os.makedirs(self.pocket_items_directory)

    def write(self, pocket_item):
        yyyymm = date.fromtimestamp(int(pocket_item['time_added'])).strftime('%Y-%m')
        partition_file = path.join(self.pocket_items_directory, yyyymm+'-pocket-items')
        with open(partition_file, 'a') as f:
            f.write(json.dumps(pocket_item))
            f.write('\n')
