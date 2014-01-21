#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os.path
import shutil

from functools import wraps
from mutagen.easymp4 import EasyMP4
from mutagen.easyid3 import EasyID3
from docopt import docopt


__version__ = '0.2.0'

# the following text keys are registered for the sake of compatibility.
for frameid, key in ({
    "TPE2": "albumartist"
}.items()):
    EasyID3.RegisterTextKey(key, frameid)


class SimpleDict(object):
    '''A compatible wrapper for EasyID3 and EasyMP4.'''
    def __init__(self, meta):
        self.meta = meta

    def __getattr__(self, name):
        # delegate everything to the self.meta under the hood
        return getattr(self.meta, name)

    def __getitem__(self, name):
        # special care for the tracknumber and discnumber
        # both of them are rendered as index/total pair.
        if name in self.meta:
            if name in ('tracknumber', 'discnumber'):
                return int(self.meta[name][0].split('/')[0])
            return self.meta[name][0]
        else:
            # FUTURE: extend the tag support, for example: tracktotal
            raise KeyError(name)


def load(filename):
    """Return a tagging instance."""
    _, ext = os.path.splitext(filename)
    if ext == '.m4a':
        return EasyMP4(filename)
    elif ext == '.mp3':
        return EasyID3(filename)
    else:
        raise NotImplementedError('unknown extension: %s' % ext)


def argparsed(func):
    @wraps(func)
    def wrapped(argv):
        args = docopt(func.__doc__, argv=argv)
        return func(args)
    return wrapped


@argparsed
def dump(args):
    """
usage: tag dump <files>...

Dump audio meta data of the <files>.
    """
    for f in args['<files>']:
        try:
            meta = load(f)
            print(f)
            print(meta.pprint())
        except NotImplementedError as exc:
            print('Skipping %s: %s' % (f, exc.message))


@argparsed
def rename(args):
    """
usage: tag rename [options] <pattern> <files>...

Rename <files> with the naming <pattern> formated by the tags.

Options:
  <pattern>           The file name pattern using python string format
                      syntax. See 'tag help tags' for supported tags.
  -p, --dry-run       Print the action the command will take without
                      actually changing any files.
  --verbose           Output extra information about the work being done.

Examples:

  tag rename '{discnumber}-{tracknumber:02}.{album} - {title}' foo.mp3

    """
    pattern = args['<pattern>']
    for f in args['<files>']:
        try:
            meta = SimpleDict(load(f))
        except NotImplementedError as exc:
            if args['--verbose']:
                print('Skipping %s: %s' % (f, exc.message))
            continue

        _, ext = os.path.splitext(f)
        filename = unicode(pattern).format(**meta) + ext
        print("'%s'  ==>  '%s'" % (f, filename.encode('utf-8')))
        if not args['--dry-run']:
            fullname = os.path.join(os.path.dirname(f), filename)
            shutil.move(f, fullname)


@argparsed
def update(args):
    """
usage:
  tag update [--tracknumber=<tracknumber>] [options] <files>...
  tag update [--trackstart=<trackstart>] [options] <files>...

Update the <files> with the specified tags.

Options:
  --artist=<artist>   Set the artist tag metadata.
  --album=<album>     Set the album tag metadata.

  --title=<title>     Set the title tag metadata.
  --albumartist=<album-artist>
                      Set the album artist tag metadata.
  --discnumber=<discnumber>
                      Set the disc number tag metadata.
  --tracknumber=<tracknumber>
                      Set the track number tag metadata.
  --trackstart=<trackstart>
                      If set, the tracknumber is incremented in ascending order.

  -p, --dry-run       Print the action the command will take without
                      actually changing any files.
  --verbose           Output extra information about the work being done.

Examples:

  1. update the compiled album
  tag update --artist='张靓颖‘ --album-artist='Various Artists' foo.mp3

  2. update the album track number with sorted order
  tag update --albumartist='Various Artists' --trackstart=50 50.mp3 51.mp3

    """
    def iter(args):
        for k, v in args.items():
            if k in ('--dry-run', '--trackstart', '--verbose'):
                continue
            if v is not None and k.startswith('--'):
                yield (k[2:], v.decode('utf-8'))

    options = dict(iter(args))
    for index, f in enumerate(args['<files>'],
                              int(args.get('--trackstart') or 1)):
        try:
            meta = load(f)
        except NotImplementedError as exc:
            if args['--verbose']:
                print('Skipping %s: %s' % (f, exc.message))
            continue

        if args.get('--trackstart'):
            options.update(tracknumber=str(index))

        if args['--dry-run']:
            print("Update tags for %s:" % f)
            print("\n".join("%s: %s" % (k, v) for k, v in options.items()))
        else:
            meta.update(options)
            meta.save(f)


def help(argv):
    if len(argv) > 1:
        cmd = argv[-1]
        try:
            print(globals()[cmd].__doc__)
        except KeyError:
            exit("%r is not a tag command. See 'tag help'." % cmd)
    else:
        docopt(main.__doc__, argv='-h')


def tags():
    """
The tag uses the same tag naming convention as EasyID3 in the mutagen library.
Here are the most commonly used tag names:

    +==============+=======+======+
    | Tag Name     | ID3v2 | AAC  |
    |==============+=======+======|
    | artist       | TPE1  | ©ART |
    |--------------+-------+------|
    | albumartist  | TPE2  | aART |
    |--------------+-------+------|
    | album        | TALB  | ©alb |
    |--------------+-------+------|
    | title        | TIT2  | ©nam |
    |--------------+-------+------|
    | discnumber   | TPOS  | disk |
    |--------------+-------+------|
    | tracknumber  | TRCK  | trkn |
    +--------------+-------+------+

    """
    raise NotImplementedError


def main(argv=None):
    """A mutagen-based tag editor.

Usage:
  tag <command> [<options>...]


General Options:
  -h, --help    Show help.
  --version     Show version and exit.

Commands:
 rename         Rename file using pattern with tags.
 update         Update the tags.
 dump           Dumps the tags.
 tags           Show generic tag names.

See 'tag help <command>' for more information on a specific command."""
    args = docopt(main.__doc__,
                  version='tag version %s' % __version__,
                  options_first=True,
                  argv=argv or sys.argv[1:])

    cmd = args['<command>']
    try:
        method = globals()[cmd]
        assert callable(method)
    except (KeyError, AssertionError):
        exit("%r is not a tag command. See 'tag help'." % cmd)

    argv = [args['<command>']] + args['<options>']
    return method(argv)

if __name__ == "__main__":
    main()
