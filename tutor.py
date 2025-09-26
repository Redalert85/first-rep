from openai import OpenAI
from dotenv import load_dotenv
import os, pathlib, sys

# Load .env explicitly
ENV_PATH = pathlib.Path(__file__).with_name(".env")
load_dotenv(dotenv_path=ENV_PATH)

api_key = os.getenv("OPENAI_API_KEY")
print("Key present:", bool(api_key))
if not api_key:
    print("OPENAI_API_KEY missing")
    sys.exit(1)

client = OpenAI(api_key=api_key)

# Test prompt (no mention of API key!)
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"system","content":"You are a concise bar-prep tutor."},
        {"role":"user","content":"Give a one-sentence definition of the Parol Evidence Rule."}
    ],
    temperature=0.2,
)

print("MODEL:", resp.model)
print("REPLY:", resp.choices[0].message.content)
