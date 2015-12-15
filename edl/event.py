import re
from .effects import Cut, Timewarp


class Event(object):
    """Represents an edit event (or, more specifically, an EDL line denoting a
    clip being part of an EDL event)
    """

    def __init__(self, options):
        """Initialisation function with options:
        """
        self.comments = []
        self.timewarp = None
        self.next_event = None
        self.track = None
        self.clip_name = None
        self.source_file = None
        self.transition = None
        self.aux = None
        self.reel = None
        self.rec_end_tc = None
        self.rec_start_tc = None
        self.src_end_tc = None
        self.src_start_tc = None
        self.num = None
        self.tr_code = None

        # TODO: This is absolutely wrong and not safe. Please validate the
        #       incoming values, before adopting them as instance variables
        #       and instance methods
        for o in options:
            self.__dict__[o] = options[o]

    # def __repr__(self):
    #     v = ["(\n"]
    #     for k in self.__dict__:
    #         v.append("    %s=%s,\n" % (k, self.__dict__[k]))
    #     v.append(")")
    #     return ''.join(v)

    def to_string(self):
        """Human Readable string representation of edl event.

        Returns the string representation of this Event which is suitable
        to be written to a file to gather back the EDL itself.
        """
        effect = ''
        if self.transition:
            try:
                effect = 'EFFECTS NAME IS %s\n' % self.transition.effect
            except AttributeError:
                pass

        s = "%(num)-6s %(reel)-32s %(track)-5s %(tr_code)-3s %(aux)-4s " \
            "%(src_start_tc)s %(src_end_tc)s %(rec_start_tc)s " \
            "%(rec_end_tc)s\n" \
            "%(effect)s" \
            "%(notes)s" \
            "%(timewarp)s" % {
                'num': self.num if self.num else '',
                'reel': self.reel if self.reel else '',
                'track': self.track if self.track else '',
                'aux': self.aux if self.aux else '',
                'tr_code': self.tr_code if self.tr_code else '',
                'src_start_tc': self.src_start_tc,
                'src_end_tc': self.src_end_tc,
                'rec_start_tc': self.rec_start_tc,
                'rec_end_tc': self.rec_end_tc,
                'effect': effect,
                'notes': '%s\n' % '\n'.join(self.comments)
                if self.comments else '',
                'timewarp': '%s\n' % self.timewarp.to_string()
                if self.has_timewarp() else ''}

        return s

    def get_comments(self):
        """Return comments array
        """
        return self.comments

    def outgoing_transition_duration(self):
        """TBC
        """
        if self.next_event:
            return self.next_event.incoming_transition_duration()
        else:
            return 0

    def reverse(self):
        """Returns true if clip is timewarp reversed
        """
        return self.timewarp and self.timewarp.reverse

    def copy_properties_to(self, event):
        """Copy event properties to another existing event object
        """
        for k in self.__dict__:
            event.__dict__[k] = self.__dict__[k]
        return event

    def has_transition(self):
        """Returns true if clip if clip uses a transition and not a Cut
        """
        return not isinstance(self.transition, Cut)

    def incoming_transition_duration(self):
        """Returns incoming transition duration in frames, returns 0 if no
        transition set
        """
        d = 0
        if not isinstance(self.transition, Cut):
            d = int(self.aux)
        return d

    def ends_with_transition(self):
        """Returns true if the clip ends with a transition (if the next clip
        starts with a transition)
        """
        if self.next_event:
            return self.next_event.has_transition()
        else:
            return False

    def has_timewarp(self):
        """Returns true if the clip has a timewarp (speed ramp, motion memory,
        you name it)
        """
        if isinstance(self.timewarp, Timewarp):
            return True
        else:
            return False

    def black(self):
        """Returns true if event is black slug
        """
        return self.reel == "BL"

    def rec_length(self):
        """Returns record length of event in frames before transition
        """
        return self.rec_end_tc.frames - self.rec_start_tc.frames

    def rec_length_with_transition(self):
        """Returns record length of event in frames including transition
        """
        return self.rec_length() + self.outgoing_transition_duration()

    def src_length(self):
        """Returns source length of event in frames before transition
        """
        return self.src_end_tc.frames - self.src_start_tc.frames

    def capture_from_tc(self):
        raise NotImplementedError

    def capture_to_and_including_tc(self):
        raise NotImplementedError

    def capture_to_tc(self):
        raise NotImplementedError

    def speed(self):
        raise NotImplementedError

    def generator(self):
        raise NotImplementedError

    def get_clip_name(self):
        return self.clip_name

    def get_reel(self):
        return self.reel

    def event_number(self):
        return self.num

    def get_track(self):
        return self.track

    def get_tr_code(self):
        return self.tr_code

    def get_aux(self):
        return self.aux


class StatementError(Exception):
    """Exception for Statement errors
    """


class Statement(object):
    """Base class for Event statements
    """
    _identifier = None
    _regex = None

    def __init__(self, raw_text=None):
        if (raw_text is not None) and (not isinstance(raw_text, basestring)):
            raise TypeError("Raw statement data must be a string")
        self._prev_statement = None
        self._next_statement = None
        self._raw = raw_text
        # Don't call _parse in base init to prevent subclass overrides from
        # setting values in their super call, then stomping them with their
        # instance variable setup. Could put the super at the end of subclass
        # inits, but then get into wonky dependency ordering.

    def __str__(self):
        # ToDo: Format output "columns" to use StandardForm as base alignment.
        # See spec Appendices E and F (pg. 53-57) for examples.
        return self._raw

    def _parse(self, raw_text):
        """Parse raw data and update fields.
        :type basestring raw_text: Raw text data for statement
        """

    @property
    def raw(self):
        return self._raw


class Title(Statement):
    """A Title Statement as defined by the CMX standard.
    """

    _identifier = "TITLE:"
    _regex = re.compile("TITLE:\s?(?P<title>.+)")

    def __init__(self, raw_text=None):
        super(Title, self).__init__(raw_text)
        self._title = None

        if self.raw:
            self._parse(self.raw)

    def __str__(self):
        return " ".join([self._identifier, self._title if self._title else ""])

    def _parse(self, raw_text):
        try:
            title = self._regex.search(raw_text).group('title')
        except (AttributeError, TypeError):
            raise StatementError("Statement is not a valid Title statement:\n\t\"{}\"".format(raw_text))
        # Bypass the title-setting safeguards. For now we'll assume that
        # data read from an EDL file is authoritative. This may come back to
        # bite us, of course.
        self._title = title

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, basestring):
            raise TypeError("Title must be a string")
        if len(value) > 70:
            raise ValueError("Title length must be no more than 70 characters")
        self._title = value


class FrameCodeMode(Statement):
    """A Frame Code Mode (FCM) Statement as defined by the CMX standard.
    """

    _identifier = "FCM:"
    _regex = re.compile("FCM:(\s+)?(?P<mode>(?:NON\s)?DROP\sFRAME)")
    DROP_FRAME = "DROP FRAME"
    NON_DROP_FRAME = "NON DROP FRAME"

    def __init__(self, raw_text=None):
        super(FrameCodeMode, self).__init__(raw_text)
        self._isDropFrame = False

        if self.raw:
            self._parse(self.raw)

    def __str__(self):
        return " ".join([self._identifier, self._field_text])

    def _parse(self, raw_text):
        try:
            self._isDropFrame = self.DROP_FRAME == self._regex.search(raw_text).group('mode')
        except (AttributeError, TypeError):
            raise StatementError("Statement is not a valid FCM:\n\t\"{}\"".format(raw_text))

    @property
    def _field_text(self):
        return self.DROP_FRAME if self.isDropFrame else self.NON_DROP_FRAME

    @property
    def isDropFrame(self):
        return self._isDropFrame

    @isDropFrame.setter
    def isDropFrame(self, value):
        if not isinstance(value, bool):
            raise TypeError("isDropFrame must be a bool")
        self._isDropFrame = value
