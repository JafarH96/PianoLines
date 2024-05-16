from notes import Notes

line_notes = {
    1: [Notes.SI, Notes.LA],
    2: [Notes.SOL, Notes.FA],
    3: [Notes.MI, Notes.RE],
    4: [Notes.DO, Notes.SI],
    5: [Notes.LA, Notes.SOL],
    6: [Notes.FA, Notes.MI],
    7: [Notes.RE, Notes.DO],
}

notes_line = {
    1: [4, 7],
    2: [7, 3],
    3: [3, 6],
    4: [6, 2],
    5: [2, 5],
    6: [5, 1],
    7: [1, 4]
}

class Line:
    number = 1
    pos = (0, 0)
    len = 100
    notes = []
    note_shape_size = 5

    LINES_DIST = 14

    def __init__(self, number, pos, len) -> None:
        self.number = number
        self.pos = pos
        self.len = len
        self.__set_note()

    def __set_note(self):
        self.notes = line_notes[self.number]

    def get_note_pos(self, index):
        x = self.pos[0] + (self.note_shape_size * 2) + ((self.len / 7) * (7 - self.number))
        if index == 0:
            return x + (self.len / 14), self.pos[1] - Line.LINES_DIST // 2
        else:
            return x, self.pos[1]