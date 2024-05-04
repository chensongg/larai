from deepgram_client import deepgram_client

from deepgram import LiveTranscriptionEvents, LiveOptions, Microphone, LiveClient


class SST():
    def __init__(self, utternce_end_ms) -> None:
        self.dg_connection: LiveClient = deepgram_client.listen.live.v("1")
        print(self.dg_connection)
        self.utterance_end_ms = utternce_end_ms
        self.dg_connection.on(LiveTranscriptionEvents.Open, on_open)
        self.dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        self.dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        self.dg_connection.on(LiveTranscriptionEvents.SpeechStarted, on_speech_started)
        self.dg_connection.on(LiveTranscriptionEvents.Error, on_error)
        self.dg_connection.on(LiveTranscriptionEvents.Close, on_close)

    def set_on_utterance_end(self, on_utterance_end):
        self.dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, on_utterance_end)

    def start(self):
        options: LiveOptions = LiveOptions(
            model="nova-2",
            punctuate=True,
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            # To get UtteranceEnd, the following must be set:
            interim_results=True,
            utterance_end_ms=self.utterance_end_ms,
            vad_events=True,
        )
        self.dg_connection.start(options)
        # create microphone
        self.microphone = Microphone(self.dg_connection.send)

        # start microphone
        self.microphone.start()

    def stop(self):
        self.microphone.finish()
        self.dg_connection.finish()

def on_open(self, open, **kwargs):
    print(f"\n\n{open}\n\n")

def on_message(self, result, **kwargs):
    sentence = result.channel.alternatives[0].transcript
    if len(sentence) == 0:
        return
    print(f"speaker: {sentence}")

def on_metadata(self, metadata, **kwargs):
    print(f"\n\n{metadata}\n\n")

def on_error(self, error, **kwargs):
    print(f"\n\n{error}\n\n")

def on_close(self, close, **kwargs):
    print(f"\n\n{close}\n\n")

def on_speech_started(self, speech_started, **kwargs):
    print(f"\n\n{speech_started}\n\n")

def on_utterance_end(self, utterance_end, **kwargs):
    print(f"\n\n{utterance_end}\n\n")

if __name__ == "__main__":
    sst = SST(on_speech_started=on_speech_started, on_utterance_end=on_utterance_end, utternce_end_ms="2000")
    sst.start()
    input("Press Enter to stop recording...\n\n")
    sst.stop()