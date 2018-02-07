"""Test LUNs functions"""
import unittest
import sys
import os
from zfssa_utils.luns import run_luns

HERE = os.path.abspath(os.path.dirname(__file__))


class Namespace:
    """Class to simulate args parsed"""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestLUNS(unittest.TestCase):
    """Test LUNs functions"""

    def test_00_create_lun(self):
        """Test luns with arguments to use create_lun function"""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        lunscreatefile = os.path.join(HERE, 'test_create_lun.csv')
        listargs = Namespace(server=serverfile, file=lunscreatefile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='LUNS',
                             noconfirm=False)
        run_luns(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_01_list_lun(self):
        """Test luns with arguments to use list_lun function"""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        lunscreatefile = os.path.join(HERE, 'test_create_lun.csv')
        listargs = Namespace(server=serverfile, file=lunscreatefile, list=True,
                             create=False, delete=False, progress=False,
                             subparser_name='LUNS', noconfirm=False)
        run_luns(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue('PRESENT' in sys.stdout.getvalue())

    def test_02_delete_lun(self):
        """Test luns with arguments to use delete_lun function"""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        lunsdestroyfile = os.path.join(HERE, 'test_destroy_lun.csv')
        deleteargs = Namespace(server=serverfile, file=lunsdestroyfile,
                               list=False, create=False, delete=True,
                               progress=False, subparser_name='LUNS',
                               noconfirm=True)
        run_luns(deleteargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())
