#!/usr/bin/env python
"""Bootstrap virutalenv installation

If you want to use virutalenv in your bootstap script, just include this
file in the same directory with it, and add this to the top::

    from ve_setup import use_virtualenv
    use_virtualenv()

If you want to require a specific version of virtualenv, set a download
mirror, or use an alternate installation directory, you can do so by supplying
the appropriate options to ``use_virtualenv()``.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import urllib


# Defaults
VIRTUALENV_VERSION = '1.7.1.2'
VIRTUALENV_ARGS = ['python']

#
# Working around error with PYTHONHOME
#
if 'PYTHONHOME' in os.environ:
    del os.environ['PYTHONHOME']
    print "WARNING: ignoring the value of the PYTHONHOME environment " \
          " variable! This value can corrupt the virtual python installation."

def use_virtualenv(argv, version=VIRTUALENV_VERSION, activate=True,
        requirements=None):
    """Install and use virtualenv environment."""

    virtualenv = VirtualEnv(argv, version=version)
    if not virtualenv.is_exists:
        virtualenv.create()
        if requirements:
            virtualenv.install_requirements(requirements)
    if activate:
        virtualenv.activate()
    return virtualenv

def log(message):
    """Log message"""

    sys.stderr.write(": %s\n" % message)


class VirtualEnv(object):
    """Virtual environment"""

    def __init__(self, argv, version=None):
        self.python_name = os.path.basename(sys.executable)
        self.version = version or VIRTUALENV_VERSION
        self.path = os.path.abspath(argv[-1])
        self.argv = argv

    @property
    def scripts_dir(self):
        """Return path where scripts directory is located."""

        return os.path.join(self.path, 'Scripts' if sys.platform == 'win32'
                else 'bin')

    @property
    def is_exists(self):
        """Check this environment is installed."""

        return os.path.isfile(os.path.join(self.scripts_dir, self.python_name))
    
    @property
    def is_activated(self):
        """Check this environment is activated."""

        return 'VIRTUAL_ENV' in os.environ and \
                os.environ['VIRTUAL_ENV'] == self.path

    def create(self):
        """Create this environment."""

        tmpdir = tempfile.mkdtemp()
        virtualenv_requirement = 'virtualenv==%s' % self.version
        try:
            log("using virtualenv version %s" % self.version)
            installer = EZSetupInstaller(tmpdir)
            installer.install(virtualenv_requirement)
            virtualenv_py = os.path.join(tmpdir, 'virtualenv', 'virtualenv.py')
            virtualenv_cmd = [sys.executable, virtualenv_py] + self.argv
            log("execute %s" % " ".join(virtualenv_cmd))
            subprocess.call(virtualenv_cmd)
        finally:
            shutil.rmtree(tmpdir)

    def activate(self):
        """Activate this environment."""

        if self.is_activated:
            return # this environment is activated
        activate_this = os.path.join(self.scripts_dir, 'activate_this.py')
        execfile(activate_this, dict(__file__=activate_this))
        os.environ['VIRTUAL_ENV'] = self.path
        if not self.scripts_dir in os.getenv('PATH', ''):
            os.environ['PATH'] = os.pathsep.join(
                    [self.scripts_dir, os.getenv('PATH', '')])

    def install_requirements(self, requirements, extra_pip_args=None):
        """Install requirements from the `requirements` file."""

        pip_exe = os.path.join(self.scripts_dir, "pip")
        cmd = [pip_exe, "install", "-r", requirements] + (extra_pip_args or [])
        out = subprocess.Popen(cmd).communicate()


class EZSetupInstaller(object):
    """Installer"""

    EZ_SETUP_PY = 'ez_setup.py'
    EZ_SETUP_URL = 'http://peak.telecommunity.com/dist/ez_setup.py'

    def __init__(self, install_dir, ez_setup_py=None):
        self.install_dir = install_dir
        self.ez_setup_py = ez_setup_py or (
                os.path.join(os.getcwd(), self.EZ_SETUP_PY) if os.path.isfile(
                    os.path.join(os.getcwd(), self.EZ_SETUP_PY)) else
                os.path.join(self.install_dir, self.EZ_SETUP_PY))
        self._fetch_ez_setup_py()

    def install(self, requirement):
        """Install given requirement."""

        env = os.environ.copy()
        env['PYTHONPATH'] = self.install_dir
        ez_setup_cmd = [sys.executable, self.ez_setup_py,
                '-q', '--editable', '--build-directory',  self.install_dir,
                requirement]
        log("download %s with %s" % (requirement, " ".join(ez_setup_cmd)))
        subprocess.call(ez_setup_cmd, env=env)

    def _fetch_ez_setup_py(self):
        """Fetch ez_setup.py."""

        if not os.path.isfile(self.ez_setup_py):
            ez_setup_url = self.EZ_SETUP_URL
            log("download %s to %s" % (ez_setup_url, self.ez_setup_py))
            urllib.urlretrieve(ez_setup_url, self.ez_setup_py)


if __name__ == '__main__':
    import traceback

    def main():
        """Main function."""

        version = VIRTUALENV_VERSION
        args = sys.argv[1:] if len(sys.argv) > 1 else VIRTUALENV_ARGS
        use_virtualenv(args, version)

    try:
        main()
        sys.exit(0)
    except Exception, e: # Catch all exceptions. pylint: disable=W0703
        sys.stderr.write(traceback.format_exc() if __debug__ else str(e))
        sys.exit(1)

