===============================
tagcli
===============================


A mutagen-based tag editor.

You may use it to rename audio file with pattern

::

    $ tag renmae '{tracknumber:02} - {title}' *.m4a
    foo.m4a ==> 01 - Some Song.m4a
    [...]

or update tags

::

    $ tag update --album='Top 100 hits' *.mp3
