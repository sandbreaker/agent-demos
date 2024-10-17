import os
import re
from anthropic import AnthropicBedrock

client = AnthropicBedrock()

def query_claude(prompt: str) -> str:
    message = client.messages.create(
        # model="anthropic.claude-3-5-sonnet-20240620-v1:0",
        model="anthropic.claude-3-sonnet-20240229-v1:0",
        max_tokens=256,
        messages=[
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
    )

    return message.content[0].text

food_healthiness = {
    "egg": "not healthy",
    "bread": "healthy",
    "cereal": "not healthy",
    "burger": "not healthy",
    "pizza": "not healthy",
    "salad": "healthy",
    "grass": "healthy",
    "chocolate": "healthy",
    "salmon": "healthy",
    "fries": "not healthy",
    "pasta": "not healthy",
    "pizza": "not healthy",
    "ice cream": "not healthy",
}

def lookup_food_healthiness(food):
    return food_healthiness.get(food.lower().strip(), "unknown")

def build_health_score(meals):
    meal_items = [f"{meal} ({lookup_food_healthiness(meal)})" for meal in meals]
    meal_description = ", ".join(meal_items)

    return meal_description

def analyze_my_meals(meals):
    meals_consumed = build_health_score(meals)

    prompt = f"""
        You're my AI agent a food rater who cares about my diet. Analyze if the following meals are healthy:

        {meals_consumed} 

        Please pay special attention to following output:
        - healthy
        - not healthy

        Please structure your response as follows:
        1. Brief overview of healty meals consumed
        2. Brief overview of unhealthy meals
        3. Brief explanation of the recommendation for tomorrow and if I can eat unhealthy meals
    """
    print(prompt)

    return query_claude(prompt)

def main():
    input_meals = input("What did you eat today (comma delimited)?")
    meals = input_meals.split(",")
    res = analyze_my_meals(meals)
    print(res)

if __name__ == "__main__":
    main()