#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import shutil

from functools import wraps
from mutagen.easymp4 import EasyMP4
from mutagen.easyid3 import EasyID3
from docopt import docopt


__version__ = "0.1.0"

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
            if name in ('tracknumber','discnumber'):
                return int(self.meta[name][0].split('/')[0])
            return self.meta[name][0]
        else:
            return None

def load(filename):
    """Return a tagging instance."""
    _, ext = os.path.splitext(filename)
    if ext == '.m4a':
        return EasyMP4(filename)
    elif ext == '.mp3':
        return EasyID3(filename)
    else:
        raise NotImplementedError('Unknown extension: %s' % ext)

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
        except NotImplemented as exc:
            print('Skipping %s: %s' % (f, exc.message))

@argparsed
def rename(args):
    """
usage: tag rename [options] <pattern> <files>...

Rename <files> with the naming <pattern> formated by the audio meta file.

Options:
    <pattern>           The file name pattern using python string format syntax.
                        See 'tag help tags' for supported tags.
    -p, --dry-run       Print the action the command will take without actually changing any files.
    --verbose           Output extra information about the work being done.

Examples:

    tag rename '{discnumber}-{tracknumber:02} {artist} - {album} - {title}' foo.mp3 bar.m4a

    """
    pattern = args['<pattern>']
    for f in args['<files>']:
        try:
            meta = SimpleDict(load(f))
        except NotImplemented as exc:
            if args['--verbose']:
                print('Skipping %s: %s' % (f, exc.message))

        _, ext = os.path.splitext(f)
        filename = unicode(pattern).format(**meta) + ext
        print("'%s'  ==>  '%s'" % (f, filename.encode('utf-8')))
        if not args['--dry-run']:
            fullname = os.path.join(os.path.dirname(f), filename)
            shutil.move(f, fullname)

@argparsed
def update(args):
    """
usage: tag update [options] [(--tracknumber=<tracknumber> | --trackstart=<trackstart>)] <files>...

Update audio metadata of <files> with specified tags.

Options:
    --artist=<artist>
    --albumartist=<album-artist>
    --album=<album>
    --title=<title>
    --discnumber=<discnumber>
    --tracknumber=<tracknumber>
    --trackstart=<trackstart>)
                        If --trackstart is set, the tracknumber is populated
                        automatically

    -p, --dry-run       Print the action the command will take without actually
                        changing any files.

Examples:

    1. update the compiled album
    tag update --artist='张靓颖‘ --album-artist='Various Artists' foo.mp3 bar.mp3

    2. update the album track number with sorted order
    tag update --albme='Billboard 2013‘ --album-artist='Various Artists' --trackstart=50 \
        50.mp3 51.mp3

    """
    def iter(args):
        for k, v in args.items():
            if k in ('--dry-run', '--trackstart'):
                continue
            if v is not None and k.startswith('--'):
                yield (k[2:], v.decode('utf-8'))

    options = dict(iter(args))
    for index, f in enumerate(args['<files>'], int(args.get('--trackstart') or 1)):
        if args.get('--trackstart'):
            options.update(tracknumber=str(index))
        try:
            meta = load(f)
        except NotImplemented as exc:
            if args['--verbose']:
                print('Skipping %s: %s' % (f, exc.message))

        if args['--dry-run']:
            print "Update tags for %s:" % f
            print "\n".join("%s: %s" % (k, v) for k, v in options.items())
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
        print(docopt(main.__doc__, argv='-h'))

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
    raise NotImplemented


def main():
    """
usage: tag [--version] [--help]
           <command> [<args>...]

Mutagen-based tag command line utilities.

options:
   -h, --help     Print this help

commands:
   rename         Rename the audio file with meta data
   update         Update the audio meta data
   dump           Dumps the audio meta data

concepts:
    tags          The generic tag names across containers

See 'tag help <command>' for more information on a specific command.
    """
    args = docopt(main.__doc__,
                  version='tag version %s' % __version__,
                  options_first=True)

    cmd = args['<command>']
    try:
        method = globals()[cmd]
        assert callable(method)
    except (KeyError, AssertionError):
        exit("%r is not a tag command. See 'tag help'." % cmd)

    argv = [args['<command>']] + args['<args>']
    return method(argv)

if __name__ == "__main__":
    main()
