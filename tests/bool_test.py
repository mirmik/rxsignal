import unittest

from numpy import False_
import rxsignal


class BoolTest(unittest.TestCase):
    def test_bool(self):
        a = rxsignal.from_iterable([True, False, False])
        b = rxsignal.from_iterable([True, True, False])
        c = rxsignal.from_iterable([True, True, False])
        d = rxsignal.rxall(a, b, c)
        e = rxsignal.rxany(a, b, c)
        self.assertEqual(d.to_list(), [True, False, False])
        self.assertEqual(e.to_list(), [True, True, False])
