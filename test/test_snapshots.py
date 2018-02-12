"""Test Snapshots functions"""
import unittest
import sys
import os
from zfssa_utils.snapshots import run_snaps

HERE = os.path.abspath(os.path.dirname(__file__))
CSVDIR = os.path.join(HERE, "csvfiles")
SERVERDIR = os.path.join(HERE, "serverfiles")

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
        """Create project snapshots."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projsnapfile = os.path.join(CSVDIR, PROJSNAPFILE)
        listargs = Namespace(server=serverfile, file=projsnapfile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='SNAPSHOTS',
                             noconfirm=False, timeout=100)
        run_snaps(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_01_list_snap_project(self):
        """List/Show project snapshots."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projcreatefile = os.path.join(CSVDIR, PROJSNAPFILE)
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='SNAPSHOTS',
                             noconfirm=False, timeout=100)
        run_snaps(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('PRESENT' in sys.stdout.getvalue())

    def test_02_delete_snap_projects(self):
        """Delete project snapshots."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projdestroyfile = os.path.join(CSVDIR, PROJSNAPFILE)
        listargs = Namespace(server=serverfile, file=projdestroyfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='SNAPSHOTS',
                             noconfirm=True, timeout=100)
        run_snaps(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_03_create_snap_filesystem(self):
        """Create filesystem snapshots."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projsnapfile = os.path.join(CSVDIR, FSSNAPFILE)
        listargs = Namespace(server=serverfile, file=projsnapfile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='SNAPSHOTS',
                             noconfirm=False, timeout=100)
        run_snaps(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_04_list_snap_filesystem(self):
        """List/Show filesystem snapshots."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projcreatefile = os.path.join(CSVDIR, FSSNAPFILE)
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='SNAPSHOTS',
                             noconfirm=False, timeout=100)
        run_snaps(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('PRESENT' in sys.stdout.getvalue())

    def test_05_delete_snap_filesystem(self):
        """Delete filesystem snapshots."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projdestroyfile = os.path.join(CSVDIR, FSSNAPFILE)
        listargs = Namespace(server=serverfile, file=projdestroyfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='SNAPSHOTS',
                             noconfirm=True, timeout=100)
        run_snaps(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_06_create_snap_lun(self):
        """Create lun snapshots."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projsnapfile = os.path.join(CSVDIR, LUNSNAPFILE)
        listargs = Namespace(server=serverfile, file=projsnapfile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='SNAPSHOTS',
                             noconfirm=False, timeout=100)
        run_snaps(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_07_list_snap_lun(self):
        """List/Show lun snapshots."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projcreatefile = os.path.join(CSVDIR, LUNSNAPFILE)
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='SNAPSHOTS',
                             noconfirm=False, timeout=100)
        run_snaps(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('PRESENT' in sys.stdout.getvalue())

    def test_08_delete_snap_lun(self):
        """Delete lun snapshots."""
        serverfile = os.path.join(SERVERDIR, 'serverOS86.yml')
        projdestroyfile = os.path.join(CSVDIR, LUNSNAPFILE)
        listargs = Namespace(server=serverfile, file=projdestroyfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='SNAPSHOTS',
                             noconfirm=True, timeout=100)
        run_snaps(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())
