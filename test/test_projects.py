"""Test Projects functions"""
import unittest
import sys
import os
from zfssa_utils.projects import run_projects

HERE = os.path.abspath(os.path.dirname(__file__))


class Namespace:
    """Class to simulate args parsed"""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestProjects(unittest.TestCase):
    """Test Projects functions"""

    def test_00_create_projects(self):
        """Test projects with arguments to use create_projects function"""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projcreatefile = os.path.join(HERE, 'test_create_projects.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=False, create=True, delete=False,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=False, timeout=100)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())

    def test_01_list_projects(self):
        """Test projects with arguments to use list_projects function"""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projcreatefile = os.path.join(HERE, 'test_create_projects.csv')
        listargs = Namespace(server=serverfile, file=projcreatefile,
                             list=True, create=False, delete=False,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=False, timeout=100)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue('PRESENT' in sys.stdout.getvalue())

    def test_02_delete_projects(self):
        """Test projects with arguments to use delete_projects function"""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        projdestroyfile = os.path.join(HERE, 'test_destroy_projects.csv')
        listargs = Namespace(server=serverfile, file=projdestroyfile,
                             list=False, create=False, delete=True,
                             progress=False, subparser_name='PROJECTS',
                             noconfirm=True, timeout=100)
        run_projects(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue('SUCCESS' in sys.stdout.getvalue())
