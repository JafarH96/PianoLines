from enum import Enum

note_number = {
    'do': 1,
    're': 2,
    'mi': 3,
    'fa': 4,
    'sol': 5,
    'la': 6,
    'si': 7
}

class Notes(Enum):
    DO = 1
    RE = 2
    MI = 3
    FA = 4
    SOL = 5
    LA = 6
    SI = 7

class Note:
    note: Notes
    octave = 0

    def __init__(self, note, octave) -> None:
        self.note = note
        self.octave = octave