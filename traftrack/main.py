#!/usr/bin/env python3
'''
Traffic tracker with SMS reporting

Usage:
  traftrack --users=FILE --l10n=FILE [--verbosity=LEVEL]

Options:
  --users=FILE    path to the config with users descriptions
  --l10n=FILE     path to the localization file

  --verbosity=LEVEL  logging level from 0 to 4 [default: 2]
                       0 for only critical errors
                       1 for all errors
                       2 for all warnings
                       3 for info messages (i.e. report have been sent to XXX)
                       4 for full output with debug information
'''
import logging
import sys

from docopt import docopt

import config
import yamaps


def main(argv):
    args = docopt(__doc__, argv=argv, version='0.1')

    users = config.read_users_config(args['--users'])
    l10n = config.read_l10n(args['--l10n'])
    log_level = 50 - 10 * max(0, min(4, int(args['--verbosity'])))
    set_logger(log_level)

    for uid, u in users.items():
        report = create_report(config.read_places(u['places_config']),
                               l10n.get(u['lang']))
        send_report(u, report)
        logging.getLogger().info('Report have been sent to %s', uid)


def create_report(places, l10n):
    traffic = {}
    for place in places:
        traffic[place.name] = yamaps.get_traffic(
            place.mask_path,
            place.coord,
            place.size,
            place.zoom)
    return format_report(traffic, l10n)


def format_report(traffic_level_map, l10n):
    msg = l10n['Greetings']

    for place in sorted(traffic_level_map):
        traffic_level = traffic_level_map[place]
        msg += " {}: {}".format(l10n.get(place, place),
                                l10n[traffic_level])
    return msg


def send_report(user, report):
    logging.getLogger().debug('Sending SMS to %s: %s',
                              user['phone'], report)


def set_logger(level):
    f = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=f)
    logging.getLogger().setLevel(level)



if __name__ == '__main__':
    main(sys.argv[1:])
