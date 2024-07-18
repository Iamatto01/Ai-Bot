# AI_Agent.py
import datetime
import requests
import json

class AI_Agent:
    def __init__(self, oracle_client, gemini_api_key):
        self.memory = []
        self.emotion = "neutral"  # Default emotional state
        self.emotion_history = []  # List to store past emotions and timestamps
        self.personality_traits = ["friendly"]  # Example traits
        self.oracle_client = oracle_client  # OracleDB client for state management
        self.description = "Handles input processing, emotion management, and memory storage for the AI agent."
        self.gemini_api_key = gemini_api_key  # Your Gemini API key

    def analyze_intent(self, input_text):
        if "joke" in input_text.lower():
            return "request_joke"
        elif "steam sale" in input_text.lower():
            return "steam_sale"
        elif "fifa game" in input_text.lower():
            return "fifa_game"
        elif "cryptocurrency" in input_text.lower():
            return "cryptocurrency"
        elif any(word in input_text.lower() for word in ["date", "today", "day", "time"]):
            return "current_date_time"
        else:
            return "unknown"

    def process_input(self, input_text):
        intent = self.analyze_intent(input_text)
        return intent

    def generate_response(self, input_text):
        response = f"I'm feeling {self.emotion}."
        intent = self.analyze_intent(input_text)
        
        if intent == "request_joke":
            response += " Here's a joke: Why don't scientists trust atoms? Because they make up everything!"
        elif intent == "steam_sale":
            response += " Let me check for you..."
            response += self.check_steam_sales()
        elif intent == "fifa_game":
            response += " Let me check for you..."
            response += self.check_fifa_games()
        elif intent == "cryptocurrency":
            response += " Let me check Gemini for you..."
            response += self.check_gemini_data()
        elif intent == "current_date_time":
            response += f" The current date and time is {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
        else:
            response += " I'm not sure how to respond to that yet. Let me learn from this."
            response += self.generate_with_gemini(input_text)
            
        return response

    def generate_with_gemini(self, input_text):
        url = "https://api.gemini.com/v1/pubticker/btcusd"  # Adjust the URL to fit the purpose
        headers = {"Authorization": f"Bearer {self.gemini_api_key}"}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                generated_response = f"\nGemini data: {data}"
                self.save_generated_response(input_text, generated_response)
                return generated_response
            else:
                return "\nFailed to fetch Gemini data. Please try again later."
        except Exception as e:
            return f"\nError fetching Gemini data: {str(e)}"

    def save_generated_response(self, input_text, generated_response):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = {
            "timestamp": timestamp,
            "input_text": input_text,
            "generated_response": generated_response,
            "emotion": self.emotion
        }
        self.oracle_client.insert_generated_response(data)

    def save_state(self):
        data = {
            "agent_id": "AI_Agent_001",  # Example agent ID
            "emotion": self.emotion,
            "memory": self.memory,
            "emotion_history": self.emotion_history,
        }
        
        # Convert datetime objects to ISO format strings
        data["emotion_history"] = [{"emotion": entry["emotion"], "timestamp": entry["timestamp"].isoformat()} for entry in self.emotion_history]

        self.oracle_client.insert_document(data)

    def load_state(self):
        state = self.oracle_client.fetch_document({"agent_id": "AI_Agent_001"})
        if state:
            self.memory = state.get("memory", [])
            self.emotion = state.get("emotion", "neutral")
            self.emotion_history = state.get("emotion_history", [])

    def update_emotion(self, new_emotion):
        self.emotion = new_emotion
        self.emotion_history.append({"emotion": new_emotion, "timestamp": datetime.datetime.now()})

    def check_steam_sales(self):
        # Example function to check Steam sales (using mock data)
        # Replace with actual Steam API integration
        return "\nSteam Sales: Half-Life 3 - 50% off until tomorrow!"

    def check_fifa_games(self):
        # Example function to check FIFA game announcements (using mock data)
        # Replace with actual FIFA game data integration
        return "\nUpcoming FIFA Game: FIFA 25 announced for release next month!"

    def check_gemini_data(self):
        # Example function to fetch cryptocurrency data from Gemini API
        url = "https://api.gemini.com/v1/pubticker/btcusd"
        headers = {"Authorization": f"Bearer {self.gemini_api_key}"}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                price = data.get("last", "N/A")
                return f"\nCurrent Bitcoin (BTC) price: ${price}"
            else:
                return "\nFailed to fetch Gemini data. Please try again later."
        except Exception as e:
            return f"\nError fetching Gemini data: {str(e)}"

    # Placeholder for other API integration functions
    # Add functions to interact with other APIs as needed
