from notes import *

class NoteSheet:
    notes = []
    file_path: str
    current_note = 0

    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.__read_file()

    def __read_file(self):
        with open(self.file_path, 'r') as file:
            for notes_line in file.readlines():
                notes_list = notes_line.split('-')
                for note_str in notes_list:
                    note_num = note_number[note_str.replace(' ', '').replace('\n', '').removesuffix('#').lower()]
                    note = Note(Notes(note_num), 0)
                    print(note.note.name)
                    self.notes.append(note)

    def next(self):
        self.current_note += 1
        if self.current_note >= len(self.notes):
            self.current_note = 0

    def get_note(self):
        return self.notes[self.current_note]