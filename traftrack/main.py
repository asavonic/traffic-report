#!/usr/bin/env python3
'''
Traffic tracker with SMS reporting

Usage:
  traftrack [--places=FILE] [--l10n=FILE --l10n-lang=LANG] [--debug]

Options:
  --places=FILE  path to the places description
  --l10n=FILE    path to the localization file
  --l10n-lang=LANG  language to use in localization [default: en_EN]
  --debug        dump intermediate images and print debug messages
'''
import sys
from docopt import docopt
import logging

import yamaps
import reporter
import config


def main(argv):
    args = docopt(__doc__, argv=argv, version='0.1')
    places = config.read_places(args['--places'])
    debug = args['--debug']
    set_logger(debug)
    yamaps.DEBUG = debug

    if args['--l10n']:
        lang = args['--l10n-lang']
        l10n = config.read_l10n(args['--l10n']).get(lang)
    else:
        l10n = None

    traffic = {}
    for place in places:
        traffic[place.name] = yamaps.get_traffic(
            place.mask_path,
            place.coord,
            place.size,
            place.zoom)

    reporter.send_report(format_report(traffic, l10n))


def format_report(traffic_level_map, l10n):
    msg = l10n['Greetings'] if l10n else ''

    for place in sorted(traffic_level_map):
        traffic_level = traffic_level_map[place]
        if l10n:
            traffic_level = l10n(traffic_level)
        msg += " {}: {}".format(place, traffic_level)
    return msg


def set_logger(debug):
    if debug:
        f = '%(asctime)-15s %(message)s'
        logging.basicConfig(format=f)
        logging.getLogger().setLevel(logging.DEBUG)


if __name__ == '__main__':
    main(sys.argv[1:])
