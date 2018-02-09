"""Test Projects functions"""
import unittest
import sys
import os
from zfssa_utils.projects import run_projects
from zfssa_utils.common import PROJECTLOGFILE

HERE = os.path.abspath(os.path.dirname(__file__))


class Namespace:
    """Class to simulate args parsed"""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestProjects(unittest.TestCase):
    """Test Projects functions"""

    def test_00_create_projects(self):
        """Test create projects."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projcreatefile = os.path.join(HERE, 'test_create_projects.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=False, timeout=100)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_01_create_exists(self):
        """Test create projects to fail to create an existing projects."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projcreatefile = os.path.join(HERE, 'test_create_projects.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=False, timeout=100)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_02_create_fail_csv(self):
        """Test create projects with wrong csv"""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projcreatefile = os.path.join(HERE, 'test_create_lun.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=False, timeout=100)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_03_create_fail_conn_error(self):
        """Test create projects with wrong connection"""
        serverfile = os.path.join(HERE, 'fakeServer.yml')
        projcreatefile = os.path.join(HERE, 'test_create_projects.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=False, timeout=2)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_04_create_fail_progress(self):
        """Test create projects with wrong connection and progress"""
        serverfile = os.path.join(HERE, 'fakeServer.yml')
        projcreatefile = os.path.join(HERE, 'test_create_projects.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=False, create=True, delete=False,
                             progress=True, subparser_name='PROJECTS',
                             noconfirm=False, timeout=2)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(PROJECTLOGFILE))
        try:
            os.remove(PROJECTLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_05_list_projects(self):
        """Test list projects."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projcreatefile = os.path.join(HERE, 'test_create_projects.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=False, timeout=100)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('PRESENT' in sys.stdout.getvalue())

    def test_06_list_short_csv(self):
        """Test list projects with short csv."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projcreatefile = os.path.join(HERE, 'test_destroy_projects.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=False, timeout=100)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('PRESENT' in sys.stdout.getvalue())

    def test_07_list_fail_csv(self):
        """Test list projects with short csv."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projcreatefile = os.path.join(HERE, 'test_destroy_fs.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=False, timeout=100)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_08_list_fail_conn_error(self):
        """Test list projects with wrong connection."""
        serverfile = os.path.join(HERE, 'fakeServer.yml')
        projcreatefile = os.path.join(HERE, 'test_destroy_fs.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=False, timeout=2)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_09_list_fail_progress(self):
        """Test list projects with wrong connection and progress."""
        serverfile = os.path.join(HERE, 'fakeServer.yml')
        projcreatefile = os.path.join(HERE, 'test_destroy_fs.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=True, subparser_name='PROJECTS',
                             noconfirm=False, timeout=2)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(PROJECTLOGFILE))
        try:
            os.remove(PROJECTLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_10_delete_projects(self):
        """Test delete projects."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projdestroyfile = os.path.join(HERE, 'test_destroy_projects.csv')
        listargs = Namespace(server=serverfile, file=projdestroyfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=True, timeout=100)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_11_delete_fail_csv(self):
        """Test delete projects with with wrong csv"""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projdestroyfile = os.path.join(HERE, 'test_destroy_fs.csv')
        listargs = Namespace(server=serverfile, file=projdestroyfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=True, timeout=100)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_12_delete_fail_conn_error(self):
        """Test delete projects with wrong connection."""
        serverfile = os.path.join(HERE, 'fakeServer.yml')
        projdestroyfile = os.path.join(HERE, 'test_destroy_projects.csv')
        listargs = Namespace(server=serverfile, file=projdestroyfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=True, timeout=2)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('FAIL' in sys.stdout.getvalue())

    def test_13_delete_fail_progress(self):
        """Test delete projects with wrong connection and progress"""
        serverfile = os.path.join(HERE, 'fakeServer.yml')
        projdestroyfile = os.path.join(HERE, 'test_destroy_projects.csv')
        listargs = Namespace(server=serverfile, file=projdestroyfile,
                             list=False, create=False, delete=True,
                             progress=True, subparser_name='PROJECTS',
                             noconfirm=True, timeout=2)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(PROJECTLOGFILE))
        try:
            os.remove(PROJECTLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_14_create_progress(self):
        """Test create projects with progress."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projcreatefile = os.path.join(HERE, 'test_create_projects.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=False, create=True, delete=False,
                             progress=True, subparser_name='PROJECTS',
                             noconfirm=False, timeout=100)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(PROJECTLOGFILE))
        try:
            os.remove(PROJECTLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_15_list_progress(self):
        """Test list projects with progress."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projcreatefile = os.path.join(HERE, 'test_create_projects.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=True, subparser_name='PROJECTS',
                             noconfirm=False, timeout=100)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(PROJECTLOGFILE))
        try:
            os.remove(PROJECTLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_16_delete_progress(self):
        """Test delete projects with progress."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projdestroyfile = os.path.join(HERE, 'test_destroy_projects.csv')
        listargs = Namespace(server=serverfile, file=projdestroyfile,
                             list=False, create=False, delete=True,
                             progress=True, subparser_name='PROJECTS',
                             noconfirm=True, timeout=100)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue(os.path.exists(PROJECTLOGFILE))
        try:
            os.remove(PROJECTLOGFILE)
        except Exception:
            self.fail("file created but unable to remove.")
