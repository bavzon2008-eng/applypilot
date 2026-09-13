import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

ANAKIN_API_KEY = os.getenv("ANAKIN_API_KEY")
ANAKIN_BASE_URL = "https://api.anakin.io/v1"


def get_headers():
    if not ANAKIN_API_KEY:
        raise RuntimeError("ANAKIN_API_KEY is missing from .env")

    return {
        "X-API-Key": ANAKIN_API_KEY,
        "Content-Type": "application/json",
    }


def search_web(prompt, limit=5):
    response = requests.post(
        f"{ANAKIN_BASE_URL}/search",
        headers=get_headers(),
        json={
            "prompt": prompt,
            "limit": limit,
        },
        timeout=60,
    )

    response.raise_for_status()
    return response.json()

def resolve_wire_actions(query):
    response = requests.get(
        f"{ANAKIN_BASE_URL}/wire/resolve",
        headers=get_headers(),
        params={"q": query},
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


def run_wire_action(action_id, params):
    response = requests.post(
        f"{ANAKIN_BASE_URL}/wire/task",
        headers=get_headers(),
        json={
            "action_id": action_id,
            "params": params,
        },
        timeout=60,
    )

    response.raise_for_status()
    return response.json()


def get_wire_job(job_id):
    response = requests.get(
        f"{ANAKIN_BASE_URL}/wire/jobs/{job_id}",
        headers=get_headers(),
        timeout=60,
    )

    response.raise_for_status()
    return response.json()


def wait_for_wire_job(job_id, max_attempts=12):
    for _ in range(max_attempts):
        result = get_wire_job(job_id)

        status = result.get("status")

        if status in ["completed", "ok", "success"]:
            return result

        if status in ["failed", "error"]:
            raise RuntimeError(
                f"Anakin Wire job failed: {result}"
            )

        time.sleep(3)

    raise TimeoutError(
        "Anakin Wire job did not finish in time"
    )