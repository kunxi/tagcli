#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pkg_resources
from docopt import docopt

#__version__ = pkg_resources.require("tagcli")[0].version
__version__ = "0.1.0"

class Runner(object):
    @staticmethod
    def rename(*args):
        """
        usage: tag rename [--dry-run] <pattern> <files>...

        """
        pass

def main():
    """
usage: tag [--version] [--help] [--dry-run]
           <command> [<args>...]

options:
   -h, --help     Print this help
   --dry-run      Print the action the command will take without actually changing any files.

The most commonly used commands are:
   rename         Rename the audio file with meta data
   update         Update the audio meta data
   dump           Dumps the audio meta data

See 'tag help <command>' for more information on a specific command.
    """
    args = docopt(main.__doc__,
                  version='tag version %s' % __version__,
                  options_first=True)

    cmd = args['<command>']
    try:
        if cmd == 'help':
            if args['<args>']:
                cmd = args['<args>'][-1]
                method = docopt(getattr(Runner, cmd).__doc__)
            else:
                print(docopt(main.__doc__, argv='-h'))

        method = getattr(Runner, cmd)
        assert callable(method)
        return method(args)
    except (AttributeError, AssertionError):
        exit("%r is not a tag command. See 'tag help'." % cmd)

if __name__ == "__main__":
    main()
