class Wallet:
    def __init__(self, emeralds=0, rubies=0, ender_eyes=0):
        self.emeralds = emeralds
        self.rubies = rubies
        self.ender_eyes = ender_eyes

    def transfer(self, other, emeralds=0, rubies=0, ender_eyes=0):
        if self.emeralds >= emeralds and self.rubies >= rubies and self.ender_eyes >= ender_eyes:
            self.emeralds -= emeralds
            self.rubies -= rubies
            self.ender_eyes -= ender_eyes
            other.emeralds += emeralds
            other.rubies += rubies
            other.ender_eyes += ender_eyes
            return True
        return False
import yaml
import pathlib

SHOP_PATH = pathlib.Path(__file__).resolve().parent.parent / 'data' / 'shop.yaml'

with open(SHOP_PATH, 'r') as f:
    SHOP = yaml.safe_load(f) or {}

def get_shop():
    return SHOP.get('shop', {})
