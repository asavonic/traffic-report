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

import client
import reporter
import config


def main(argv):
    args = docopt(__doc__, argv=argv, version='0.1')
    conf = config.read_config(args['--config'])
    for c in conf['clients']:
        report = client.make_report(c)
        reporter.send_report(report, c)


if __name__ == '__main__':
    main(sys.argv[1:])
