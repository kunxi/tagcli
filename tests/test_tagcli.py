#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import sys
import unittest
import shutil

from mutagen.easymp4 import EasyMP4
from mutagen.easyid3 import EasyID3
from tagcli import load, dump, rename, update
from tempfile import mkstemp
from . import redirected_io, TestCase

class TestID3(TestCase):
    original = os.path.join('tests', 'data', 'silence-44-s-v1.mp3')
    suffix = '.mp3'

    def test_load(self):
        assert isinstance(load(self.filename), EasyID3)

    def test_dump(self):
        with redirected_io() as stdout:
            dump(['dump', self.filename])
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
            rename(['rename',  '--dry-run', '{tracknumber:02} {artist} - {album} - {title}', self.filename])
            assert stdout.getvalue() == """'%s'  ==>  '02 piman - Quod Libet Test Data - Silence.mp3'
""" % self.filename

    def test_update(self):
        update(['update', '--artist=Bob Dylan',
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
            dump(['dump', self.filename])
            assert stdout.getvalue() == '''%s
MPEG-4 audio, 3.71 seconds, 2914 bps (audio/mp4)
artist=Test Artist
''' % self.filename

    def test_rename(self):
        with redirected_io() as stdout:
            rename(['rename',  '--dry-run', '{artist}', self.filename])
            assert stdout.getvalue() == """'%s'  ==>  'Test Artist.m4a'
""" % self.filename

    def test_update(self):
        update(['update', "--artist=Alice", self.filename])
        assert EasyMP4(self.filename)['artist'][0] == 'Alice'
