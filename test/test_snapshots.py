"""Test Snapshots functions"""
import unittest
import sys
import os
from zfssa_utils.snapshots import run_snaps

HERE = os.path.abspath(os.path.dirname(__file__))

PROJSNAPFILE = "test_project_snaps.csv"
FSSNAPFILE = "test_fs_snaps.csv"
LUNSNAPFILE = "test_lun_snaps.csv"


class Namespace:
    """Class to simulate args parsed"""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestSnapshots(unittest.TestCase):
    """Test Snapshots functions"""

    def test_00_create_snap_project(self):
        """Test snapshots with arguments to create a project snap."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projsnapfile = os.path.join(HERE, PROJSNAPFILE)
        listargs = Namespace(server=serverfile, file=projsnapfile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='SNAPSHOTS',
                             noconfirm=False, timeout=100)
        run_snaps(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_01_list_snap_project(self):
        """Test snapshots with arguments to list/show a project snap."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projcreatefile = os.path.join(HERE, PROJSNAPFILE)
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='SNAPSHOTS',
                             noconfirm=False, timeout=100)
        run_snaps(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('PRESENT' in sys.stdout.getvalue())

    def test_02_delete_snap_projects(self):
        """Test snapshots with arguments to delete a project snap."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projdestroyfile = os.path.join(HERE, PROJSNAPFILE)
        listargs = Namespace(server=serverfile, file=projdestroyfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='SNAPSHOTS',
                             noconfirm=True, timeout=100)
        run_snaps(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_03_create_snap_filesystem(self):
        """Test snapshots with arguments to create a filesystem snap."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projsnapfile = os.path.join(HERE, FSSNAPFILE)
        listargs = Namespace(server=serverfile, file=projsnapfile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='SNAPSHOTS',
                             noconfirm=False, timeout=100)
        run_snaps(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_04_list_snap_filesystem(self):
        """Test snapshots with arguments to list/show a filesystem snap."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projcreatefile = os.path.join(HERE, FSSNAPFILE)
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='SNAPSHOTS',
                             noconfirm=False, timeout=100)
        run_snaps(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('PRESENT' in sys.stdout.getvalue())

    def test_05_delete_snap_filesystem(self):
        """Test snapshots with arguments to delete a filesystem snap."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projdestroyfile = os.path.join(HERE, FSSNAPFILE)
        listargs = Namespace(server=serverfile, file=projdestroyfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='SNAPSHOTS',
                             noconfirm=True, timeout=100)
        run_snaps(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_06_create_snap_lun(self):
        """Test snapshots with arguments to create a lun snap."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projsnapfile = os.path.join(HERE, LUNSNAPFILE)
        listargs = Namespace(server=serverfile, file=projsnapfile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='SNAPSHOTS',
                             noconfirm=False, timeout=100)
        run_snaps(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_07_list_snap_lun(self):
        """Test snapshots with arguments to list/show a lun snap."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projcreatefile = os.path.join(HERE, LUNSNAPFILE)
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='SNAPSHOTS',
                             noconfirm=False, timeout=100)
        run_snaps(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('PRESENT' in sys.stdout.getvalue())

    def test_08_delete_snap_lun(self):
        """Test snapshots with arguments to delete a lun snap."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projdestroyfile = os.path.join(HERE, LUNSNAPFILE)
        listargs = Namespace(server=serverfile, file=projdestroyfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='SNAPSHOTS',
                             noconfirm=True, timeout=100)
        run_snaps(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())
