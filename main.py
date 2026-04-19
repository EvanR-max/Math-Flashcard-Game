# main.py
import random
from datetime import date
import csv

# Functions

### Menu ###
def display_menu():
    """Display the main menu and return validated user choice."""
    while True:
        print("\nSelect one of the options:")
        print("(m)ultiplication")
        print("(a)ddition")
        print("(r)esults")
        print("(q)uit")
        choice = input("Enter your choice: ").lower()
        if choice in ['m', 'a', 'r', 'q']:
            return choice
        else:
            print("Invalid input. Please enter m, a, r, or q.")

### Addition ###

def make_addition_flashcard():
    """Make an addition flashcard and return (question, answer)."""
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    question = f"What is {x} + {y}? "
    answer = x + y
    return question, answer

### Multiplication ###

def make_multiplication_flashcard():
    """Make a multiplication flashcard and return (question, answer)."""
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    question = f"What is {x} X {y}? "
    answer = x * y
    return question, answer

### Validating number ###
# This section is making sure that what the user inputs is a numerical value and not a letter. An answer that makes sense. In this case it makes sense that it is a number
def get_valid_number(prompt):
    """Prompt user for a number, keep asking until valid."""
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            return int(user_input)
        else:
            print("Invalid input. Please enter a number.")

### Round ###

def play_round(operation, user_name):
    """Play 5 flashcards and return score."""
    score = 0
    total = 0
    for i in range(5):
        if operation == 'a':
            question, answer = make_addition_flashcard()
        else:
            question, answer = make_multiplication_flashcard()

        print(f"\nYour current score is {score} out of {total}")
        user_answer = get_valid_number(question)
        total += 1
        if user_answer == answer:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect, the correct answer was {answer}.")

    print(f"\nRound over! You scored {score} out of {total}")
    save_results(user_name, score)
    input("Press Enter to return to main menu...")
    return score

### Save Results ###

def save_results(user_name, score):
    """Save user's result to results.csv and keep best score per day."""
    today = date.today().isoformat()
    results = {}

    # Read existing results
    try:
        with open('results.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            for row in reader:
                name, d, s = row
                results[(name, d)] = int(s)
    except FileNotFoundError:
        pass  # File does not exist yet

    # Update if better score
    if (user_name, today) not in results or score > results[(user_name, today)]:
        results[(user_name, today)] = score

    # Write back to file
    with open('results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["User_name", "Date", "Score"])
        for (name, d), s in results.items():
            writer.writerow([name, d, s])

### Results ###

def display_results(user_name):
    """Display all results for a given user."""
    try:
        with open('results.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            found = False
            print(f"\nResults for {user_name}:")
            for row in reader:
                name, d, s = row
                if name == user_name:
                    print(f"Date: {d}, Score: {s}")
                    found = True
            if not found:
                print("No results found.")
    except FileNotFoundError:
        print("No results file found yet.")
    input("Press Enter to return to main menu...")

# Main Program

def main():
    print("Welcome to the Math Flashcard Game!")
    user_name = input("Please enter your name: ")

    while True:
        choice = display_menu()
        if choice == 'q':
            print("Thanks for playing! Goodbye!")
            break
        elif choice == 'r':
            display_results(user_name)
        else:
            play_round(choice, user_name)

# Only run main if this file is executed directly
if __name__ == "__main__":
    main()
