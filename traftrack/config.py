import json


class Place(object):
    def __init__(self, j):
        self.name = j['name']
        self.coord = (j['lat'], j['lon'])
        self.size = (j['size_x'], j['size_y'])
        self.zoom = j['zoom']
        self.mask_path = j['mask_path']
        self.max_levels = j['max_levels']


def read_places(filename):
    with open(filename, 'r') as f:
        return [Place(place) for place in json.load(f)['places']]


class L10n(object):
    def __init__(self, j):
        self.lang_map = j

    def get(self, lang):
        return self.lang_map[lang]


def read_l10n(filename):
    with open(filename, 'r') as f:
        return L10n(json.load(f))
