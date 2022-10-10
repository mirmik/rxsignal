import unittest
import rxsignal


class MathTest(unittest.TestCase):
    def test_sum(self):
        a = rxsignal.from_iterable([1, 2, 3])
        b = rxsignal.from_iterable([4, 5, 6])
        c = a + b
        self.assertEqual(c.to_list(), [5, 7, 9])

    def test_sum_with_constant(self):
        a = rxsignal.from_iterable([1, 2, 3])
        b = 4
        c = a + b
        self.assertEqual(c.to_list(), [5, 6, 7])

    def test_sum_with_constant2(self):
        a = 4
        b = rxsignal.from_iterable([1, 2, 3])
        c = 8
        d = a + b + c
        self.assertEqual(d.to_list(), [13, 14, 15])

    def test_mul(self):
        a = rxsignal.from_iterable([1, 2, 3])
        b = rxsignal.from_iterable([4, 5, 6])
        c = a * b
        self.assertEqual(c.to_list(), [4, 10, 18])

    def test_mul_with_constant(self):
        a = rxsignal.from_iterable([1, 2, 3])
        b = 4
        c = a * b
        self.assertEqual(c.to_list(), [4, 8, 12])

    def test_div(self):
        a = rxsignal.from_iterable([1, 2, 3])
        b = rxsignal.from_iterable([4, 5, 6])
        c = a / b
        self.assertEqual(c.to_list(), [0.25, 0.4, 0.5])

    def test_sub_with_constant_1(self):
        a = rxsignal.from_iterable([1, 2, 3])
        b = 4
        c = a - b
        self.assertEqual(c.to_list(), [-3, -2, -1])

    def test_sub_with_constant_2(self):
        a = 4
        b = rxsignal.from_iterable([1, 2, 3])
        c = a - b
        self.assertEqual(c.to_list(), [3, 2, 1])
