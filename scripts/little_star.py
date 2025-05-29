import pygame.midi
import time

def play_melody(melody, bpm=100, instrument=0):
    quarter_note = 60 / bpm
    melody_with_durations = [(note, dur * quarter_note) for note, dur in melody]
    
    pygame.midi.init()
    try:
        player = pygame.midi.Output(pygame.midi.get_default_output_id())
        player.set_instrument(instrument)
        
        for note, dur in melody_with_durations:
            if note > 0:
                player.note_on(note, 100)
                time.sleep(dur)
                player.note_off(note, 100)
            else:
                time.sleep(dur)
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            del player
        except:
            pass
        pygame.midi.quit()

def main():
    melodies = {
        "1": {
            "name": "Twinkle Twinkle Little Star",
            "melody": [
                (60, 1), (60, 1), (67, 1), (67, 1), (69, 1), (69, 1), (67, 2),
                (65, 1), (65, 1), (64, 1), (64, 1), (62, 1), (62, 1), (60, 2),
                (67, 1), (67, 1), (65, 1), (65, 1), (64, 1), (64, 1), (62, 2),
                (67, 1), (67, 1), (65, 1), (65, 1), (64, 1), (64, 1), (62, 2),
                (60, 1), (60, 1), (67, 1), (67, 1), (69, 1), (69, 1), (67, 2),
                (65, 1), (65, 1), (64, 1), (64, 1), (62, 1), (62, 1), (60, 2)
            ],
            "instrument": 0,
            "bpm": 100
        },
        "2": {
            "name": "Happy Birthday",
            "melody": [
                (60, 0.5), (60, 0.5), (62, 1), (60, 1), (65, 1), (64, 2),
                (60, 0.5), (60, 0.5), (62, 1), (60, 1), (67, 1), (65, 2),
                (60, 0.5), (60, 0.5), (72, 1), (69, 1), (65, 1), (64, 1), (62, 2),
                (70, 0.5), (70, 0.5), (69, 1), (65, 1), (67, 1), (65, 2)
            ],
            "instrument": 0,
            "bpm": 120
        },
        "3": {
            "name": "Ode to Joy (Beethoven)",
            "melody": [
                (64, 1), (64, 1), (65, 1), (67, 1), (67, 1), (65, 1), (64, 1), (62, 1),
                (60, 1), (60, 1), (62, 1), (64, 1), (64, 1.5), (62, 0.5), (62, 2),
                (64, 1), (64, 1), (65, 1), (67, 1), (67, 1), (65, 1), (64, 1), (62, 1),
                (60, 1), (60, 1), (62, 1), (64, 1), (62, 1.5), (60, 0.5), (60, 2)
            ],
            "instrument": 0,
            "bpm": 100
        },
        "4": {
            "name": "Jingle Bells",
            "melody": [
                (64, 1), (64, 1), (64, 2), (64, 1), (64, 1), (64, 2),
                (64, 1), (66, 1), (60, 1.5), (62, 0.5), (64, 2),
                (65, 1), (65, 1), (65, 1), (65, 1), (65, 1), (64, 1), (64, 1), (64, 0.5), (64, 0.5),
                (64, 1), (62, 1), (62, 1), (64, 1), (62, 2), (66, 2)
            ],
            "instrument": 0,
            "bpm": 150
        },
        "5": {
            "name": "Für Elise (Opening)",
            "melody": [
                (64, 0.5), (63, 0.5), (64, 0.5), (63, 0.5), (64, 0.5), (59, 0.5), (62, 0.5), (60, 0.5),
                (57, 1), (0, 0.5), (55, 0.5), (57, 0.5), (60, 0.5), (62, 1), (0, 0.5), (60, 0.5),
                (62, 0.5), (64, 1), (0, 0.5), (59, 0.5), (62, 0.5), (64, 0.5), (65, 1), (0, 0.5),
                (64, 0.5), (63, 0.5), (64, 0.5), (63, 0.5), (64, 0.5), (59, 0.5), (62, 0.5), (60, 0.5),
                (57, 1)
            ],
            "instrument": 0,
            "bpm": 90
        },
        "6": {
            "name": "Mary Had a Little Lamb",
            "melody": [
                (64, 1), (62, 1), (60, 1), (62, 1), (64, 1), (64, 1), (64, 2),
                (62, 1), (62, 1), (62, 2), (64, 1), (67, 1), (67, 2),
                (64, 1), (62, 1), (60, 1), (62, 1), (64, 1), (64, 1), (64, 1), (64, 1),
                (62, 1), (62, 1), (64, 1), (62, 1), (60, 2)
            ],
            "instrument": 0,
            "bpm": 120
        }
    }

    while True:
        print("\n=== MIDI Melody Player ===")
        print("Available Melodies:")
        for key, melody in melodies.items():
            print(f"{key}: {melody['name']} (BPM: {melody['bpm']})")
        print("q: Quit")
        
        choice = input("\nSelect a melody to play (1-6) or 'q' to quit: ")
        
        if choice.lower() == 'q':
            print("Goodbye!")
            break
            
        if choice in melodies:
            selected = melodies[choice]
            print(f"\nPlaying {selected['name']}... (Press Ctrl+C to stop)")
            try:
                play_melody(
                    selected["melody"],
                    bpm=selected["bpm"],
                    instrument=selected["instrument"]
                )
            except KeyboardInterrupt:
                print("\nPlayback stopped.")
        else:
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()