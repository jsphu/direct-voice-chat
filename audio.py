import pyaudio
import logging

class AudioManager:
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream_in = None
        self.stream_out = None

    def start_streams(self):
        """Initializes both input (mic) and output (speaker) streams."""
        try:
            # Output stream (Playback)
            self.stream_out = self.p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                output=True,
                frames_per_buffer=self.CHUNK
            )

            # Input stream (Capture)
            self.stream_in = self.p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )
            return True
        except Exception as e:
            logging.error(f"Failed to initialize audio streams: {e}")
            return False

    def read_chunk(self):
        """Reads a chunk of audio from the microphone."""
        if self.stream_in:
            try:
                return self.stream_in.read(self.CHUNK, exception_on_overflow=False)
            except Exception as e:
                logging.debug(f"Error reading audio chunk: {e}")
        return None

    def write_chunk(self, data):
        """Writes a chunk of audio to the speaker."""
        if self.stream_out:
            try:
                self.stream_out.write(data)
            except Exception as e:
                logging.debug(f"Error writing audio chunk: {e}")

    def close(self):
        """Closes all streams and terminates PyAudio."""
        if self.stream_in:
            self.stream_in.stop_stream()
            self.stream_in.close()
        if self.stream_out:
            self.stream_out.stop_stream()
            self.stream_out.close()
        self.p.terminate()
