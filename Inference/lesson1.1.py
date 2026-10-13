# pip install tiktoken
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")  # OpenAI's tokenizer; Claude's differs, but the idea is the same

samples = [
    "the cat",
    "pembrolizumab",
    "Contraindicated in patients with known hypersensitivity",
    "FDA-2024-D-1234",
]

for text in samples:
    ids = enc.encode(text)      # str -> list[int]
    # TODO: turn each id back into its text piece (hint: enc.decode takes a list)
    pieces = ...
    print(f"{len(ids):>3} tokens | {pieces}")