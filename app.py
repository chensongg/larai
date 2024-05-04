from tts import tts, play

from agents import start_next_session, respond


RESPONSE_FILENAME = "last.wav"
REC_SAMPLERATE = 32000
FRAME_DURATION_MS = 30
BLOCKSIZE = int(REC_SAMPLERATE * FRAME_DURATION_MS / 1000)

channels = [1]
mapping  = [c - 1 for c in channels]
downsample = 1

messages = [
    {
        "role": "system",
        "content": """
            You are Lara, a therapist AI trained in cognitive behavioral therapy.
            Always ask follow up questions related to the user's input. Please introduce yourself briefly if it's your first time speaking with the user.
        """,
    },
]

def main():
    message = start_next_session()
    while True:
        tts(message, RESPONSE_FILENAME)
        play(RESPONSE_FILENAME)
        resp = input('> ')
        if resp == 'exit':
            break
        message = respond(resp)

if __name__ == "__main__":
    main()
