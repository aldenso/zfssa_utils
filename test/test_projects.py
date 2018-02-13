"""Test Projects functions"""
import unittest
import sys
import os
from zfssa_utils.projects import run_projects
from zfssa_utils.common import PROJECTLOGFILE

HERE = os.path.abspath(os.path.dirname(__file__))
CSVDIR = os.path.join(HERE, "csvfiles")
SERVERDIR = os.path.join(HERE, "serverfiles")


class Namespace:
    """Class to simulate args parsed"""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestProjects(unittest.TestCase):
    """Test Projects functions"""

    def test_00_create_projects(self):
        """Create projects."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projcreatefile = os.path.join(CSVDIR, 'test_create_projects.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=False, timeout=100, cert=False)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_01_create_exists(self):
        """Create projects but fail trying, existing project."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projcreatefile = os.path.join(CSVDIR, 'test_create_projects.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=False, timeout=100, cert=False)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_02_create_fail_csv(self):
        """Create projects with wrong csv."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projcreatefile = os.path.join(CSVDIR, 'test_create_lun.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=False, timeout=100, cert=False)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_03_create_fail_conn_error(self):
        """Create projects with wrong connection."""
        serverfile = os.path.join(SERVERDIR, 'fakeServer.yml')
        projcreatefile = os.path.join(CSVDIR, 'test_create_projects.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=False, timeout=2, cert=False)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_04_create_fail_progress(self):
        """Create projects with wrong connection and progress."""
        serverfile = os.path.join(SERVERDIR, 'fakeServer.yml')
        projcreatefile = os.path.join(CSVDIR, 'test_create_projects.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=False, create=True, delete=False,
                             progress=True, subparser_name='PROJECTS',
                             noconfirm=False, timeout=2, cert=False)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(PROJECTLOGFILE))
        try:
            os.remove(PROJECTLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_05_list_projects(self):
        """List projects."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projcreatefile = os.path.join(CSVDIR, 'test_create_projects.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=False, timeout=100, cert=False)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('PRESENT' in sys.stdout.getvalue())

    def test_06_list_short_csv(self):
        """List projects with short csv."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projcreatefile = os.path.join(CSVDIR, 'test_destroy_projects.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=False, timeout=100, cert=False)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('PRESENT' in sys.stdout.getvalue())

    def test_07_list_fail_csv(self):
        """List projects with wrong csv."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projcreatefile = os.path.join(CSVDIR, 'test_destroy_fs.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=False, timeout=100, cert=False)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_08_list_fail_conn_error(self):
        """List projects with wrong connection."""
        serverfile = os.path.join(SERVERDIR, 'fakeServer.yml')
        projcreatefile = os.path.join(CSVDIR, 'test_destroy_fs.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=False, timeout=2, cert=False)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_09_list_fail_progress(self):
        """List projects with wrong connection and progress."""
        serverfile = os.path.join(SERVERDIR, 'fakeServer.yml')
        projcreatefile = os.path.join(CSVDIR, 'test_destroy_fs.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=True, subparser_name='PROJECTS',
                             noconfirm=False, timeout=2, cert=False)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(PROJECTLOGFILE))
        try:
            os.remove(PROJECTLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_10_delete_projects(self):
        """Delete projects."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projdestroyfile = os.path.join(CSVDIR, 'test_destroy_projects.csv')
        listargs = Namespace(server=serverfile, file=projdestroyfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=True, timeout=100, cert=False)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_11_delete_fail_csv(self):
        """Delete projects with with wrong csv"""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projdestroyfile = os.path.join(CSVDIR, 'test_destroy_fs.csv')
        listargs = Namespace(server=serverfile, file=projdestroyfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=True, timeout=100, cert=False)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_12_delete_fail_conn_error(self):
        """Delete projects with wrong connection."""
        serverfile = os.path.join(SERVERDIR, 'fakeServer.yml')
        projdestroyfile = os.path.join(CSVDIR, 'test_destroy_projects.csv')
        listargs = Namespace(server=serverfile, file=projdestroyfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=True, timeout=2, cert=False)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_13_delete_fail_progress(self):
        """Delete projects with wrong connection and progress."""
        serverfile = os.path.join(SERVERDIR, 'fakeServer.yml')
        projdestroyfile = os.path.join(CSVDIR, 'test_destroy_projects.csv')
        listargs = Namespace(server=serverfile, file=projdestroyfile,
                             list=False, create=False, delete=True,
                             progress=True, subparser_name='PROJECTS',
                             noconfirm=True, timeout=2, cert=False)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(PROJECTLOGFILE))
        try:
            os.remove(PROJECTLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_14_create_progress(self):
        """Create projects with progress."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projcreatefile = os.path.join(CSVDIR, 'test_create_projects.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=False, create=True, delete=False,
                             progress=True, subparser_name='PROJECTS',
                             noconfirm=False, timeout=100, cert=False)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(PROJECTLOGFILE))
        try:
            os.remove(PROJECTLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_15_list_progress(self):
        """List projects with progress."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projcreatefile = os.path.join(CSVDIR, 'test_create_projects.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=True, subparser_name='PROJECTS',
                             noconfirm=False, timeout=100, cert=False)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(PROJECTLOGFILE))
        try:
            os.remove(PROJECTLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_16_delete_progress(self):
        """Delete projects with progress."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projdestroyfile = os.path.join(CSVDIR, 'test_destroy_projects.csv')
        listargs = Namespace(server=serverfile, file=projdestroyfile,
                             list=False, create=False, delete=True,
                             progress=True, subparser_name='PROJECTS',
                             noconfirm=True, timeout=100, cert=False)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(PROJECTLOGFILE))
        try:
            os.remove(PROJECTLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")
