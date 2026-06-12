from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_quiz(context):

    prompt = f"""
Generate 5 multiple-choice questions from the content below.

Return ONLY valid JSON.

Format:

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "A"
  }}
]

Rules:
1. Create exactly 5 questions.
2. Each question must have 4 options.
3. answer must be ONLY A, B, C, or D.
4. Do not return explanations.
5. Do not return markdown.
6. Return JSON only.

Content:

{context}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    quiz_text = response.choices[0].message.content

    # Remove markdown if model accidentally returns it
    quiz_text = quiz_text.replace("```json", "")
    quiz_text = quiz_text.replace("```", "")
    quiz_text = quiz_text.strip()

    try:
        quiz = json.loads(quiz_text)
        return quiz

    except Exception as e:

        print("JSON Parsing Error")
        print(quiz_text)

        raise Exception(
            "Unable to parse quiz JSON returned by Groq."
        )