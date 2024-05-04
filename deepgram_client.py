import os
from deepgram import DeepgramClient, DeepgramClientOptions

from dotenv import load_dotenv
load_dotenv(".env")

config = DeepgramClientOptions(
    options={"keepalive": "true"}
)

deepgram_client = DeepgramClient(api_key=os.getenv('DG_API_KEY'), config=config)
