# pip install anthropic

import time
import anthropic

from dotenv import load_dotenv
load_dotenv()   # loads .env so the client finds your key
client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY automatically
MODEL = "claude-haiku-5-5"                   # copy the current smallest Haiku model ID from the docs' Models page

def timed_stream(prompt: str, max_tokens: int):
    start = time.perf_counter()
    ttft = None
    with client.messages.stream(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            if ttft is None:
                ttft = time.perf_counter() - start
            print(text, end="", flush=True)
        final = stream.get_final_message()
    total = time.perf_counter() - start
    # TODO: print ttft, total, final.usage.input_tokens, final.usage.output_tokens,
    #       final.stop_reason, and decode speed in tokens/sec
    print("\nBlocks:", [b.type for b in final.content], "| stop:", final.stop_reason)
    ttft_str = f"{ttft:.3f}s" if ttft is not None else "no text"    
    print(f"TTFT: {ttft_str}, Total: {total:.3f}s")
    print(f"Input tokens: {final.usage.input_tokens}, Output tokens: {final.usage.output_tokens}")
    print(f"Stop reason: {final.stop_reason}")
    if ttft is not None and total > ttft:
        decode_speed = final.usage.output_tokens / (total - ttft)
        print(f"Decode speed: {decode_speed:.2f} tokens/sec")

timed_stream("Name 3 FDA centers. One line each.", max_tokens=100)
timed_stream("Explain the FDA drug approval process in about 600 words.", max_tokens=1500)
timed_stream("Explain the FDA drug approval process in about 600 words.", max_tokens=200)
filler = "The sponsor must submit safety data to the agency. " * 1000   # roughly 10K tokens
timed_stream(filler + "\nSummarize the text above in one sentence.", max_tokens=50)