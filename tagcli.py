#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pkg_resources
from docopt import docopt

#__version__ = pkg_resources.require("tagcli")[0].version
__version__ = "0.1.0"

class Runner(object):
    @classmethod
    def rename(cls, argv, options):
        """
usage: tag rename [--dry-run] <pattern> <files>...

Rename <files> with the <pattern> formated by the audio meta file.

options:
   --dry-run      Print the action the command will take without actually changing any files.

examples:
    tag rename '{discnumber}-{tracknumber} {artist} - {album} - {title}' foo.mp3 bar.m4a

    See 'tag help tags' for supported tags.

        """
        args = docopt(cls.rename.__doc__, argv=argv)

    @classmethod
    def tags(cls):
        """
The foobar 2000 convention is adopted for the tag name. You are free to use container-specific
tag name or the generic tag name as specified below for the sake of portability:

    +-------------+-----------------------+------+
    | Tag Name    | ID3v2                 | AAC  |
    |-------------+-----------------------+------+
    | artist      | TPE1                  | ©art |
    |-------------+-----------------------+------+
    | album       | TALB                  | ©alb |
    |-------------+-----------------------+------+
    | title       | TIT2                  | ©nam |
    |-------------+-----------------------+------+
    | discnumber  | TPOS                  | disk |
    |-------------+-----------------------+------+
    | tracknumber | TRCK                  | trkn |
    |-------------+-----------------------+------+
    | genre       | TCON                  | gnre |
    |-------------+-----------------------+------|
    | date        | TYER(v2.3) TDRC(v2.4) | ©day |
    +-------------+-----------------------+------+

    data source:
        [mp4v2 wiki]: https://code.google.com/p/mp4v2/wiki/iTunesMetadata
        [Foobar2000:ID3 Tag Mapping]: http://wiki.hydrogenaudio.org/index.php?title=Foobar2000:ID3_Tag_Mapping
        """
        raise NotImplemented

    @classmethod
    def help(cls, argv, args):
        if args['<args>']:
            cmd = args['<args>'][-1]
            try:
                print(getattr(Runner, cmd).__doc__)
            except AttributeError:
                exit("%r is not a tag command. See 'tag help'." % cmd)
        else:
            print(docopt(main.__doc__, argv='-h'))

def main():
    """
usage: tag [--version] [--help]
           <command> [<args>...]

options:
   -h, --help     Print this help

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
        method = getattr(Runner, cmd)
        assert callable(method)
        argv = [args['<command>']] + args['<args>']
        return method(argv, args)
    except (AttributeError, AssertionError):
        exit("%r is not a tag command. See 'tag help'." % cmd)

if __name__ == "__main__":
    main()
