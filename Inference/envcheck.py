import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

path = find_dotenv(usecwd=True)
print("cwd:       ", Path.cwd())
print(".env found:", path or "NOT FOUND")
print("loaded:    ", load_dotenv(path))
key = os.environ.get("ANTHROPIC_API_KEY")
print("key set:   ", bool(key), "| prefix:", key[:7] if key else None, "| length:", len(key) if key else 0)
from dotenv import dotenv_values
print("names:     ", [repr(k) for k in dotenv_values(path)])