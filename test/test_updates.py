"""Test Updates functions"""
import unittest
import sys
import os
from zfssa_utils.updates import run_updates
from zfssa_utils.common import UPDATELOGFILE

HERE = os.path.abspath(os.path.dirname(__file__))
CSVDIR = os.path.join(HERE, "csvfiles")
SERVERDIR = os.path.join(HERE, "serverfiles")


class Namespace:
    """Class to simulate args parsed"""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestUpdates(unittest.TestCase):
    """Test Updates functions"""

    def test_00_update(self):
        """Update project, filesystem and lun."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        updatefile = os.path.join(CSVDIR, 'update_component.csv')
        listargs = Namespace(server=serverfile, file=updatefile,
                             progress=False, subparser_name='UPDATE',
                             timeout=100, cert=False)
        run_updates(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertFalse('FAIL' in sys.stdout.getvalue())

    def test_01_update_fail_csv(self):
        """Update project, filesystem and lun with wrong csv."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        updatewrongfile = os.path.join(CSVDIR, 'test_create_fs.csv')
        listargs = Namespace(server=serverfile, file=updatewrongfile,
                             progress=False, subparser_name='UPDATE',
                             timeout=100, cert=False)
        run_updates(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('Wrong type' in sys.stdout.getvalue())

    def test_02_update_progress(self):
        """Update project, filesystem and lun with progress."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        updatefile = os.path.join(CSVDIR, 'update_component.csv')
        listargs = Namespace(server=serverfile, file=updatefile,
                             progress=True, subparser_name='UPDATE',
                             timeout=100, cert=False)
        run_updates(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertFalse('FAIL' in sys.stdout.getvalue())
        self.assertTrue(os.path.exists(UPDATELOGFILE))
        try:
            os.remove(UPDATELOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_03_update_fail_conn_error(self):
        """Update project, filesystem and lun with wrong connection."""
        serverfile = os.path.join(SERVERDIR, 'fakeServer.yml')
        updatefile = os.path.join(CSVDIR, 'update_component.csv')
        listargs = Namespace(server=serverfile, file=updatefile,
                             progress=False, subparser_name='UPDATE',
                             timeout=2, cert=False)
        run_updates(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_04_update_fail_progress(self):
        """Update project, filesystem and lun with wrong connection & progress.
        """
        serverfile = os.path.join(SERVERDIR, 'fakeServer.yml')
        updatefile = os.path.join(CSVDIR, 'update_component.csv')
        listargs = Namespace(server=serverfile, file=updatefile,
                             progress=True, subparser_name='UPDATE',
                             timeout=2, cert=False)
        run_updates(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(UPDATELOGFILE))
        try:
            os.remove(UPDATELOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_05_update_fail(self):
        """Update project, filesystem and lun with wrong user."""
        serverfile = os.path.join(SERVERDIR, 'server_baduser.yml')
        updatefile = os.path.join(CSVDIR, 'update_component.csv')
        listargs = Namespace(server=serverfile, file=updatefile,
                             progress=False, subparser_name='UPDATE',
                             timeout=100, cert=False)
        run_updates(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())
