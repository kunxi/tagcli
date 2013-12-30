#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import shutil
import pkg_resources

from functools import wraps
from mutagen.mp4 import MP4
from docopt import docopt


#__version__ = pkg_resources.require("tagcli")[0].version
__version__ = "0.1.0"
__all__ = ['dump', 'rename', 'help']


def add_generic_tags(metadata, format):
    if format == MP4:
        for key, value in [
            ('artist', '\xa9ART'),
            ('album', '\xa9alb'),
            ('title', '\xa9nam'),
            ('genre', 'gnre'),
            ('date', '\xa9day')]:
            if value in metadata:
                metadata[key] = metadata[value][0]

        if 'trkn' in metadata:
            metadata['tracknumber'] = metadata['trkn'][0][0]
        discnumber = metadata.get('disk')
        metadata['discnumber'] = discnumber[0][0] if discnumber else '1'

def meta_gen(files):
    """Yield (metadaa, filename) tuple for each file."""
    formats = {
        'm4a': MP4
    }
    for f in files:
        _, ext = os.path.splitext(f)
        if ext:
            ext = ext[1:]
        format = formats.get(ext.lower())
        if format:
            metadata = format(f)
            # update the metadata with generic field name
            add_generic_tags(metadata, format)
            yield metadata, f

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
    for m, f in meta_gen(args['<files>']):
        print(f)
        print(m.pprint())

@argparsed
def rename(args):
    """
usage: tag rename [options] <pattern> <files>...

Rename <files> with the naming <pattern> formated by the audio meta file.

Options:
    <pattern>           The file name pattern using python string format syntax.
                        See 'tag help tags' for supported tags.
    -p, --dry-run       Print the action the command will take without actually changing any files.

Examples:

tag rename '{discnumber}-{tracknumber:02} {artist} - {album} - {title}' foo.mp3 bar.m4a

    """
    pattern = args['<pattern>']
    for m, f in meta_gen(args['<files>']):
        _, ext = os.path.splitext(f)
        filename = unicode(pattern).format(**m) + ext
        print("'%s'  ==>  '%s'" % (f, filename.encode('utf-8')))
        if not args['--dry-run']:
            fullname = os.path.join(os.path.dirname(f), filename)
            shutil.move(f, fullname)

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
The foobar 2000 convention is adopted for the tag name. You are free to use container-specific
tag name or the generic tag name as specified below for the sake of portability:

    +-------------+-----------------------+------+
    | Tag Name    | ID3v2                 | AAC  |
    |-------------+-----------------------+------+
    | artist      | TPE1                  | ©ART |
    |-------------+-----------------------+------+
    | album       | TALB                  | ©alb |
    |-------------+-----------------------+------+
    | title       | TIT2                  | ©nam |
    |-------------+-----------------------+------+
    | discnumber  | TPOS                  | disk |
    |-------------+-----------------------+------+
    | tracknumber | TRCK                  | trkn |
    +-------------+-----------------------+------+

    data source:
        [mp4v2 wiki]: https://code.google.com/p/mp4v2/wiki/iTunesMetadata
        [Foobar2000:ID3 Tag Mapping]: http://wiki.hydrogenaudio.org/index.php?title=Foobar2000:ID3_Tag_Mapping
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
