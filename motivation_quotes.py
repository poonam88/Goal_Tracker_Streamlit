import random

def get_motivation():
    quotes = [
        "Believe in yourself and all that you are.",
        "You are stronger than you think.",
        "Small steps every day lead to big results.",
        "Don't watch the clock; do what it does. Keep going.",
        "Success is the sum of small efforts repeated daily.",
        "Discipline is the bridge between goals and accomplishment.",
        "Dream big. Start small. Act now.",
        "Keep going. Everything you need will come to you."
    ]
    return random.choice(quotes)
