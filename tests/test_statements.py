import unittest
from edl.event import Statement, Title, StatementError


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

    def test_init_with_raw_text(self):
        """Verify Statements save their raw text
        """
        raw_text = "Test text"
        statement = Statement(raw_text)
        self.assertEqual(raw_text, statement.raw)
        self.assertEqual(raw_text, str(statement))

    def test_invalid_raw_types(self):
        """Verify Statements reject invalid raw_text types
        """
        for invalid in self.invalid_raw_types:
            self.assertRaises(TypeError, Statement, invalid)


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

    def test_parse_valid_titles(self):
        """Verify that valid titles parse correctly"""
        for test_title in self.valid_raw_titles:
            title = Title(test_title)
            # Strip leading whitespace to avoid false negatives
            self.assertEqual(test_title.lstrip(' '), str(title))

    def test_parse_invalid_titles(self):
        """Verify that invalid titles raise StatementErrors"""
        for test_title in self.invalid_raw_titles:
            self.assertRaises(StatementError, Title, test_title)

    def test_assign_valid_titles(self):
        """Verify that assigning valid titles works"""
        for test_title in self.valid_title_values:
            title = Title()
            title.title = test_title
            self.assertEqual(test_title, title.title)

    def test_assign_invalid_titles(self):
        """Verify that assigning invalid titles raises StatementErrors"""
        def assign_value(obj, value):
            assert(isinstance(obj, Title))
            obj.title = value

        for test_title in self.invalid_title_values:
            if isinstance(test_title, basestring):
                expected_exc = ValueError
            else:
                expected_exc = TypeError
            title = Title()
            self.assertRaises(expected_exc, assign_value, title, test_title)
