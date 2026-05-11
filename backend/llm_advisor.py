import os
import requests


API_URL = (
    "https://api-inference.huggingface.co/models/"
    "google/flan-t5-large"
)


def generate_llm_summary(score, effort, findings):
    token = os.getenv("HF_TOKEN")

    if not token:
        return None

    findings_text = "\n".join(
        [
            f"- {item['keyword']}: {item['issue']}. "
            f"Recommendation: {item['recommendation']}"
            for item in findings
        ]
    )

    prompt = f"""
You are an expert AMD ROCm migration advisor.

ROCm Readiness Score: {score}/100
Estimated Effort: {effort}

Findings:
{findings_text}

Write a concise executive summary (4-6 sentences)
explaining:
1. Migration risk.
2. Most critical blockers.
3. Recommended migration priorities.
4. Overall recommendation.
"""

    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 250,
            "temperature": 0.2,
        },
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=60,
        )

        if response.status_code != 200:
            return None

        result = response.json()

        if isinstance(result, list):
            return result[0]["generated_text"].replace(
                prompt, ""
            ).strip()

        return None

    except Exception:
        return None