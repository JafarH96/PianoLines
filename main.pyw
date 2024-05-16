from piano_lines import PianoLines, PianoModes

def main():
    board = PianoLines((400, 400), PianoModes.Trainer)
    board.run()

if __name__ == '__main__':
    main()


