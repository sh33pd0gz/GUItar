from enum import Enum, auto
from typing import Dict, List, NewType, Tuple

from intervals import NOTES, MajorScale, Note

Fret = NewType("Fret", int)
String = NewType("String", int)


class Position(Enum):
    OPEN = auto()
    A = auto()
    F = auto()
    D = auto()


STRING_WEIGHT = {6: 0, 5: 5, 4: 10, 3: 15, 2: 19, 1: 24}


class FretboardNotes:
    scale: List[Note]
    notes: Dict[String, List[Tuple[Fret, Note]]] = {}

    def __init__(
        self,
        major_scale: MajorScale,
        tuning: Tuple[str, ...] = ("E", "B", "G", "D", "A", "E"),
    ):
        self.scale = major_scale.scale
        [
            self.notes.setdefault(String(string + 1), []).append((Fret(fret), note))
            for string, string_tuning in enumerate(tuning)
            for fret in range(13)
            if (note := NOTES[(NOTES.index(string_tuning) + fret) % len(NOTES)])
            in self.scale
        ]

    def filter_notes_by_position(
        self, anchor: Fret = Fret(0)
    ) -> Dict[String, List[Tuple[Fret, Note]]]:
        # ranked = []
        # filtered = {}
        # for string, pairs in self.notes.items():
        #     for pair in pairs:
        #         if (
        #             pair[0] < 5
        #             and (rank := STRING_WEIGHT[string] + pair[0]) not in ranked
        #         ):
        #             ranked.append(rank)
        #             filtered.setdefault(string, []).append(pair)
        # return self.notes
        ranked = []
        filtered = {}
        for string, pairs in self.notes.items():
            for pair in pairs:
                if (pair[0] < anchor + 4) and (pair[0] > anchor - 4):
                    filtered.setdefault(string, []).append(pair)
        return filtered


# for testing
if __name__ == "__main__":
    fretboard_notes = FretboardNotes(MajorScale("C"))
    print(fretboard_notes.filter_notes_by_position())
