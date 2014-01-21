Quickstart
==========

Rename files with pattern

::

    $ tag renmae '{tracknumber:02} - {title}' *.m4a
    foo.m4a ==> 01 - Some Song.m4a
    [...]

Update tags

::

    $ tag update --album='Top 100 hits' *.mp3

Dump tags

::

    $ tag dump *.mp3
    MPEG-4 audio, 3.71 seconds, 2914 bps (audio/mp4)
    artist=Test Artist

Show the help

::

    $ tag help
    usage: tag [--version] [--help]
           <command> [<args>...]

    [...]

Show the help for command

::

    $ tag help update
    usage:
      tag update [--tracknumber=<tracknumber>] [options] <files>...
      tag update [--trackstart=<trackstart>] [options] <files>...
    [...]
