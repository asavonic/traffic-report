#!/usr/bin/env python3
'''
Traffic tracker with SMS reporting

Usage:
  traftrack [--config=FILE]

Options:
  --config=FILE  path to the configuration file
'''
import sys
from docopt import docopt

import yamaps
import reporter
import config


def main(argv):
    args = docopt(__doc__, argv=argv, version='0.1')
    conf = config.read_config(args['--config'])
    for user in conf.users:
        traffic = {}
        for place in user.places:
            traffic[place.name] = yamaps.get_traffic(
                place.mask_path,
                place.coord,
                place.size,
                place.zoom)
        reporter.send_report(format_report(traffic, user, conf),
                             user)


def format_report(traffic_level_map, client, config):
    strings = config.strings[client.lang]
    msg = strings['Greetings']
    for place in sorted(traffic_level_map):
        msg += " {}: {}".format(place, strings[traffic_level_map[place]])
    return msg


if __name__ == '__main__':
    main(sys.argv[1:])
