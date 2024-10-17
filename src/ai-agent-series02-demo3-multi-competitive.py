import os
import random
import time
from anthropic import AnthropicBedrock


class NumberGuessingAgent:
    def __init__(self, name):
        self.name = name
        self.client = AnthropicBedrock()
        self.min = 1
        self.max = 100
        self.guesses = []

    def make_guess(self):
        prompt = f"We are playing a number guessing game. The secret number is between {self.min} and {self.max}. My previous guesses were: {self.guesses}. Based on this information, what would be the best next guess? Respond with just the number, nothing else."

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]

        response = self.client.messages.create(
            model="anthropic.claude-3-sonnet-20240229-v1:0",
            max_tokens=500,
            messages=messages,
            temperature=0.5
        )
        
        guess = int(response.content[0].text.strip())
        self.guesses.append(guess)

        return guess

    def update_range(self, guess, is_higher):
        if is_higher:
            self.min = max(self.min, guess + 1)
        else:
            self.max = min(self.max, guess - 1)

class NumberGuessingGame:
    def __init__(self):
        self.agents = [
            NumberGuessingAgent("Agent1"),
            NumberGuessingAgent("Agent2")
        ]
        self.secret_number = random.randint(1, 100)
        # self.secret_number = 1
        self.max_rounds = 10

    def play_game(self):
        print(f"Starting Number Guessing Game! The secret number is between 1 and 100.")
        
        for round in range(1, self.max_rounds + 1):
            print(f"\n--Round {round}:")
            for agent in self.agents:
                print(f"{agent.name}'s turn...")
                guess = agent.make_guess()
                print(f"{agent.name} guesses: {guess}")
                
                if guess == self.secret_number:
                    print(f"{agent.name} wins! The secret number was {self.secret_number}.")
                    return
                
                is_higher = guess < self.secret_number
                hint = "higher" if is_higher else "lower"
                print(f"The secret number is {hint} than {guess}.")
                
                # Update both agents' ranges
                for a in self.agents:
                    a.update_range(guess, is_higher)
                
                time.sleep(1)  # Add a small delay for readability

        print(f"\nGame Over! No one guessed the number. The secret number was {self.secret_number}.")

# Example usage
if __name__ == "__main__":
    game = NumberGuessingGame()
    game.play_game()