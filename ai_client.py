import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is missing from .env")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

MODEL = "inclusionai/ling-3.0-flash-sante:free"

def analyze_opportunities(profile, opportunities):
    today = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""
You are ApplyPilot, an autonomous opportunity application agent.

TODAY'S DATE:
{today}

USER PROFILE:
{json.dumps(profile, indent=2)}

LIVE WEB OPPORTUNITIES:
{json.dumps(opportunities, indent=2)}

Your job is to carefully analyze every opportunity.

IMPORTANT RULES:

1. CHECK WHETHER THE OPPORTUNITY IS CURRENTLY ACTIVE.

2. Look for evidence such as:
   - expired
   - listing expired
   - applications closed
   - no longer accepting applications
   - position filled
   - deadline has passed
   - closing date in the past

3. If the opportunity is clearly expired or closed:
   - eligibility = "low"
   - action = "SKIP"
   - score must be 0-20
   - explain that the opportunity is no longer active
   - NEVER recommend APPLY_NOW

4. Do NOT assume that "no deadline stated" means the opportunity is active.

5. If there is no deadline information and there is no evidence that
   the opportunity is expired, you may mark the deadline as:
   "No deadline stated"

6. Only recommend APPLY_NOW when the opportunity appears to be
   currently active AND is a strong match.

7. Consider:
   - user education
   - skills
   - location
   - goal
   - eligibility
   - deadline
   - current/expired status
   - relevance

8. Match score must be from 0-100.

9. Recommended actions:
   - APPLY_NOW
   - PREPARE
   - SKIP

Return ONLY valid JSON.

Use exactly this structure:

{{
  "recommendations": [
    {{
      "title": "...",
      "url": "...",
      "score": 0,
      "eligibility": "high/medium/low/unknown",
      "matching_skills": [],
      "missing_requirements": [],
      "deadline": "...",
      "status": "active/expired/closed/unknown",
      "action": "APPLY_NOW/PREPARE/SKIP",
      "reason": "..."
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a precise opportunity analysis agent. "
                    "Never recommend expired or closed opportunities. "
                    "Return valid JSON only."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.1,
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("AI returned an empty response")

        # Clean common model formatting before JSON parsing
    content = content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "", 1)
        content = content.replace("```", "")
        content = content.strip()

    # Remove accidental text before/after the JSON object
    start = content.find("{")
    end = content.rfind("}")

    if start != -1 and end != -1:
        content = content[start:end + 1]

    try:
        return json.loads(content)

    except json.JSONDecodeError:
        # Some models return Python-style dictionaries using single quotes.
        # Try converting that representation safely.
        import ast

        try:
            parsed = ast.literal_eval(content)

            if isinstance(parsed, dict):
                return parsed

            raise RuntimeError(
                "AI returned a valid object, but it was not a JSON object."
            )

        except Exception as parse_error:
            raise RuntimeError(
                "AI returned invalid structured output.\n\n"
                f"Raw AI response:\n{content}\n\n"
                f"Parser error: {parse_error}"
            )