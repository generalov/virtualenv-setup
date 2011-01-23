This tool could help you to create new isolated Python environment.


Status and License
------------------

It is written by Evgeny Generalov, and sponsored by the, damn!.. nothing. It is
licensed under an `MIT-style permissive license`_.


Usage
-----

The easiest way to create virtualenv is open a terminal and type::
   
   python -murllib https://github.com/generalov/virtualenv-setup/raw/master/ve_setup.py | python
   . ./python/bin/activate

You can pass any option to the virtualenv_::

   python -murllib https://github.com/generalov/virtualenv-setup/raw/master/ve_setup.py \
      | python - --no-site-packages .venv

Common usage pattern::

   Usage: ve_setup.py [options] [[virtualenv options] DEST_DIR]

The `DEST_DIR` being suplied must be the latest argument. I'm stupid here.


Win32
^^^^^

Certainly, sir! I tested It with some sort of wine::

    wine C:/python26/python.exe ve_setup.py


What It Does
------------

``ve_setup.py`` is tool to download virtualenv and create new isolated Python
environment.

The basic problem being addressed is to create isolated Python environment on
systems where virtualenv package is not installed. Imagine you have an hosting
with very old ``setuptools`` and without ``virtualenv``. How can you create
isolated Python environment?

``ve_setup.py`` can help you. It download ez_setup.py_ to fetch desired version
of the ``virtualenv`` package into a temporary directory. Then It creates new
isolated Python environment with your arguments in the given directory (named
``python`` by default).


Using ve_setup 
--------------

If you want to use virutalenv in your script, just put ``ve_setup.py`` into the
any directory at the ``PYTHONPATH``, and add this to the top::

    import os, ve_setup
    dest_dir = os.path.join(os.path.dirname(__file__), 'python')
    ve_setup.use_virtualenv([dest_dir])

This will create virtualenv if needed and activate it.


.. _ez_setup.py: http://peak.telecommunity.com/dist/ez_setup.py
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _`MIT-style permissive license`: LICENCE
