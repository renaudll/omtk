import unittest
import pymel.core as pymel

class TestCase(unittest.TestCase):
    def test_simple(self):
        pymel.createNode('transform')
