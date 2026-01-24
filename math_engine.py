import random

def generate_question(level=9):
    qtype = random.choice(["linear", "distance", "area", "exponents"])

    if qtype == "linear":
        return {
            "question": "Solve: 3(2x − 5) − 4 = 2x + 7",
            "answer": "5"
        }

    if qtype == "distance":
        return {
            "question": "Find distance between points (−2, 3) and (4, −3)",
            "answer": "10"
        }

    if qtype == "area":
        return {
            "question": "Find area of a circle of radius 7 cm (π = 22/7)",
            "answer": "154"
        }

    if qtype == "exponents":
        return {
            "question": "Evaluate: (2³ × 2⁵) / 2⁴",
            "answer": "16"
        }