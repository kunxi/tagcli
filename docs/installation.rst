.. _Installation:

Installation
============

tagcli works with CPython version 2.6, 2.7 and also pypy.

There is no plan to support python 3 unless the dependency, mutagen_, supports
python 3.

.. _mutagen: https://code.google.com/p/mutagen/

Installing a released version
-----------------------------

You can install the most recent tagcli version using `easy_install`_::

    $ sudo easy_install tagcli

Or you can also use pip_ ::

    $ sudo pip install tagcli

Either way we strongly recommend using these tools in combination with
`virtualenv`_::

    $ mkvirtualenv tagcli
    $ pip install tagcli

This will install a tagcli egg in your Python installation's `site-packages`
directory.

Alternatively you can install tagcli from the release tarball:

1.  Download the most recent tarball from the `download page`_.
2.  Unpack the tarball.
3.  ``sudo python setup.py install``

Note that the last command will automatically download and install
`setuptools`_ if you don't already have it installed.  This requires a working
Internet connection.

This will install tagcli into your Python installation's `site-packages`
directory.


Installing the development version
----------------------------------

If you prefer living on the edge, be my guest. ::

    $ git clone git://github.com/kunxi/tagcli.git
    $ cd tagcli
    $ sudo python setup.py install

Please checkout :ref:`contributing` for more details for development installation.

.. _download page: https://github.com/kunxi/tagcli/releases/latest
.. _setuptools: http://peak.telecommunity.com/DevCenter/setuptools
.. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _Git: http://git-scm.org/
.. _pip: http://www.pip-installer.org/
.. _virtualenv: http://www.virtualenv.org/


Troubleshooting
---------------

A command line utility, ``tag`` will be installed with the tagcli package.
You may invoke the following command for verification after installation::

    $ tag --version
    tag version 0.2.0

If the shell complains that the command is not found, try run the following
command for diagnosis::

    $ python -m tagcli --version
    tag version 0.2.0

Make sure you have activated the appropriated virtualenv if the 
tagcli is installed in the virtualenv environment.

If it works, it is likely that ``tag`` is not in your ``PATH``
environment variable. Try to find the ``tag`` command and add its directory in
your ``PATH`` environment variable.

If the python interpreter complains that ``No module named tagcli``, try
to reinstall the tagcli as specified above.
