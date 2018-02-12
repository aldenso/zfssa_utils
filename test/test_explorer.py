"""Test Explorer functions"""
import unittest
import sys
import os
import six
from zfssa_utils.explorer import run_explorer
# from zfssa_utils.common import urls_constructor

HERE = os.path.abspath(os.path.dirname(__file__))

DATASET = ['cluster',
           'problems',
           'datalinks',
           'version',
           'routing',
           'routes',
           'projects',
           'luns',
           'filesystems',
           'interfaces',
           'devices',
           'pools',
           'fc_initiators',
           'fc_initiator-groups',
           'fc_target-groups',
           'fc_targets',
           'iscsi_initiators',
           'iscsi_targets',
           'iscsi_initiator-groups',
           'iscsi_target-groups',
           'users']


class Namespace:
    """Class to simulate args parsed"""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestExplorer(unittest.TestCase):
    """Test Explorer generation."""

    def test_00_explorer(self):
        """Test explorer creation."""
        serverfile = os.path.join(HERE, 'serverOS86.yml')
        listargs = Namespace(server=serverfile, subparser_name='EXPLORER',
                             progress=False, timeout=100)
        run_explorer(listargs)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        output = sys.stdout.getvalue()
        print(output)
        item_list = [x.split(" ")[4] for x in output.splitlines()]
        DATASETCOPY = None
        if six.PY2:
            DATASETCOPY = DATASET[:]
        else:
            DATASETCOPY = DATASET.copy()
        for item in item_list:
            DATASETCOPY.remove(item)
        if DATASETCOPY:
            self.fail("Item list not complete.")
        try:
            for root, dirs, files in os.walk("data"):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.remove(os.path.join(root, name))
            os.removedirs("data")
        except Exception:
            self.fail("file created but unable to remove directory data.")
