"""Test templates functions"""
import unittest
import sys
import os
from zfssa_utils.templates import write_file, create_template


class Namespace:
    """Class to simulate args parsed"""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestTemplates(unittest.TestCase):
    """Test LUNs functions"""

    def test_00_write_files(self):
        """Write file."""
        filename = "test_file"
        data = "some line to write\nand test the function.\n"
        write_file(filename, data)
        try:
            with open(filename, 'r') as file:
                content = file.read()
                self.assertEqual(data, content)
        except Exception:
            self.fail("Failed to read file.")
        try:
            os.remove(filename)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_01_write_existing(self):
        """Write a file that already exists."""
        filename = "test_file"
        data = "some line to write\nand test the function.\n"
        try:
            with open(filename, "w") as file:
                file.write(data)
        except Exception as err:
            print("Not able to create file: '{}'".format(err))

        with self.assertRaises(SystemExit) as cm:
            write_file(filename, data)
        self.assertTrue('already exists' in cm.exception.code)

        try:
            os.remove(filename)
        except Exception:
            self.fail("file created but unable to remove.")

    def test_02_write_fail(self):
        """Write a file with a non existent directory."""
        nodir = "unknown"
        filename = "test_file"
        data = "some line to write\nand test the function.\n"
        write_file(os.path.join(nodir, filename), data)
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        self.assertTrue('Not able' in sys.stdout.getvalue())
