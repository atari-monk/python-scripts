import math
import struct
import time
import pyaudio
import threading
from queue import Queue

# ===== CONFIGURATION =====
INTERVAL_CONFIG = [
    {
        'name': '5-minute',
        'interval': 5 * 60,  # 5 minutes in seconds
        'frequency': 800,    # Hz
        'duration': 0.3,     # seconds
        'repetitions': 1,    # number of beeps
        'message': '5 minutes have passed'
    },
    {
        'name': '15-minute',
        'interval': 15 * 60,  # 15 minutes in seconds
        'frequency': 1000,    # Hz
        'duration': 0.3,      # seconds
        'repetitions': 2,     # number of beeps
        'message': '15 minutes have passed'
    },
    {
        'name': '60-minute',
        'interval': 60 * 60,  # 60 minutes in seconds
        'frequency': 1200,    # Hz
        'duration': 0.3,      # seconds
        'repetitions': 3,     # number of beeps
        'message': '1 hour has passed'
    }
]
# ===== END CONFIG =====

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

class IntervalBeeper:
    def __init__(self):
        self.beeper = Beeper()
        self.running = False

    def start(self):
        self.running = True
        last_times = {item['name']: time.time() for item in INTERVAL_CONFIG}
        
        print("\n🔊 Starting interval beeper (Ctrl+C to stop)")
        for item in INTERVAL_CONFIG:
            mins = item['interval'] // 60
            print(f"{item['name']}: every {mins} min - {item['repetitions']} beep(s) at {item['frequency']}Hz")
        
        try:
            while self.running:
                current_time = time.time()
                
                for item in INTERVAL_CONFIG:
                    if current_time - last_times[item['name']] >= item['interval']:
                        self.beeper.play(
                            frequency=item['frequency'],
                            duration=item['duration'],
                            repetitions=item['repetitions']
                        )
                        print(f"\n⏰ {item['message']} ({time.strftime('%H:%M:%S')})")
                        last_times[item['name']] = current_time
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.stop()
            
    def stop(self):
        self.running = False
        print("\n⏹️ Beeper stopped")

def main():
    print("""
    ⏱️ Interval Beeper
    -----------------
    Running with pre-configured intervals:
    """)
    
    for item in INTERVAL_CONFIG:
        print(f"- {item['name']}: every {item['interval']//60} min")
    
    beeper = IntervalBeeper()
    beeper.start()

if __name__ == "__main__":
    main()