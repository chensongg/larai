from src.tts import tts, play

from src.llm import start_next_session, respond, anderson, lara


RESPONSE_FILENAME = "last.wav"
REC_SAMPLERATE = 32000

def main():
    agent = anderson
    message = start_next_session(agent)
    def speak(message):
        tts(message, RESPONSE_FILENAME)
        play(RESPONSE_FILENAME)
    while True:
        speak(message)
        resp = input('> ')
        if resp == 'exit':
            respond("We are out of time, and must end the session.")
            speak(message)
            exit(0)
        message = respond(resp, agent)

if __name__ == "__main__":
    main()
