import os

# Placeholder for OpenAI integration
# In a real scenario, use:
# import openai
# openai.api_key = os.getenv("OPENAI_API_KEY")

class AIEngine:
    @staticmethod
    def parse_task_input(user_input: str):
        """
        Mock AI parsing logic.
        Future: Call OpenAI API to extracting structured data.
        """
        print(f"[AI Engine] Parsing: {user_input}")
        
        # Simple heuristic for demo purposes
        priority = "Medium"
        if "urgent" in user_input.lower() or "important" in user_input.lower():
            priority = "High"
        
        date = "Today"
        if "tomorrow" in user_input.lower():
            date = "Tomorrow"
            
        return {
            "title": user_input,
            "date": date,
            "time": "Flexible", # Default
            "priority": priority,
            "mood": "Neutral" # Default
        }

    @staticmethod
    def get_motivation_message(mood: str):
        """
        Returns a motivational message based on mood.
        """
        messages = {
            "Tired": "It's okay to rest. Small steps count.",
            "Focused": "You're in the zone! Crush it.",
            "Stressed": "Take a deep breath. One thing at a time.",
            "Motivated": "Let's use this energy! What's next?"
        }
        return messages.get(mood, "Keep moving forward.")
