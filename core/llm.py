# llm_client.py
import os
import openai

openai.api_key = os.getenv("OPENAI_KEY")

def call_llm(prompt: str, model="gpt-4o-mini", temperature=0.7, max_tokens=1000):
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content