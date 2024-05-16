import time
from notes import Notes

class NoteButton:
    note: Notes
    pos = (0, 0)
    size = (30, 30)
    color = (0, 0, 0)
    pressed_color = (50, 50, 50)
    current_time = 0

    def __init__(self, note, pos, size = (30, 30), color = (0, 0, 0)) -> None:
        self.note = note
        self.pos = pos
        self.size = size
        self.color = color

    def name(self):
        return self.note.name
    
    def clicked(self, x, y):
        if self.pos[0] + self.size[0] >= x >= self.pos[0]:
            if self.pos[1] + self.size[1] >= y >= self.pos[1]:
                return True
            
        return False
    
    def get_color(self):
        if self.current_time:
            if self.current_time + 0.5 > time.time():
                return self.pressed_color
            else:
                return self.color
        else:
            return self.color

    def pressed(self):
        self.current_time = time.time()