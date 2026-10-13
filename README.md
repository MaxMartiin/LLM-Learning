# LLM Learning

A hands-on log of learning LLM engineering in Python. Each lesson is a small script I wrote, ran, and debugged. Lessons 1.1–1.2 run locally; 1.3–1.4 call the Claude API (Claude Haiku 5.5).

## How I'm learning

Guided curriculum with an AI tutor. For each topic I get the concept, a code skeleton with TODOs, and a prediction to make before running. I write the implementation, run it, compare the results to my prediction, and debug what breaks.

## 1. Inference

| File           | What it covers                                                                                                   |
| -------------- | ---------------------------------------------------------------------------------------------------------------- |
| `lesson1.1.py` | Tokenization: how text becomes token IDs, and why rare words and ID strings use more tokens                      |
| `lesson1.2.py` | Sampling: a softmax + temperature sampler built from scratch, 1,000 draws per temperature                        |
| `lesson1.3.py` | Latency and streaming: measures time-to-first-token, total time, and decode speed on live API calls              |
| `lesson1.4.py` | Cost and output control: per-call cost from token usage, prompt caching, and structured extraction with Pydantic |
| `envcheck.py`  | Debug script I used to track down why my API key wasn't loading from `.env`                                      |

## What I learned

- **Prefill is fast, decode is slow.** Growing the input 700× (23 → 16K tokens) added only ~0.66s to time-to-first-token. Prefill reads input in parallel (roughly 24K tokens/sec here); decode writes one token at a time (~170 tokens/sec).
- **Big inputs cost money more than time.** In the 16K-token test, input was ~99% of the call's cost.
- **Prompt caching works.** A cached call cost ~82% less than the same call uncached. Output tokens aren't discounted, so they become the main cost once input is cached.
- **Current Claude models reject `temperature`.** The SDK raised a `TypeError`. Consistent output now comes from clear prompts, structured outputs, and validating results in code.
- **Thinking tokens share the `max_tokens` budget.** One 200-token call spent everything on hidden thinking and returned no text, so I check `stop_reason` and content block types before trusting a response.
- **Length instructions are soft.** Asking for "about 600 words" produced 1,100+ and hit the token cap. `max_tokens` is a hard cutoff, not a target.

## Setup

```
py -m pip install anthropic python-dotenv pydantic tiktoken
```

Create a `.env` file in the repo root (it's git-ignored):

```
ANTHROPIC_API_KEY=your-key-here
```

## Next

Data collection and sanitation → RAG → agents.
