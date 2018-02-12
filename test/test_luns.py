"""Test LUNs functions"""
import unittest
import sys
import os
from zfssa_utils.luns import run_luns
from zfssa_utils.common import LUNLOGFILE

HERE = os.path.abspath(os.path.dirname(__file__))


class Namespace:
    """Class to simulate args parsed"""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestLUNS(unittest.TestCase):
    """Test LUNs functions"""

    def test_00_create_lun(self):
        """Create luns."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        lunscreatefile = os.path.join(HERE, 'test_create_lun.csv')
        listargs = Namespace(server=serverfile, file=lunscreatefile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='LUNS',
                             noconfirm=False, timeout=100)
        run_luns(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_01_create_lun_exists(self):
        """Create luns but fail trying, existing lun."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        lunscreatefile = os.path.join(HERE, 'test_create_lun.csv')
        listargs = Namespace(server=serverfile, file=lunscreatefile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='LUNS',
                             noconfirm=False, timeout=100)
        run_luns(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_02_create_fail_csv(self):
        """Create luns with wrong csv."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        lunswrongfile = os.path.join(HERE, 'test_create_fs.csv')
        listargs = Namespace(server=serverfile, file=lunswrongfile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='LUNS',
                             noconfirm=False, timeout=100)
        run_luns(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_03_create_fail_conn_error(self):
        """Create luns with wrong connection."""
        serverfile = os.path.join(HERE, 'fakeServer.yml')
        lunscreatefile = os.path.join(HERE, 'test_create_lun.csv')
        listargs = Namespace(server=serverfile, file=lunscreatefile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='LUNS',
                             noconfirm=False, timeout=2)
        run_luns(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_04_create_fail_progress(self):
        """Create luns with wrong connection and progress."""
        serverfile = os.path.join(HERE, 'fakeServer.yml')
        lunscreatefile = os.path.join(HERE, 'test_create_lun.csv')
        listargs = Namespace(server=serverfile, file=lunscreatefile,
                             list=False, create=True, delete=False,
                             progress=True, subparser_name='LUNS',
                             noconfirm=False, timeout=2)
        run_luns(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue(os.path.exists(LUNLOGFILE))
        try:
            os.remove(LUNLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_05_list_lun(self):
        """List luns."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        lunscreatefile = os.path.join(HERE, 'test_create_lun.csv')
        listargs = Namespace(server=serverfile, file=lunscreatefile, list=True,
                             create=False, delete=False, progress=False,
                             subparser_name='LUNS', noconfirm=False,
                             timeout=100)
        run_luns(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue('PRESENT' in sys.stdout.getvalue())

    def test_06_list_lun_short_csv(self):
        """List luns with short csv."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        lunsdestroyfile = os.path.join(HERE, 'test_destroy_lun.csv')
        listargs = Namespace(server=serverfile, file=lunsdestroyfile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='LUNS',
                             noconfirm=False, timeout=100)
        run_luns(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue('PRESENT' in sys.stdout.getvalue())

    def test_07_list_fail_csv(self):
        """List luns with wrong csv."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        lunswrongfile = os.path.join(HERE, 'test_create_fs.csv')
        listargs = Namespace(server=serverfile, file=lunswrongfile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='LUNS',
                             noconfirm=False, timeout=100)
        run_luns(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_08_list_fail_conn_error(self):
        """List luns with wrong connection."""
        serverfile = os.path.join(HERE, 'fakeServer.yml')
        lunscreatefile = os.path.join(HERE, 'test_create_lun.csv')
        listargs = Namespace(server=serverfile, file=lunscreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='LUNS',
                             noconfirm=False, timeout=2)
        run_luns(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_09_list_fail_progress(self):
        """List luns with wrong connection and progress."""
        serverfile = os.path.join(HERE, 'fakeServer.yml')
        lunscreatefile = os.path.join(HERE, 'test_create_lun.csv')
        listargs = Namespace(server=serverfile, file=lunscreatefile,
                             list=True, create=False, delete=False,
                             progress=True, subparser_name='LUNS',
                             noconfirm=False, timeout=2)
        run_luns(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue(os.path.exists(LUNLOGFILE))
        try:
            os.remove(LUNLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_10_delete_lun(self):
        """Delete luns."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        lunsdestroyfile = os.path.join(HERE, 'test_destroy_lun.csv')
        deleteargs = Namespace(server=serverfile, file=lunsdestroyfile,
                               list=False, create=False, delete=True,
                               progress=False, subparser_name='LUNS',
                               noconfirm=True, timeout=100)
        run_luns(deleteargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_11_delete_fail_csv(self):
        """Delete luns with wrong csv."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        lunswrongfile = os.path.join(HERE, 'test_create_fs.csv')
        listargs = Namespace(server=serverfile, file=lunswrongfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='LUNS',
                             noconfirm=True, timeout=100)
        run_luns(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_12_delete_fail_conn_error(self):
        """Delete luns with wrong connection."""
        serverfile = os.path.join(HERE, 'fakeServer.yml')
        lunsdestroyfile = os.path.join(HERE, 'test_destroy_lun.csv')
        listargs = Namespace(server=serverfile, file=lunsdestroyfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='LUNS',
                             noconfirm=True, timeout=2)
        run_luns(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_13_delete_fail_progress(self):
        """Delete luns with wrong connection and progress."""
        serverfile = os.path.join(HERE, 'fakeServer.yml')
        lunsdestroyfile = os.path.join(HERE, 'test_destroy_lun.csv')
        listargs = Namespace(server=serverfile, file=lunsdestroyfile,
                             list=False, create=False, delete=True,
                             progress=True, subparser_name='LUNS',
                             noconfirm=True, timeout=2)
        run_luns(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue(os.path.exists(LUNLOGFILE))
        try:
            os.remove(LUNLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_14_create_progress(self):
        """Create luns with progress."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        lunscreatefile = os.path.join(HERE, 'test_create_lun.csv')
        listargs = Namespace(server=serverfile, file=lunscreatefile,
                             list=False, create=True, delete=False,
                             progress=True, subparser_name='LUNS',
                             noconfirm=False, timeout=100)
        run_luns(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue(os.path.exists(LUNLOGFILE))
        try:
            os.remove(LUNLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_15_list_progress(self):
        """List luns with progress."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        lunscreatefile = os.path.join(HERE, 'test_create_lun.csv')
        listargs = Namespace(server=serverfile, file=lunscreatefile,
                             list=True, create=False, delete=False,
                             progress=True, subparser_name='LUNS',
                             noconfirm=False, timeout=100)
        run_luns(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue(os.path.exists(LUNLOGFILE))
        try:
            os.remove(LUNLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_16_delete_progress(self):
        """Delete luns with progress."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        lunsdestroyfile = os.path.join(HERE, 'test_destroy_lun.csv')
        listargs = Namespace(server=serverfile, file=lunsdestroyfile,
                             list=False, create=False, delete=True,
                             progress=True, subparser_name='LUNS',
                             noconfirm=True, timeout=100)
        run_luns(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue(os.path.exists(LUNLOGFILE))
        try:
            os.remove(LUNLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")
