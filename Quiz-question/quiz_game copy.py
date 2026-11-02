"""
Quiz Game (CLI Based)
---------------------
Features:
  - Multiple questions (multiple choice)
  - Score tracking
  - Random question selection
"""

import random

QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": 3,
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "answer": 2,
    },
    {
        "question": "What is 12 x 8?",
        "options": ["96", "86", "108", "98"],
        "answer": 1,
    },
    {
        "question": "Which language is used to style web pages?",
        "options": ["HTML", "Python", "CSS", "SQL"],
        "answer": 3,
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["Charles Dickens", "William Shakespeare", "Mark Twain", "Jane Austen"],
        "answer": 2,
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "answer": 4,
    },
    {
        "question": "In Python, which keyword defines a function?",
        "options": ["func", "def", "function", "lambda"],
        "answer": 2,
    },
    {
        "question": "How many continents are there?",
        "options": ["5", "6", "7", "8"],
        "answer": 3,
    },
    {
        "question": "What gas do plants absorb from the air?",
        "options": ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"],
        "answer": 3,
    },
    {
        "question": "Which data structure uses LIFO order?",
        "options": ["Queue", "Stack", "Array", "Tree"],
        "answer": 2,
    },
]


def ask_number(prompt, low, high):
    """Keep asking until the user enters a number between low and high."""
    while True:
        raw = input(prompt).strip()
        if raw.isdigit() and low <= int(raw) <= high:
            return int(raw)
        print(f"  Please enter a number between {low} and {high}.")


def ask_question(number, total, q):
    """Show one question and return True if answered correctly."""
    print(f"\nQuestion {number}/{total}: {q['question']}")
    for i, option in enumerate(q["options"], start=1):
        print(f"  {i}. {option}")

    choice = ask_number("Your answer (1-4): ", 1, len(q["options"]))

    if choice == q["answer"]:
        print("  Correct!")
        return True

    correct_text = q["options"][q["answer"] - 1]
    print(f"  Wrong! The correct answer was: {correct_text}")
    return False


def get_rating(percent):
    if percent == 100:
        return "Perfect score! Outstanding!"
    if percent >= 70:
        return "Great job!"
    if percent >= 40:
        return "Not bad, keep practicing!"
    return "Better luck next time!"


def play_round():
    print("\nHow many questions would you like to answer?")
    count = ask_number(f"Enter a number (1-{len(QUESTIONS)}): ", 1, len(QUESTIONS))

    # random.sample picks unique random questions (no repeats in a round)
    selected = random.sample(QUESTIONS, count)
    score = 0

    for i, q in enumerate(selected, start=1):
        if ask_question(i, count, q):
            score += 1

    percent = score / count * 100
    print("\n" + "=" * 35)
    print(f"  Final Score: {score}/{count} ({percent:.0f}%)")
    print(f"  {get_rating(percent)}")
    print("=" * 35)
    return score, count


def main():
    print("=" * 35)
    print("     WELCOME TO THE QUIZ GAME")
    print("=" * 35)

    total_score = 0
    total_asked = 0

    while True:
        score, count = play_round()
        total_score += score
        total_asked += count

        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            break

    print(f"\nOverall across all rounds: {total_score}/{total_asked} correct.")
    print("Thanks for playing!")


if __name__ == "__main__":
    main()