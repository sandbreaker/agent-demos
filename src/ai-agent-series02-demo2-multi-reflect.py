import os
import json
from anthropic import AnthropicBedrock

class Agent:
    def __init__(self, name, specialty):
        self.name = name
        self.specialty = specialty
        self.client = AnthropicBedrock()
        self.performance_history = []

    def process_task(self, task_description, data):
        # prompt = f"You are an AI assistant specializing in {self.specialty}. Please process this data: {data}"
        prompt = f"You are a {self.specialty} specialist. Please {task_description} based on the following data: {data}"
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

        result = response.content[0].text
        self.performance_history.append({"task": task_description, "result": result})

        return result

    def reflect(self):
        reflection_prompt = f"You are a {self.specialty} specialist. Please reflect on your recent performance and suggest improvements based on the following history: {json.dumps(self.performance_history)}"
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": reflection_prompt
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

        reflection = response.content[0].text
        print(f"{self.name}'s reflection: {reflection}")

        return reflection


class MultiAgentSystem:
    def __init__(self):
        self.client = AnthropicBedrock()
        self.agents = [
            Agent("Alice", "data cleaning and preprocessing"),
            Agent("Bob", "data analysis"),
            # Agent("Charlie", "data visualization"),
            # Agent("Dana", "insights generation"),
            # Agent("Eve", "report writing")
        ]
        self.system_performance_history = []

    def generate_report(self, raw_data):
        result = raw_data
        process_steps = []
        for agent in self.agents:
            print(f"{agent.name} ({agent.specialty}) is working on the task...")
            if agent.specialty == "data cleaning and preprocessing":
                task = "clean and preprocess the data"
            elif agent.specialty == "data analysis":
                task = "perform a comprehensive analysis of the data"
            elif agent.specialty == "data visualization":
                task = "create appropriate visualizations for the analyzed data"
            elif agent.specialty == "insights generation":
                task = "generate key insights from the analysis and visualizations"
            elif agent.specialty == "report writing":
                task = "write a comprehensive report summarizing the findings"
            
            result = agent.process_task(task, result)
            process_steps.append({"agent": agent.name, "task": task, "result": result})
        
        self.system_performance_history.append({"raw_data": raw_data, "process_steps": process_steps, "final_report": result})
        return result

    def system_reflect(self):
        reflection_prompt = f"You are an AI system designed to generate comprehensive reports. Please analyze the following performance history and suggest improvements to the overall process: {json.dumps(self.system_performance_history)}"
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": reflection_prompt
                    }
                ]
            }
        ]

        response = self.client.messages.create(
            model="anthropic.claude-3-sonnet-20240229-v1:0",
            max_tokens=1000,
            messages=messages,
            temperature=0.5
        )

        reflection = response.content[0].text
        print(f"System reflection: {reflection}")

        return reflection

    def collaborate(self, input_data):
        result = input_data
        for agent in self.agents:
            print(f"{agent.name} ({agent.specialty}) is processing the data...")
            result = agent.process_task(result)
            print(f"{result}")
        return result

# Example usage
if __name__ == "__main__":
    # Insight instruction. Skip for now.
    # raw_data = """
    # Sales data for a retail company over the past year:
    # - Monthly revenue figures
    # - Product category performance
    # - Customer demographics
    # - Seasonal trends
    # - Online vs in-store sales comparison
    # """
    raw_data = [
        {"date": "2023-01-01", "revenue": 1500, "product_category": "Electronics", "customer_age": 35, "sale_type": "Online"},
        {"date": "2023-01-02", "revenue": 2200, "product_category": "Clothing", "customer_age": 28, "sale_type": "In-store"},
        {"date": "2023-01-03", "revenue": 1800, "product_category": "Home", "customer_age": 45, "sale_type": "Online"},
        {"date": "2023-01-04", "revenue": 3000, "product_category": "Electronics", "customer_age": 52, "sale_type": "In-store"},
        {"date": "2023-01-05", "revenue": 2500, "product_category": "Food", "customer_age": 39, "sale_type": "Online"}
    ]

    # raw_data = """
    #     date: 2023-01-01, revenue:1500, product_category: Electronics, customer_age: 35, sale_type:Online
    #     date: 2023-01-02, revenue:2200, product_category: Clothing, customer_age: 35, sale_type:In-store
    # """

    # Create and run the report generation system
    report_system = MultiAgentSystem()
    final_report = report_system.generate_report(raw_data)

    print("\n\n\nFinal generated report:")
    print(final_report)

    # Perform individual agent reflections
    print("\n\n\nIndividual Agent Reflections:")
    for agent in report_system.agents:
        agent.reflect()

    # Perform system-wide reflection
    print("\n\n\nSystem-wide Reflection:")
    report_system.system_reflect()
