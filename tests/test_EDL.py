# -*- coding: utf-8 -*-
import os
import sys
import unittest
from itertools import izip_longest
from edl import EDL


class EDLTestCase(unittest.TestCase):
    """tests the edl.edl.List class
    """

    def test_init_valid_fps(self):
        def verify_valid_framerate(fps_):
            try:
                edl = EDL(fps_)
            except (TypeError, ValueError), e:
                self.fail("Valid value {} raised {} on init".format(fps_, e.__class__.__name__))
            self.assertIsInstance(edl, EDL)
            if isinstance(fps_, basestring):
                # No try/except here; we expect this value to be valid.
                fps_ = float(fps_)
            if isinstance(fps_, float):
                self.assertEqual(edl.fps, str(int(fps_)) if fps_.is_integer() else str(fps_))
            else:
                self.assertEqual(edl.fps, str(fps_))

        # Test valid integer framerates
        for fps in [24, 25, 30, 50, 60]:
            verify_valid_framerate(fps)

        # Test valid float framerates
        for fps in [23.98, 24.0, 25.00, 29.97, 30.000, 50.0, 59.94, 60.00000000]:
            verify_valid_framerate(fps)

        # Test valid string framerates
        for fps in ['23.98', '23.980', '24', '24.0', '25', '25.00', '29.97', '30', '30.0', '50',
                    '50.00', '59.94', '59.94000', '60', '60.000000']:
            verify_valid_framerate(fps)

        # Test valid unicode framerates
        for fps in [u'23.98', u'23.980', u'24', u'24.0', u'25', u'25.00', u'29.97', u'30', u'30.0', u'50',
                    u'50.00', u'59.94', u'59.94000', u'60', u'60.000000']:
            verify_valid_framerate(fps)

    def test_init_invalid_fps(self):
        def verify_invalid_framerate(fps_):
            if isinstance(fps_, (basestring, int, float)):
                expected_exc = ValueError
            else:
                expected_exc = TypeError

            self.assertRaises(expected_exc, EDL, fps_)

        # Test invalid integer framerates
        for fps in [-sys.maxint - 1, 100, -1, 0, 1, 23, 26, 29, 31, 49, 51, 59, 61, sys.maxint]:
            verify_invalid_framerate(fps)

        # Test invalid float framerates
        for fps in [-100000000.00, -123463.34532, -.0000001, .00004, 23.979999999, 23.99999999,
                    59.9399999999, 1000.2341234, 12349082341234]:
            verify_invalid_framerate(fps)

        # Test invalid string framerates
        for fps in ['not_a_number', '-205.0', '24.0.1', '23.9800000001', '239485029345680']:
            verify_invalid_framerate(fps)

        # Test invalid unicode framerates
        for fps in [u'not_a_number', u'-205.0', u'24.0.1', u'23.9800000001', u'239485029345680']:
            verify_invalid_framerate(fps)

        # Test invalid types
        for fps in [None, ['24'], (29.97, 30), {'fps': 30}]:
            verify_invalid_framerate(fps)

    def test_output_matches_input(self):
        """testing if to_string will output the EDL as string
        """
        for test_file in ['test_24.edl', 'test.edl', 'test_50.edl']:
            test_fpath = os.path.join("..", "tests", "test_data", test_file)
            with open(test_fpath) as f:
                expected_edl = [line.rstrip('\n') for line in f.readlines()]
            actual_edl = EDL.from_file(24, test_fpath)

            # Remove blank lines, since they don't affect data content
            expected_edl = [line for line in expected_edl if line]
            actual_edl = [str(statement) for statement in actual_edl if statement]

            self.maxDiff = None

            self.assertEqual(len(expected_edl), len(actual_edl),
                             "Generated EDL has the same number of data lines as original EDL.")

            for expected, actual in izip_longest(expected_edl, actual_edl):
                # Remove extraneous whitespace to prevent false negatives
                expected = " ".join(expected.split())
                actual = " ".join(actual.split())

                self.assertEqual(expected, actual, "Generated EDL line is the same as original EDL line.")
