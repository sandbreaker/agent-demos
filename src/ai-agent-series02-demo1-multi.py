import os
import json
from anthropic import AnthropicBedrock

class Agent:
    def __init__(self, name, specialty):
        self.name = name
        self.specialty = specialty
        self.client = AnthropicBedrock()

    def process_data(self, data):
        prompt = f"You are an AI assistant specializing in {self.specialty}. Please process this data: {data}"
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

        return response.content[0].text

class MultiAgentSystem:
    def __init__(self):
        self.agents = [
            Agent("Alice", "data cleaning"),
            Agent("Bob", "data analysis"),
            # Agent("Charlie", "report generation")
        ]

    def collaborate(self, input_data):
        result = input_data
        for agent in self.agents:
            print(f"{agent.name} ({agent.specialty}) is processing the data...")
            result = agent.process_data(result)
            print(f"{result}")
        return result

# Example usage
if __name__ == "__main__":
    # Sample input data
    raw_data = "Sales data: Product A - 100 units, Product B - 150 units, Product C - 75 units"

    # Create and run the multi-agent system
    mas = MultiAgentSystem()
    final_result = mas.collaborate(raw_data)

    print("\nFinal result:")
    print(final_result)