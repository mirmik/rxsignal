import unittest
import rxsignal


class OperatorTest(unittest.TestCase):
    def test_buffer(self):
        a = rxsignal.from_iterable([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        b = a.buffer_with_count(3)
        self.assertEqual(b.to_list(), [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]])
