"""Test Filesystems functions"""
import unittest
import sys
import os
from zfssa_utils.filesystems import run_filesystems

HERE = os.path.abspath(os.path.dirname(__file__))


class Namespace:
    """Class to simulate args parsed"""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestFilesystems(unittest.TestCase):
    """Test Filesystems functions"""

    def test_00_create_filesystems(self):
        """Test filesystems with args to use create_filesystems function"""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        fscreatefile = os.path.join(HERE, 'test_create_fs.csv')
        listargs = Namespace(server=serverfile, file=fscreatefile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='FILESYSTEMS',
                             noconfirm=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_01_list_filesystems(self):
        """Test filesystems with args to use list_filesystems function"""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        fscreatefile = os.path.join(HERE, 'test_create_fs.csv')
        listargs = Namespace(server=serverfile, file=fscreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='FILESYSTEMS',
                             noconfirm=False)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('PRESENT' in sys.stdout.getvalue())

    def test_02_delete_filesystems(self):
        """Test filesystems with args to use delete_filesystems function"""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        fsdestroyfile = os.path.join(HERE, 'test_destroy_fs.csv')
        listargs = Namespace(server=serverfile, file=fsdestroyfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='FILESYSTEMS',
                             noconfirm=True)
        run_filesystems(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("needs to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())
