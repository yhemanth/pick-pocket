from datetime import date


class PocketItem():
    def __init__(self, pocket_item):
        self.item_id = pocket_item['item_id']
        self.resolved_url = pocket_item['resolved_url']
        self.time_added = date.fromtimestamp(int(pocket_item['time_added']))
        self.time_updated = date.fromtimestamp(int(pocket_item['time_updated']))

    def __str__(self):
        return self.item_id+"|"+self.resolved_url+"|"+str(self.time_added)+"|"+str(self.time_updated)
