import os

import openai

openai.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_KEY")


def call_llm(prompt: str, model="gpt-4o-mini", temperature=0.7, max_tokens=1000):
    if not openai.api_key:
        return f"[Mock LLM response] {prompt[:200]}"

    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content
