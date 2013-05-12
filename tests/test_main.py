import unittest
import time
import datastore

"""
A collection of some basic tests for the datastore library.
"""


class TestMstore(unittest.TestCase):
    db = datastore.mstore()

    def test_mstore(self):
        """
        Tests mongo keystore
        """
        pi = 3.14
        self.db.set("pi", pi)
        returned = self.db.get("pi")
        self.assertEqual(pi, returned)

if __name__ == '__main__':
    unittest.main()
