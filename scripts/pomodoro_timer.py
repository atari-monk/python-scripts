import math
import struct
import time
import pyaudio
import threading
from queue import Queue

class Beeper:
    def __init__(self):
        self.sample_rate = 44100
        self.p = pyaudio.PyAudio()
        self.queue = Queue()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        
    def _generate_tone(self, frequency, duration, amplitude=0.5):
        num_samples = int(self.sample_rate * duration)
        samples = (amplitude * math.sin(2 * math.pi * frequency * (i / self.sample_rate)) for i in range(num_samples))
        return b''.join(struct.pack('f', s) for s in samples)
    
    def _run(self):
        stream = None
        try:
            stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=self.sample_rate, output=True)
            while True:
                frequency, duration, repetitions = self.queue.get()
                samples = self._generate_tone(frequency, duration)
                for _ in range(repetitions):
                    if stream.is_active():
                        stream.write(samples)
                        time.sleep(0.1)
        finally:
            if stream:
                stream.stop_stream()
                stream.close()
    
    def play(self, frequency, duration, repetitions=1):
        self.queue.put((frequency, duration, repetitions))
    
    def __del__(self):
        self.p.terminate()

class PomodoroTimer:
    def __init__(self):
        self.beeper = Beeper()
        self.running = False
        self.session_count = 0
        self.work_duration = 25 * 60  # 25 minutes
        self.short_break = 5 * 60      # 5 minutes
        self.long_break = 15 * 60     # 15 minutes
        self.sessions_before_long_break = 4

    def start(self):
        self.running = True
        self.session_count = 0
        
        try:
            while self.running:
                self.session_count += 1
                
                # Work session
                print(f"\n🍅 WORK SESSION {self.session_count}/{self.sessions_before_long_break} (25 min)")
                self._countdown(self.work_duration)
                self.beeper.play(880.0, 0.3, 2)  # High pitch double beep
                
                # Check if it's time for long break
                if self.session_count % self.sessions_before_long_break == 0:
                    # Long break
                    print("\n🌴 LONG BREAK (15 min)")
                    self._countdown(self.long_break)
                    self.beeper.play(440.0, 0.3, 3)  # Low pitch triple beep
                else:
                    # Short break
                    print("\n☕ SHORT BREAK (5 min)")
                    self._countdown(self.short_break)
                    self.beeper.play(660.0, 0.3, 2)  # Medium pitch double beep
                
        except KeyboardInterrupt:
            self.stop()

    def _countdown(self, seconds):
        for remaining in range(seconds, 0, -1):
            if not self.running:
                break
            mins, secs = divmod(remaining, 60)
            print(f"\rTime remaining: {mins:02d}:{secs:02d}", end="")
            time.sleep(1)
        print("\r" + " " * 30 + "\r", end="")  # Clear line

    def stop(self):
        self.running = False
        print("\n⏹️ Pomodoro stopped")

def main():
    print("""
    🍅 Pomodoro Timer
    -----------------
    Work: 25 min
    Short Break: 5 min
    Long Break: 15 min
    Long break after 4 sessions
    
    Press Ctrl+C to stop
    """)
    
    timer = PomodoroTimer()
    timer.start()

if __name__ == "__main__":
    main()