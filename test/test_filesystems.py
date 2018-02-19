"""Test Filesystems functions"""
import unittest
import sys
import os
from zfssa_utils.filesystems import run_filesystems
from zfssa_utils.common import FSLOGFILE

HERE = os.path.abspath(os.path.dirname(__file__))
CSVDIR = os.path.join(HERE, "csvfiles")
SERVERDIR = os.path.join(HERE, "serverfiles")


class Namespace:
    """Class to simulate args parsed"""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestFilesystems(unittest.TestCase):
    """Test Filesystems functions"""

    def test_00_create_filesystems(self):
        """Create filesystems."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        fscreatefile = os.path.join(CSVDIR, 'test_create_fs.csv')
        listargs = Namespace(server=serverfile, file=fscreatefile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='FILESYSTEMS',
                             noconfirm=False, timeout=100, cert=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_01_create_exists(self):
        """Create filesystems but fail trying, existing filesystem."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        fscreatefile = os.path.join(CSVDIR, 'test_create_fs.csv')
        listargs = Namespace(server=serverfile, file=fscreatefile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='FILESYSTEMS',
                             noconfirm=False, timeout=100, cert=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_02_create_fail_csv(self):
        """Create filesystems with wrong csv."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        fscreatefile = os.path.join(CSVDIR, 'test_create_lun.csv')
        listargs = Namespace(server=serverfile, file=fscreatefile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='FILESYSTEMS',
                             noconfirm=False, timeout=100, cert=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_03_create_fail_conn_error(self):
        """Create filesystems with wrong connection."""
        serverfile = os.path.join(SERVERDIR, 'fakeServer.yml')
        fscreatefile = os.path.join(CSVDIR, 'test_create_fs.csv')
        listargs = Namespace(server=serverfile, file=fscreatefile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='FILESYSTEMS',
                             noconfirm=False, timeout=2, cert=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_04_create_fail_progress(self):
        """Create filesystems with wrong connection and progress."""
        serverfile = os.path.join(SERVERDIR, 'fakeServer.yml')
        fscreatefile = os.path.join(CSVDIR, 'test_create_fs.csv')
        listargs = Namespace(server=serverfile, file=fscreatefile,
                             list=False, create=True, delete=False,
                             progress=True, subparser_name='FILESYSTEMS',
                             noconfirm=False, timeout=2, cert=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(FSLOGFILE))
        try:
            os.remove(FSLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_05_list_filesystems(self):
        """List filesystems."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        fscreatefile = os.path.join(CSVDIR, 'test_create_fs.csv')
        listargs = Namespace(server=serverfile, file=fscreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='FILESYSTEMS',
                             noconfirm=False, timeout=100, cert=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_06_list_short_csv(self):
        """List filesystems with short csv."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        fscreatefile = os.path.join(CSVDIR, 'test_destroy_fs.csv')
        listargs = Namespace(server=serverfile, file=fscreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='FILESYSTEMS',
                             noconfirm=False, timeout=100, cert=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_07_list_fail_csv(self):
        """List filesystems with wrong csv."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        fscreatefile = os.path.join(CSVDIR, 'test_create_lun.csv')
        listargs = Namespace(server=serverfile, file=fscreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='FILESYSTEMS',
                             noconfirm=False, timeout=100, cert=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_08_list_fail_conn_error(self):
        """List filesystems with wrong connection."""
        serverfile = os.path.join(SERVERDIR, 'fakeServer.yml')
        fscreatefile = os.path.join(CSVDIR, 'test_destroy_fs.csv')
        listargs = Namespace(server=serverfile, file=fscreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='FILESYSTEMS',
                             noconfirm=False, timeout=2, cert=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_09_list_fail_progress(self):
        """List filesystems with wrong connection and progress."""
        serverfile = os.path.join(SERVERDIR, 'fakeServer.yml')
        fscreatefile = os.path.join(CSVDIR, 'test_destroy_fs.csv')
        listargs = Namespace(server=serverfile, file=fscreatefile,
                             list=True, create=False, delete=False,
                             progress=True, subparser_name='FILESYSTEMS',
                             noconfirm=False, timeout=2, cert=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(FSLOGFILE))
        try:
            os.remove(FSLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_10_delete_filesystems(self):
        """Delete filesystems."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        fsdestroyfile = os.path.join(CSVDIR, 'test_destroy_fs.csv')
        listargs = Namespace(server=serverfile, file=fsdestroyfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='FILESYSTEMS',
                             noconfirm=True, timeout=100, cert=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_11_delete_fail_csv(self):
        """Delete filesystems with wrong csv."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        fsdestroyfile = os.path.join(CSVDIR, 'test_create_lun.csv')
        listargs = Namespace(server=serverfile, file=fsdestroyfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='FILESYSTEMS',
                             noconfirm=True, timeout=100, cert=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_12_delete_fail_conn_error(self):
        """Delete filesystems with wrong connection."""
        serverfile = os.path.join(SERVERDIR, 'fakeServer.yml')
        fsdestroyfile = os.path.join(CSVDIR, 'test_destroy_fs.csv')
        listargs = Namespace(server=serverfile, file=fsdestroyfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='FILESYSTEMS',
                             noconfirm=True, timeout=2, cert=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_13_delete_fail_progress(self):
        """Delete filesystems with wrong connection and progress."""
        serverfile = os.path.join(SERVERDIR, 'fakeServer.yml')
        fsdestroyfile = os.path.join(CSVDIR, 'test_destroy_fs.csv')
        listargs = Namespace(server=serverfile, file=fsdestroyfile,
                             list=False, create=False, delete=True,
                             progress=True, subparser_name='FILESYSTEMS',
                             noconfirm=True, timeout=2, cert=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(FSLOGFILE))
        try:
            os.remove(FSLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_14_create_progress(self):
        """Create filesystems with progress."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        fscreatefile = os.path.join(CSVDIR, 'test_create_fs.csv')
        listargs = Namespace(server=serverfile, file=fscreatefile,
                             list=False, create=True, delete=False,
                             progress=True, subparser_name='FILESYSTEMS',
                             noconfirm=False, timeout=100, cert=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(FSLOGFILE))
        try:
            os.remove(FSLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_15_list_progress(self):
        """List filesystems with progress."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        fscreatefile = os.path.join(CSVDIR, 'test_create_fs.csv')
        listargs = Namespace(server=serverfile, file=fscreatefile,
                             list=True, create=False, delete=False,
                             progress=True, subparser_name='FILESYSTEMS',
                             noconfirm=False, timeout=100, cert=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(FSLOGFILE))
        try:
            os.remove(FSLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_16_delete_progress(self):
        """Delete filesystems with progress."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        fsdestroyfile = os.path.join(CSVDIR, 'test_destroy_fs.csv')
        listargs = Namespace(server=serverfile, file=fsdestroyfile,
                             list=False, create=False, delete=True,
                             progress=True, subparser_name='FILESYSTEMS',
                             noconfirm=True, timeout=100, cert=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(FSLOGFILE))
        try:
            os.remove(FSLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")
