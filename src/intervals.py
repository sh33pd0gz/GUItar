from enum import Enum
from typing import List, Literal, Tuple, get_args

Note = Literal["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
NOTES: Tuple[Note, ...] = get_args(Note)


class MajorScaleIntervals(Enum):
    UNISON = 0
    M2 = 2
    M3 = 4
    P4 = 5
    P5 = 7
    M6 = 9
    M7 = 11


class MajorScale:
    key: Note

    def __init__(self, root_note: Note):
        self.key = root_note

    @property
    def scale(self) -> List:
        return [
            NOTES[(NOTES.index(self.key) + interval.value) % len(NOTES)]
            for interval in MajorScaleIntervals
        ]


# for testing
if __name__ == "__main__":
    major_scale = MajorScale("F")
    print(major_scale.scale)
