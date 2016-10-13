import json


class Config(object):
    def __init__(self, j):
        self.users = [ConfigUser(uid, j)
                      for uid, j in j['users'].items()]
        self.strings = j['strings']


class ConfigUser(object):
    def __init__(self, uid, j):
        self.uid = uid
        self.name = j['name']
        self.lang = j['lang']
        self.contacts = j['contacts']
        self.places = [ConfigPlace(place)
                       for place in j['places']]


class ConfigPlace(object):
    def __init__(self, j):
        self.name = j['name']
        self.coord = (j['lat'], j['lon'])
        self.size = (j['size_x'], j['size_y'])
        self.zoom = j['zoom']
        self.mask_path = j['mask_path']
        self.max_levels = j['max_levels']


def read_config(filename):
    with open(filename, 'r') as f:
        return json.load(f)
