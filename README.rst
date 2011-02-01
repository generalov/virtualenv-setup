This tool could help you to create new isolated Python environment.


Status and License
------------------

It is written by Evgeny Generalov, and sponsored by the, damn!.. nobody. It is
licensed under an `MIT-style permissive license`_.


Usage
-----

The easiest way to create virtualenv to open a terminal and type::
   
   python -murllib http://tiny.cc/ve-setup | python
   . ./python/bin/activate

You can address It by full URL or pass any virtualenv_ option::

   python -murllib https://github.com/generalov/virtualenv-setup/raw/1.0/ve_setup.py \
      | python - --no-site-packages .venv

Common usage pattern::

   Usage: ve_setup.py [[virtualenv options] DEST_DIR]

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

If you want to use virutalenv in your script, just put ``ve_setup.py`` into any
directory on the ``PYTHONPATH``, and add this to the top::

    #!/usr/bin/env python
    try:
        from ve_setup import use_virtualenv
    except ImportError:
        import urllib
        urllib.retrive("http://tiny.cc/ve-setup", 've_setup.py')
        from ve_setup import use_virtualenv

    use_virtualenv(['--distribute', "python"], requirements="requirements.pip")

This will create virtualenv if needed, install requirements and activate it.


.. _ez_setup.py: http://peak.telecommunity.com/dist/ez_setup.py
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _`MIT-style permissive license`: LICENCE
