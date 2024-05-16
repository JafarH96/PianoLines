import pygame
import random
import sys
import time
from notes import *
from buttons import NoteButton
from line import *
from note_sheets import NoteSheet
from enum import Enum
from utils import get_base_dir


class PianoModes(Enum):
    Trainer = 1
    Music = 2
    Note_Lines = 3


class PianoLines:
    mode: PianoModes
    note_sheet: NoteSheet
    note: Note

    lines = []
    note_buttons = []

    size = (200, 200)

    line_len = 350

    correct_score = 0
    wrong_score = 0

    note_timeout = 5

    running = True
    pause = False
    hint = False

    def __init__(self, size, mode, note_sheet_path = None) -> None:
        self.mode = mode
        if note_sheet_path:
            self.set_note_sheet(note_sheet_path)
        self.size = (max(size[0], 400), max(size[1], 350))
        self.initialize_board()
        self.initialize_lines()
        self.initialize_note_buttons()
        self.generate_note()

    def initialize_board(self):
        pygame.init()
        pygame.display.set_caption('Piano Lines')
        logo_surface = pygame.image.load(f"{get_base_dir()}/logo.png")
        pygame.display.set_icon(logo_surface)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)
        self.c_x = self.screen.get_width() // 2
        self.c_y = self.screen.get_height() // 2
        self.font = pygame.font.SysFont('arial', 14)
        self.scores_font = pygame.font.SysFont('tahoma', 20)

    def initialize_lines(self):
        self.lines_start_y = 60
        lines_offset = self.lines_start_y
        for i in range(7):
            self.lines.append(Line(i+1, (self.c_x - (self.line_len // 2), lines_offset), self.line_len))
            lines_offset += Line.LINES_DIST

    def initialize_note_buttons(self):
        buttons_space = 6
        button_width = 40
        button_height = 80
        buttons_start_pos_x = self.c_x - ((7 * button_width / 2) + (3 * buttons_space))
        buttons_start_pos_y = self.size[1] - (button_height + 10)
        current_button_x = buttons_start_pos_x
        for i in range(7):
            note = Notes(i + 1)
            self.note_buttons.append(NoteButton(note, (current_button_x, buttons_start_pos_y), (button_width, button_height), (255, 255, 255)))
            current_button_x += (buttons_space + button_width)

    def set_note_sheet(self, file_path):
        self.note_sheet = NoteSheet(file_path)
        self.note = self.note_sheet.get_note()

    def generate_note(self):
        if self.mode == PianoModes.Trainer:
            rand = random.randint(1, 7)
            octave = random.randint(0, 1)
            self.note = Note(Notes(rand), octave)
        else:
            self.note = self.note_sheet.get_note()

    def set_score(self, note):
        if note == self.note.note:
            self.correct_score += 1
            self.hint = False
            if self.mode == PianoModes.Music:
                self.note_sheet.next()
        else:
            self.wrong_score += 1
            self.set_wrong_note_temp()
        self.generate_note()

    def set_wrong_note_temp(self):
        self.last_wrong_note = self.note
        self.wrong_note_time = time.time()
        self.hint = True

    def draw_lines(self):
        for line in self.lines:
            if line.number == 1:
                pygame.draw.line(self.screen, 'red', (line.pos[0] + (line.len // 2), line.pos[1]), (line.pos[0] + line.len, line.pos[1]))
            elif line.number == 7:
                pygame.draw.line(self.screen, 'red', (line.pos[0], line.pos[1]), (line.pos[0] + (line.len // 2), line.pos[1]))
            else:
                pygame.draw.line(self.screen, 'black', (line.pos[0], line.pos[1]), (line.pos[0] + line.len, line.pos[1]))

    def draw_note(self):
        line_num = notes_line[self.note.note.value][self.note.octave] - 1
        pos = self.lines[line_num].get_note_pos(self.note.octave)
        time_text = self.font.render(f'{self.note_timeout - self.seconds:.0f}', True, 'white')
        pygame.draw.circle(self.screen, 'black', pos, Line.note_shape_size)
        self.screen.blit(time_text, (pos[0]-(Line.note_shape_size/3),pos[1]-(Line.note_shape_size)))

    def draw_buttons(self):
        for note_button in self.note_buttons:
            btn_color = note_button.get_color()
            text = self.font.render(note_button.name(), True, (255-btn_color[0], 255-btn_color[1], 255-btn_color[2]))
            rect_x, rect_y = note_button.pos
            rect_width, rect_height = note_button.size
            rectangle = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
            pygame.draw.rect(self.screen, note_button.get_color(), rectangle)
            text_x, text_y = rect_x + rect_width / 4, rect_y + rect_height / 2
            self.screen.blit(text, (text_x, text_y))

    def draw_score(self):
        scores_pos_y = 10
        correct_score_pos_x = 20
        wrong_score_pos_x = self.c_x
        correct_text = self.scores_font.render(f'Correct: {self.correct_score}', True, (10, 120, 50))
        wrong_text = self.scores_font.render(f'Wrong: {self.wrong_score}', True, (200, 30, 30))
        self.screen.blit(correct_text, (correct_score_pos_x, scores_pos_y))
        self.screen.blit(wrong_text, (wrong_score_pos_x, scores_pos_y))

    def show_hint(self):
        if self.wrong_note_time + 0.5 < time.time():
            self.hint = False
            return
        line_num = notes_line[self.last_wrong_note.note.value][self.last_wrong_note.octave] - 1
        pos = self.lines[line_num].get_note_pos(self.last_wrong_note.octave)
        text = self.scores_font.render(self.last_wrong_note.note.name, True, (0, 0, 0))
        self.screen.blit(text, pos)

    def play_sound(self, file_name):
        pygame.mixer.music.load(f"{get_base_dir()}/sounds/{file_name}.wav")
        pygame.mixer.music.play()

    def key_released(self, key):
        if key == pygame.K_a:
            self.note_buttons[0].pressed()
            self.play_sound('do')
            self.set_score(Notes.DO)
        elif key == pygame.K_s:
            self.note_buttons[1].pressed()
            self.play_sound('re')
            self.set_score(Notes.RE)
        elif key == pygame.K_d:
            self.note_buttons[2].pressed()
            self.play_sound('mi')
            self.set_score(Notes.MI)
        elif key == pygame.K_f:
            self.note_buttons[3].pressed()
            self.play_sound('fa')
            self.set_score(Notes.FA)
        elif key == pygame.K_g:
            self.note_buttons[4].pressed()
            self.play_sound('sol')
            self.set_score(Notes.SOL)
        elif key == pygame.K_h:
            self.note_buttons[5].pressed()
            self.play_sound('la')
            self.set_score(Notes.LA)
        elif key == pygame.K_j:
            self.note_buttons[6].pressed()
            self.play_sound('si')
            self.set_score(Notes.SI)
    
    def run(self):
        start_ticks=pygame.time.get_ticks()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos
                    for button in self.note_buttons:
                        if button.clicked(x, y):
                            start_ticks=pygame.time.get_ticks()
                            button.pressed()
                            self.play_sound(button.note.name.lower())
                            self.set_score(button.note)
                            break
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                        continue
                    start_ticks=pygame.time.get_ticks()
                    self.key_released(event.key)

            if not self.pause:
                self.seconds=(pygame.time.get_ticks()-start_ticks)/1000
                if self.seconds > self.note_timeout:
                    start_ticks=pygame.time.get_ticks()
                    self.set_wrong_note_temp()
                    self.generate_note()

                self.screen.fill("gray")
                self.draw_lines()
                self.draw_note()
                self.draw_score()
                self.draw_buttons()

                if self.hint:
                    self.show_hint()

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()