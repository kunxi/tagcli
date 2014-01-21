.. _usage:

=====
Usage
=====

tag
---

``tag`` is a mutagen-based tag editor to manipulate the audio file
meta data, where other tag editors may fall short.

Usage
*****
::

  tag <command> [<options>...]

Options
*******

  ``-h, --help``
    Show help.

  ``--version``
    Show version and exit.

tag rename
----------
Usage
*****
::

  tag rename [options] <pattern> <files>...

Rename the specified ``files`` with the naming ``pattern`` formated by the tags.

Options
*******

  ``<pattern>``
    The file name pattern using python string format
    syntax. See 'tag help tags' for supported tags.

  ``-p, --dry-run``
    Print the action the command will take without
    actually changing any files.

  ``--verbose``
    Output extra information about the work being done.

Examples
********

Assuming you want to rename M4A files as the specific pattern:
``{tracknumber} - {title}.m4a``, with tagcli: ::

    tag renmae '{tracknumber} - {title}' *.m4a

If you prefer tracknumber with zero padding, like "01 - song title.m4a",
you can setup the format of the tracknumber as well::

    tag rename '{tracknumber:02} - {title}' *.m4a

.. note::

    ``tag rename`` will not move the files, it only rename the files in place,
    make sure you have write privilege in that directory.

tag update
----------

Usage
*****
::

  tag update [--tracknumber=<tracknumber>] [options] <files>...
  tag update [--trackstart=<trackstart>] [options] <files>...

Update the ``files`` with the specified tags.
Options
*******

  ``--artist=<artist>``
    Set the artist tag metadata.

  ``--albumartist=<album-artist>``
    Set the album artist tag metadata.
  
  ``--album=<album>``
    Set the album tag metadata.
  
  ``--title=<title>``
    Set the title tag metadata.

  ``--discnumber=<discnumber>``
    Set the disc number tag metadata.

  ``--tracknumber=<tracknumber>``
    Set the track number tag metadata.

  ``--trackstart=<trackstart>``
    If set, the tracknumber is incremented in ascending order.

Examples
********

Assume you have collected some popular hits from various
albums, you want to create a compilation album named as "Billboard 2013 Top 100".
First, let's copy all the songs to a dedicated folder, then run the following
command::

    tag update --album='Billboard 2013 top 100' \
      --albumartist='Various Artists' --trackstart=10 \
      roar.mp3 locked-out-of-heaven.mp3 ho-hey.mp3 ...

``tag`` will update the album and albumartist filed, so iTune and other music
organize app will recoganize them as a compilation album. The ``--trackstart``
option specifies the the tracknumber for the very first file, *roar.mp3* in our
example, then automatically increment the tracknumber for the listed files in 
the ascending order.


tag help
--------
Usage
*****
::

  tag help <command>

Get the help or the help of the specified command.
