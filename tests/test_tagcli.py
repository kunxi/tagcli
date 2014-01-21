#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import unittest
import pytest

from mutagen.easymp4 import EasyMP4
from mutagen.easyid3 import EasyID3
from tagcli import SimpleDict, load, main, rename
from . import redirected_io, TestCase


class TestID3(TestCase):
    original = os.path.join('tests', 'data', 'silence-44-s-v1.mp3')
    suffix = '.mp3'

    def test_load(self):
        assert isinstance(load(self.filename), EasyID3)

    def test_dump(self):
        with redirected_io() as stdout:
            main(['dump', self.filename])
            assert stdout.getvalue() == '''%s
album=Quod Libet Test Data
artist=piman
date=2004
genre=Darkwave
title=Silence
tracknumber=2
''' % self.filename

    def test_rename(self):
        with redirected_io() as stdout:
            main(['rename',  '--dry-run',
                  '{tracknumber:02} {artist} - {album} - {title}',
                  self.filename])
            assert stdout.getvalue() == \
                """'%s'  ==>  '02 piman - Quod Libet Test Data - Silence.mp3'
""" % self.filename

    def test_update(self):
        main(['update', '--artist=Bob Dylan',
              '--album=Family Album', '--title=Monty Python',
              self.filename])
        mp3 = EasyID3(self.filename)
        assert mp3['artist'][0] == 'Bob Dylan'
        assert mp3['album'][0] == 'Family Album'
        assert mp3['title'][0] == 'Monty Python'


class TestMP4(TestCase):
    original = os.path.join('tests', 'data', 'has-tags.m4a')
    suffix = '.m4a'

    def test_load(self):
        assert isinstance(load(self.filename), EasyMP4)

    def test_dump(self):
        with redirected_io() as stdout:
            main(['dump', self.filename])
            assert stdout.getvalue() == '''%s
MPEG-4 audio, 3.71 seconds, 2914 bps (audio/mp4)
artist=Test Artist
''' % self.filename

    def test_rename_dryrun(self):
        with redirected_io() as stdout:
            main(['rename',  '--dry-run', '{artist}', self.filename])
            assert stdout.getvalue() == """'%s'  ==>  'Test Artist.m4a'
""" % self.filename

    def test_rename(self):
        with redirected_io() as stdout:
            main(['rename',  '{artist}', self.filename])
            f = 'Test Artist.m4a'
            assert stdout.getvalue() == "'%s'  ==>  '%s'\n" % (
                self.filename, f)
            filename = os.path.join(os.path.dirname(self.filename), f)
            assert os.access(filename, os.R_OK)
            os.unlink(filename)

    def test_update_dryrun(self):
        with redirected_io() as stdout:
            main(['update', '--dry-run', "--artist=Alice", self.filename])
            assert stdout.getvalue() == """Update tags for %s:
artist: Alice
""" % self.filename

    def test_update(self):
        main(['update', "--artist=Alice", self.filename])
        assert EasyMP4(self.filename)['artist'][0] == 'Alice'


class TestCrossfire(TestCase):
    original = os.path.join('tests', 'data', 'has-tags.m4a')
    suffix = '.m4a'
    foo = '/tmp/non_exist.foo'

    def test_rename(self):
        with redirected_io() as stdout:
            main(['rename', '--dry-run', '--verbose', '{artist}',
                 self.filename, self.foo])
            assert stdout.getvalue() == """'%s'  ==>  'Test Artist.m4a'
Skipping %s: unknown extension: .foo\n""" % (self.filename, self.foo)

    def test_update_trackstart(self):
        with redirected_io() as stdout:
            main(['update', '--verbose', '--dry-run', '--artist=Alice',
                  '--trackstart=10', self.filename, self.original])
            assert stdout.getvalue() == """Update tags for %s:
tracknumber: 10
artist: Alice
Update tags for %s:
tracknumber: 11
artist: Alice
""" % (self.filename, self.original)


class TestSimpleDict(unittest.TestCase):
    def setUp(self):
        self.dict = SimpleDict(dict(foo=['egg'], bar=['spam']))

    def test_attr(self):
        assert hasattr(self.dict, 'keys')

    def test_getitem(self):
        assert self.dict['foo'] == 'egg'

    def test_key_error(self):
        with pytest.raises(KeyError):
            self.dict['non_exist']


def test_load_error():
    with pytest.raises(NotImplementedError):
        assert(load('/tmp/foo.bar'))


def test_dump_error():
    with redirected_io() as stdout:
        f = '/tmp/non_exist.bar'
        main(['dump', f])
        assert stdout.getvalue() == '''Skipping %s: unknown extension: .bar
''' % f


def test_rename_error():
    foo = '/tmp/non_exist.foo'
    bar = '/tmp/non_exist.bar'

    with redirected_io() as stdout:
        main(['rename', '{artist}', foo, bar])
        assert stdout.getvalue() == ''


def test_rename_error_verbose():
    foo = '/tmp/non_exist.foo'
    bar = '/tmp/non_exist.bar'
    with redirected_io() as stdout:
        main(['rename', '--verbose', '{artist}', foo, bar])
        assert stdout.getvalue() == '''Skipping %s: unknown extension: .foo
Skipping %s: unknown extension: .bar
''' % (foo, bar)


def test_update_error_verbose():
    foo = '/tmp/non_exist.foo'
    bar = '/tmp/non_exist.bar'
    with redirected_io() as stdout:
        main(['update', '--verbose', foo, bar])
        assert stdout.getvalue() == '''Skipping %s: unknown extension: .foo
Skipping %s: unknown extension: .bar
''' % (foo, bar)


def test_help_command():
    with redirected_io() as stdout:
        main(['help', 'rename'])
        assert stdout.getvalue() == rename.__doc__ + '\n'


def test_help_missing():
    with pytest.raises(SystemExit) as excinfo:
        main(['help', 'non-exist'])
    assert excinfo.exconly() == \
        "SystemExit: 'non-exist' is not a tag command. See 'tag help'."


def test_help():
    with redirected_io() as stdout:
        with pytest.raises(SystemExit):
            main(['help'])
        assert stdout.getvalue() == '%s\n' % main.__doc__


def test_main():
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.exconly() == """DocoptExit: Usage:
  tag <command> [<options>...]"""


def test_missing_command():
    with pytest.raises(SystemExit) as excinfo:
        main(['non-exist'])
    assert excinfo.exconly() == \
        "SystemExit: 'non-exist' is not a tag command. See 'tag help'."
