#!/usr/bin/env python
from __future__ import print_function

import sys

from sloika.tools.chunkify_with_identity import chunkify_with_identity_main
from sloika.tools.chunkify_with_remap import chunkify_with_remap_main


def main(argv):

    scripts = {
        'identity': chunkify_with_identity_main,
        'remap': chunkify_with_remap_main,
    }

    if 1 == len(argv):
        print("Available commands:")
        print('\t'+'\n\t'.join(sorted(scripts.keys())))
    else:
        command_name = argv[1]
        try:
             command_function = scripts[command_name]
        except:
            print('Unsupported command {!r}'.format(command_name))
            sys.exit(1)

        command_arguments = argv[1:]

        try:
            return command_function(command_arguments)
        except:
            print('Exception when running command {!r}'.format(command_name))
            raise


if __name__ == '__main__':
    sys.exit(main(sys.argv[:]))
