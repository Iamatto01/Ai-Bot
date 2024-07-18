# Simulation.py

class Simulation:
    def __init__(self, ai_agent, telegram_groups, mongo_client):
        self.ai_agent = ai_agent
        self.telegram_groups = telegram_groups
        self.mongo_client = mongo_client

    def start(self):
        print("Simulation started")
        self.ai_agent.load_state()
        print(f"AI Agent loaded with emotion: {self.ai_agent.emotion} and memory: {self.ai_agent.memory}")

    def run(self):
        print("Simulation running")
        while True:
            input_text = input("Enter input for AI Agent (or 'exit' to stop): ")
            if input_text.lower() == 'exit':
                break

            intent = self.ai_agent.process_input(input_text)
            response = self.ai_agent.generate_response(input_text)
            print(f"Input: {input_text} | Intent: {intent} | Response: {response}")

            new_emotion = input("Enter new emotion for AI Agent (or press enter to skip): ")
            if new_emotion:
                self.ai_agent.update_emotion(new_emotion)
                print(f"Updated AI Agent emotion to: {self.ai_agent.emotion}")

            self.ai_agent.save_state()
            print("AI Agent state saved to database.")

