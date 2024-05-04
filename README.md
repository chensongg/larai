To config
add `.env`
```
DG_API_KEY=<your deepgram api key>
LLM_MODEL=llama3-70b-8192
```
add `LLM_CONFIG_LIST`
```
[
    {
        "model": "llama3-70b-8192",
        "base_url": "https://api.groq.com/openai/v1",
        "api_key": "<your groq api key>"
    }
]
```

To run

```
python -m venv venv
source venv/bin/activate
pip install -r requirements-lock.txt
python app.py
```
