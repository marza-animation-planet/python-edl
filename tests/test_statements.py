import unittest

from edl import EDL
from edl.event import Statement, Title, FrameCodeMode, StatementError


class BaseStatementTests(unittest.TestCase):
    """Test cases for base Statement class
    """
    invalid_raw_types = [
        1234,
        1234.567,
        dict(),
        tuple(),
        list()
    ]

    def setUp(self):
        self.edl = EDL(24)

    def test_init_with_raw_text(self):
        """Verify Statements save their raw text
        """
        raw_text = "Test text"
        statement = Statement(self.edl, raw_text)
        self.assertEqual(raw_text, statement.raw)
        self.assertEqual(raw_text, str(statement))

    def test_invalid_raw_types(self):
        """Verify Statements reject invalid raw_text types
        """
        for invalid in self.invalid_raw_types:
            self.assertRaises(TypeError, Statement, self.edl, invalid)


class TitleStatementTests(unittest.TestCase):
    """Test cases for Title Statement class
    """
    # "TITLE:" must be a single block, but other whitespacing doesn't really matter.
    # That said, current behavior preserves all whitespacing after the colon and
    # optional(?) space between identifier and title.
    # ToDo: Determine whether space between identifier and title is mandatory.
    valid_raw_titles = [
        "TITLE: Test Title",
        " TITLE: Test Title",
        "TITLE:   Test title",
        "  TITLE:   Test   Title   ",
        u"TITLE: Test Title",
        u" TITLE: Test Title",
        u"TITLE:   Test title",
        u"  TITLE:   Test   Title   "
    ]

    invalid_raw_titles = [
        # TITLE must be all-caps
        "Title: Test Title",
        # TITLE: must be a single block
        "TITLE : Test Title",
        # TITLE: identifier must be present.
        "This isn't even a title",
        "Test Title",
        u"Title: Test Title",
        u"TITLE : Test Title",
        u"This isn't even a title",
        u"Test Title"
    ]

    # Title values for testing assignment
    valid_title_values = [
        "Test Title",
        "Test Title that is seventy characters which is right at the max  limit",
        u"Test Title",
        u"Test Title that is seventy characters which is right at the max  limit"
    ]

    invalid_title_values = [
        "Test Title that is seventy - one characters which is over the max limit",
        u"Test Title that is seventy - one characters which is over the max limit",
        None,
        1234,
        1234.1234,
        dict(),
        list(),
        tuple(),
    ]

    def setUp(self):
        self.edl = EDL(24)

    def test_parse_valid_titles(self):
        """Verify that valid titles parse correctly"""
        for test_title in self.valid_raw_titles:
            title = Title(self.edl, test_title)
            # Strip leading whitespace to avoid false negatives
            self.assertEqual(test_title.lstrip(' '), str(title))

    def test_parse_invalid_titles(self):
        """Verify that invalid titles raise StatementErrors"""
        for test_title in self.invalid_raw_titles:
            self.assertRaises(StatementError, Title, self.edl, test_title)

    def test_assign_valid_titles(self):
        """Verify that assigning valid titles works"""
        for test_title in self.valid_title_values:
            title = Title(self.edl)
            title.title = test_title
            self.assertEqual(test_title, title.title)

    def test_assign_invalid_titles(self):
        """Verify that assigning invalid titles raises correct exceptions"""
        def assign_value(obj, value):
            assert(isinstance(obj, Title))
            obj.title = value

        for test_title in self.invalid_title_values:
            if isinstance(test_title, basestring):
                expected_exc = ValueError
            else:
                expected_exc = TypeError
            title = Title(self.edl)
            self.assertRaises(expected_exc, assign_value, title, test_title)


class FrameCodeModeStatementTests(unittest.TestCase):
    """Test cases for Frame Code Mode Statement class
    """

    valid_statements = [
        "FCM: DROP FRAME",
        "FCM: NON DROP FRAME",
        " FCM:DROP FRAME ",
        " FCM:  NON DROP FRAME"
    ]

    invalid_statements = [
        # Colon is required for identifier
        "FCM DROP FRAME",
        # Identifier must be all-caps
        "Fcm: DROP FRAME",
        # Values must be all-caps:
        "FCM: Drop Frame",
        "FCM: Non Drop Frame",
        "This is not an FCM statement",
        # Ignoring next case for now, as we're able to parse it correctly, and
        # it will be corrected if we re-write the file.
        # "FCM: DROP FRAME  ."
    ]

    valid_values = [True, False]
    invalid_values = [
        1234,
        1234.567,
        dict(),
        tuple(),
        list(),
        # While expected displayed values, not helpful as general data
        "DROP FRAME",
        "NON DROP FRAME"
    ]

    def setUp(self):
        self.edl = EDL(24)

    def test_parse_valid_fcm(self):
        """Verify that valid FCM statements parse correctly"""
        for test_fcm in self.valid_statements:
            expected_value = "NON" not in test_fcm
            if expected_value:
                expected_str = "FCM: DROP FRAME"
            else:
                expected_str = "FCM: NON DROP FRAME"

            fcm = FrameCodeMode(self.edl, test_fcm)
            self.assertEqual(expected_value, fcm.isDropFrame)
            self.assertEqual(expected_str, str(fcm))

    def test_parse_invalid_fcm(self):
        """Verify that invalid FCM statements raise StatementErrors"""
        for test_fcm in self.invalid_statements:
            self.assertRaises(StatementError, FrameCodeMode, self.edl, test_fcm)

    def test_assign_valid_values(self):
        """Verify that assigning valid values works"""
        for test_fcm in self.valid_values:
            if test_fcm:
                expected_str = "FCM: DROP FRAME"
            else:
                expected_str = "FCM: NON DROP FRAME"
            fcm = FrameCodeMode(self.edl)
            fcm.isDropFrame = test_fcm

            self.assertEqual(test_fcm, fcm.isDropFrame)
            self.assertEqual(expected_str, str(fcm))

    def test_assign_invalid_values(self):
        """Verify that assigning invalid titles raises correct exceptions"""
        def assign_value(obj, value):
            assert(isinstance(obj, FrameCodeMode))
            obj.isDropFrame = value

        for test_fcm in self.invalid_values:
            fcm = FrameCodeMode(self.edl)
            self.assertRaises(TypeError, assign_value, fcm, test_fcm)
