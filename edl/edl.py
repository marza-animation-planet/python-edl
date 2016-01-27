# import collections
# import pprint
from timecode import Framerate
from .event import Event
# from .matchers import TitleMatcher, EventMatcher, EffectMatcher, NameMatcher, \
#     SourceMatcher, TimewarpMatcher, CommentMatcher
from .event import Statement


class EDL(object):
    """The EDL it self.

    Holds :class:`.Event` instances. It can be indexed to reach each of the
    :class:`.Event`\ s like::

      >>> l = EDL('25')
      >>> l.append(Event())
      >>> l[0]
      <edl.edl.Event object at 0x7fb630564490>

    :param basestring, int, float fps: The frame per second setting for for this EDL. Should be a
      string one of ['23.98', '24', '25', '29.97', '30', '50', '59.94', '60'].
      `fps` can not be skipped.
    """

    def __init__(self, fps):
        self.fps = Framerate(fps)
        self.events = []
        self.title = ''

    def __getitem__(self, i):
        """Returns each of the Events that this EDL holds.
        """
        return self.events[i]

    # def __repr__(self):
    #     rep = ["event(\n"]
    #     for e in self.events:
    #         rep.append(e.__repr__())
    #     rep.append(')')
    #     return ''.join(rep)

    def __len__(self):
        return len(self.events)

    @classmethod
    def from_file(cls, fps, file_):
        # ToDO: handle both files and filepaths
        with open(file_) as f:
            data = f.readlines()
        return cls._parse(fps, data)

    @classmethod
    def from_string(cls, fps, text):
        # ToDo: handle files with CRLF endings
        data = text.split('\n')
        return cls._parse(fps, data)

    @classmethod
    def _parse(cls, fps, data):
        edl = EDL(fps)
        # matchers = [TitleMatcher(), EventMatcher(fps), EffectMatcher(),
        #             NameMatcher(), SourceMatcher(), TimewarpMatcher(fps),
        #             CommentMatcher()]
        for line in data:
            line = line.rstrip('\n')  # Remove trailing newlines, usu. from files
            if line:  # Only spend cycles on lines with data
                edl.events.append(Statement(edl, line))
                # for m in matchers:
                #     if m.apply(edl, line):
                #         break

        return edl

    @property
    def isPAL(self):
        """Return True if assigned framerate is PAL"""
        return self.fps.isPAL

    @property
    def isNTSC(self):
        """Return True if assigned framerate is NTSC"""
        return self.fps.isNTSC

    @property
    def dropFrameRate(self):
        """Return drop-frame equivalent of current framerate.
        Returns current framerate if already drop-frame or if framerate is PAL.
        """
        return self.fps.dropFrameRate

    @property
    def nonDropFrameRate(self):
        """Return non-drop-frame equivalent of current framerate.
        Returns current framerate if already non-drop-frame or if framerate is
        PAL.
        """
        return self.fps.nonDropFrameRate

    def get_start(self):
        start_tc = None
        for e in self.events:
            if start_tc is None:
                start_tc = e.rec_start_tc
            else:
                if e.rec_start_tc.frames < start_tc.frames:
                    start_tc = e.rec_start_tc
        return start_tc

    def get_end(self):
        end_tc = None
        for e in self.events:
            if end_tc is None:
                end_tc = e.rec_end_tc
            else:
                if e.rec_end_tc.frames > end_tc.frames:
                    end_tc = e.rec_end_tc
        return end_tc

    def get_length(self):
        return self.get_end().frames - self.get_start().frames

    def append(self, evt):
        self.events.append(evt)

    def events(self):
        return self.events

    def without_transitions(self):
        raise NotImplementedError

    def renumbered(self):
        raise NotImplementedError

    def without_timewarps(self):
        raise NotImplementedError

    def without_generators(self):
        raise NotImplementedError

    def capture_list(self):
        raise NotImplementedError

    def from_zero(self):
        raise NotImplementedError

    def spliced(self):
        raise NotImplementedError

    def to_string(self):
        """The string output of the Events, this matches a standard EDL file
        format. Using EDL.to_string() should return the edl back to its
        original format.
        """
        # for each Event call their to_string() method and gather the output
        output_buffer = ['TITLE: %s' % self.title, '']
        for event in self.events:
            output_buffer.append(str(event))
            # output_buffer.append('')
        return '\n'.join(output_buffer)
