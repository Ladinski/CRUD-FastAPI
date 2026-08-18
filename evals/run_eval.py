import json
import requests
from pathlib import Path


CASES_PATH = Path(__file__).parent / "cases.json"
API_URL = "http://127.0.0.1:8000/tasks/analyze"


with CASES_PATH.open("r", encoding="utf-8") as file:
    cases = json.load(file)


passed = 0
failed = []


for index, case in enumerate(cases, start=1):
    response = requests.post(
        API_URL,
        json={"text": case["text"]},
        timeout=40
    )

    if response.status_code != 200:
        failed.append({
            "case": index,
            "text": case["text"],
            "error": f"HTTP {response.status_code}"
        })
        continue

    result = response.json()

    category_match = (
        result["category"] == case["expected_category"]
    )

    priority_match = (
        result["priority"] == case["expected_priority"]
    )

    if category_match and priority_match:
        passed += 1
    else:
        failed.append({
            "case": index,
            "text": case["text"],
            "expected_category": case["expected_category"],
            "actual_category": result["category"],
            "expected_priority": case["expected_priority"],
            "actual_priority": result["priority"]
        })


total = len(cases)

print(f"Score: {passed}/{total}")
print(f"Accuracy: {(passed / total) * 100:.1f}%")

if failed:
    print("\nFailed cases:")

    for failure in failed:
        print(json.dumps(failure, indent=2))