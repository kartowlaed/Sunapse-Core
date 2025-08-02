class Item:
    def __init__(self, item_id, name, count=1):
        self.id = item_id
        self.name = name
        self.count = count

class Inventory(dict):
    def add(self, item: Item):
        self[item.id] = self.get(item.id, 0) + item.count
