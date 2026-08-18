# Job card

What it does: Classifies a task into a category and priority.

Input: { "text": "string, 1-1000 characters" }

Output: {
  "category": one of [work, study, personal, other],
  "priority": one of [low, medium, high],
  "confidence": 0.0-1.0,
  "reason": "one short sentence"
}

It must never: invent a category outside the allowed list, return free text instead of the required JSON object, or make decisions outside task classification.

When unsure it should: return category "other" with low confidence instead of guessing.