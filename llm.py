import requests
import os

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"


def generate_sql(prompt, api_key=None):
    key = api_key or os.environ.get("GROQ_API_KEY", "")

    if not key:
        return "LLM_ERROR: No API key provided. Enter your Groq API key in the sidebar."

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 1024
            },
            timeout=30
        )

        if response.status_code == 401:
            return "LLM_ERROR: Invalid API key. Check your Groq API key."
        if response.status_code == 429:
            return "LLM_ERROR: Rate limit exceeded. Wait a moment and retry."

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        return "LLM_ERROR: Request timed out. Please try again."
    except Exception as e:
        return f"LLM_ERROR: {str(e)}"
