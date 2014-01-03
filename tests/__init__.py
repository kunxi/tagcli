#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import unittest

from contextlib import contextmanager
from StringIO import StringIO
from tempfile import mkstemp


@contextmanager
def redirected_io():
    stdout = sys.stdout
    sys.stdout = tmpfile = StringIO()
    yield tmpfile
    tmpfile.close()
    sys.stdout = stdout


class TestCase(unittest.TestCase):
    def setUp(self):
        fd, self.filename = mkstemp(suffix=self.suffix)
        os.close(fd)
        shutil.copy(self.original, self.filename)

    def tearDown(self):
        try:
            os.unlink(self.filename)
        except OSError:
            pass
