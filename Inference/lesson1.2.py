import math, random
from collections import Counter

# Fake scores the model might give for the blank in: "The FDA has ___ the drug."
logits = {"approved": 4.0, "rejected": 2.5, "reviewed": 2.0, "banned": 0.5, "eaten": -2.0}

def softmax(logits: dict[str, float], temperature: float) -> dict[str, float]:
    # divide each score by temperature, apply math.exp,
    # then normalize so all values sum to 1
    scaled_logits = {token: score / temperature for token, score in logits.items()}
    exp_logits = {token: math.exp(score) for token, score in scaled_logits.items()}
    total = sum(exp_logits.values())
    probs = {token: score / total for token, score in exp_logits.items()}
    return probs

def sample(logits: dict[str, float], temperature: float) -> str:
    if temperature == 0:
        # greedy: return the highest-scoring token
        return max(logits, key=logits.get)
    probs = softmax(logits, temperature)
    return random.choices(list(probs), weights=list(probs.values()))[0]

for t in [0, 0.2, 1.0, 2.0]:
    counts = Counter(sample(logits, t) for _ in range(1000))
    print(t, counts.most_common())