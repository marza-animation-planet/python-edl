#!/usr/bin/python
"""
Module EDL
unit test suite
"""

import unittest
from edl import EDL


class ParserTestCase(unittest.TestCase):
    """tests the Parser
    """
    # ToDo: Test both file and text parsing.
    # ToDo: Merge test_EDL and test_parser files.

    def test_24fps(self):
        s = EDL.from_file(24, '../tests/test_data/test_24.edl')

        # self.assertEqual(s.events[0].clip_name, 'clip 1',
        #                  'Failed clip name test')
        # self.assertEqual(s.events[0].src_length(), 1440,
        #                  'Wrong source frame length')
        # self.assertEqual(s.events[0].rec_length(), 1440,
        #                  'Wrong record frame length')
        # self.assertEqual(s.events[0].src_end_tc.frame_number, 87840,
        #                  'Wrong source end timecode')
        # self.assertEqual(s.events[0].rec_start_tc.frame_number, 0,
        #                  'Wrong record start timecode')
        # self.assertEqual(s.events[0].rec_end_tc.frame_number, 1440,
        #                  'Wrong record end timecode')
        # self.assertEqual(s.events[1].clip_name, 'clip #2',
        #                  'Failed clip name test char 2')
        # self.assertEqual(s.events[2].clip_name, 'clip -3',
        #                  'Failed clip name test char 3')
        # self.assertEqual(s.events[3].clip_name, 'clip $4',
        #                  'Failed clip name test char 4')
        # self.assertEqual(s.events[4].clip_name, 'clip &5',
        #                  'Failed clip name test char 5')
        # self.assertEqual(s.events[5].src_start_tc.frame_number, 697,
        #                  "Wrong Source start complex event")
        # self.assertEqual(s.events[5].src_end_tc.frame_number, 697,
        #                  "Wrong Source end complex event")
        # self.assertEqual(s.events[5].rec_start_tc.frame_number, 2857,
        #                  "Wrong Source start complex event")
        # self.assertEqual(s.events[5].rec_end_tc.frame_number, 2857,
        #                  "Wrong Source end complex event")

    def test_pal(self):
        s = EDL.from_file(25, '../tests/test_data/test_25.edl')

    def test_ntsc(self):
        s = EDL.from_file(25, '../tests/test_data/test_2997NDF.edl')

    def test_2398fps(self):
        s = EDL.from_file(23.98, '../tests/test_data/test_2398.edl')
