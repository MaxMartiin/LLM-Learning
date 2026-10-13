import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-haiku-5-5"
IN_PRICE, OUT_PRICE = 0.10, 0.50          # $ per 1M tokens (Haiku 5.5, prompts ≤100K)
CACHE_WRITE, CACHE_READ = 0.125, 0.01

def cost(usage) -> float:
    # TODO: return the dollar cost of one call using all four usage fields:
    #   input_tokens, cache_creation_input_tokens, cache_read_input_tokens, output_tokens
    # Gotcha: the cache fields can be None. Treat None as 0.
    input_cost  = (usage.input_tokens) * IN_PRICE / 1_000_000
    cache_write_cost = (usage.cache_creation_input_tokens or 0) * CACHE_WRITE / 1_000_000
    cache_read_cost = (usage.cache_read_input_tokens or 0) * CACHE_READ / 1_000_000
    output_cost = (usage.output_tokens) * OUT_PRICE / 1_000_000
    return input_cost + cache_write_cost + cache_read_cost + output_cost

# ---- Part A: caching ----
DOC = "The sponsor must submit safety data to the agency. " * 300   # ~5K tokens, identical every call

for question in ["Summarize the document in one sentence.",
                 "How many distinct facts does it state?"]:
    r = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        cache_control={"type": "ephemeral"},
        system=DOC,
        messages=[{"role": "user", "content": question}],
    )
    u = r.usage
    print(f"write={u.cache_creation_input_tokens} read={u.cache_read_input_tokens} "
          f"uncached={u.input_tokens} out={u.output_tokens} cost=${cost(u):.6f}")

# ---- Part B: structured output ----
LABEL = """ZENTRAVA (velorimab) injection. FICTIONAL label for practice.
INDICATIONS AND USAGE: Treatment of adults with moderate-to-severe plaque psoriasis.
DOSAGE AND ADMINISTRATION: 150 mg by IV infusion every 4 weeks.
WARNINGS AND PRECAUTIONS: Serious infections; hypersensitivity reactions; avoid live vaccines."""

class DrugLabel(BaseModel):
    # TODO: brand_name, generic_name, indication, dose, warnings (a list of strings)
    brand_name: str
    generic_name: str
    indication: str
    dose: str
    warnings: list[str]

r = client.messages.parse(
    model=MODEL,
    max_tokens=1000,
    messages=[{"role": "user", "content": f"Extract the fields from this drug label:\n\n{LABEL}"}],
    output_format=DrugLabel,
)
print(r.stop_reason)
print(r.parsed_output)
# TODO: print only the warnings, one per line
for warning in r.parsed_output.warnings:
    print(warning)