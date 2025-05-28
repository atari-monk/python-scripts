import pygame.midi
import time

def main():
    bpm = 100
    quarter_note = 60 / bpm

    melody = [
        (60, 1), (60, 1), (67, 1), (67, 1), (69, 1), (69, 1), (67, 2),
        (65, 1), (65, 1), (64, 1), (64, 1), (62, 1), (62, 1), (60, 2),
        (67, 1), (67, 1), (65, 1), (65, 1), (64, 1), (64, 1), (62, 2),
        (67, 1), (67, 1), (65, 1), (65, 1), (64, 1), (64, 1), (62, 2),
        (60, 1), (60, 1), (67, 1), (67, 1), (69, 1), (69, 1), (67, 2),
        (65, 1), (65, 1), (64, 1), (64, 1), (62, 1), (62, 1), (60, 2),
    ]

    melody_with_durations = [(note, dur * quarter_note) for note, dur in melody]

    pygame.midi.init()
    player = pygame.midi.Output(0)
    player.set_instrument(0)

    for note, dur in melody_with_durations:
        player.note_on(note, 100)
        time.sleep(dur)
        player.note_off(note, 100)

    del player
    pygame.midi.quit()