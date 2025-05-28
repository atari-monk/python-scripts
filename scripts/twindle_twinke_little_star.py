import pygame.midi
import time

# Set tempo
bpm = 100
quarter_note = 60 / bpm  # seconds per quarter note

# Melody: Twinkle, Twinkle, Little Star in C Major
# Notes: (MIDI number, duration in quarter notes)
melody = [
    (60, 1), (60, 1), (67, 1), (67, 1), (69, 1), (69, 1), (67, 2),  # Twinkle, twinkle, little star
    (65, 1), (65, 1), (64, 1), (64, 1), (62, 1), (62, 1), (60, 2),  # How I wonder what you are
    (67, 1), (67, 1), (65, 1), (65, 1), (64, 1), (64, 1), (62, 2),  # Up above the world so high
    (67, 1), (67, 1), (65, 1), (65, 1), (64, 1), (64, 1), (62, 2),  # Like a diamond in the sky
    (60, 1), (60, 1), (67, 1), (67, 1), (69, 1), (69, 1), (67, 2),  # Twinkle, twinkle, little star
    (65, 1), (65, 1), (64, 1), (64, 1), (62, 1), (62, 1), (60, 2),  # How I wonder what you are
]

# Convert to durations in seconds
melody_with_durations = [(note, dur * quarter_note) for note, dur in melody]

# Initialize MIDI
pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(0)  # Acoustic Grand Piano (or use 40 for Violin)

# Play the melody
for note, dur in melody_with_durations:
    player.note_on(note, 100)
    time.sleep(dur)
    player.note_off(note, 100)

# Cleanup
del player
pygame.midi.quit()

