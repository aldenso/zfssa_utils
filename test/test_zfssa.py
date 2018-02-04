"""Test Common functions"""
import unittest
# import sys
import os
from zfssa_utils.common import read_yaml_file, read_csv_file, response_size,\
     get_real_size, get_real_blocksize

HERE = os.path.abspath(os.path.dirname(__file__))

LUNFILEOUTPUT = [['pool_0', 'unittest', 'lun01']]

YAMLOUTPUT = {'username': 'root',
              'ip': '192.168.56.150',
              'password': 'password'}


class TestCommon(unittest.TestCase):
    """Test common script functions"""

    def test_response_size(self):
        """Test response_size function to print human readable sizes"""
        self.assertEqual(response_size(10240), '10 KB')
        self.assertEqual(response_size(9437184), '9 MB')
        self.assertEqual(response_size(103809024), '99 MB')
        self.assertEqual(response_size(137438953472), '128 GB')
        self.assertEqual(response_size(140737488355), '131.07 GB')

    def test_read_yaml_file(self):
        """Test read_yaml_file function to read a regular yml file"""
        self.assertEqual(read_yaml_file(os.path.join(HERE, "serverOS86.yml")),
                         YAMLOUTPUT)

    @unittest.expectedFailure
    def test_read_yaml_file_fail(self):
        """Test read_yaml_file function to read a file not in yml format."""
        self.assertEqual(read_yaml_file(os.path.join(HERE,
                                                     "test_fs_snaps.csv")),
                         YAMLOUTPUT)

    def test_read_csv_file(self):
        """Test read_csv_file function to read a regular csv file"""
        self.assertEqual(read_csv_file(os.path.join(HERE,
                                                    "test_destroy_lun.csv")),
                         LUNFILEOUTPUT)

    @unittest.expectedFailure
    def test_read_csv_file_fail(self):
        """Test read_csv_file function to read a file not in csv format"""
        self.assertEqual(read_csv_file(os.path.join(HERE,
                                                    "serverOS86.yml")),
                         LUNFILEOUTPUT)

    def test_get_real_size(self):
        """Test get_real_size function to convert input sizes
        (integer and string) to integer"""
        self.assertEqual(get_real_size(3, 'kb'), 3072)
        self.assertEqual(get_real_size(3, 'Mb'), 3145728)
        self.assertEqual(get_real_size(3, 'gb'), 3221225472)
        self.assertEqual(get_real_size(3, 'tB'), 3298534883328)

    def test_get_real_blocksize(self):
        """Test get_real_blocksize function to convert a string to integer"""
        self.assertEqual(get_real_blocksize('512'), '512')
        self.assertEqual(get_real_blocksize('8K'), 8192)
        self.assertEqual(get_real_blocksize('128k'), 131072)
        self.assertEqual(get_real_blocksize('1M'), 1048576)


if __name__ == "__main__":
    unittest.main()
