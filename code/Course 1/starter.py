import os
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI
import json
import re

# Load API key from .env file
load_dotenv("../.env")
client = OpenAI(base_url = "https://openai.vocareum.com/v1",
                api_key=os.getenv("OPENAI_API_KEY"))
response= None

class FitnessUser:
    """Represents a fitness app user."""
    def __init__(self, id: str, age: int, fitness_level: int, 
                 goals: List[str], preferences: List[str], 
                 limitations: List[str] = None):
        self.id = id
        self.age = age
        self.fitness_level = fitness_level
        self.goals = goals
        self.preferences = preferences
        self.limitations = limitations or []

    def __str__(self):
        return f"User {self.id}: Level {self.fitness_level}, Goals: {', '.join(self.goals)}"


# ======== TODO: AGENT 1 — Deterministic Planner ========
# Create a rule-based planner that adjusts:
# - number of workout days
# - intensity
# - workout types
# - session duration
# based on fitness level and goals

def deterministic_agent(user: FitnessUser) -> Dict:
    """Agent that creates a workout plan using deterministic rules."""
    plan = {
        "workout_days": 3,
        "session_duration": 30,
        "workout_types": [],
        "intensity": "moderate"
    }
    
    if user.fitness_level >= 4:
        plan["workout_days"] = 5
    elif user.fitness_level >= 2:
        plan["workout_days"] = 4
    
    if user.fitness_level >= 3:
        plan["session_duration"] = 45
    
    if user.fitness_level <= 2:
        plan["intensity"] = "low"
    elif user.fitness_level >= 4:
        plan["intensity"] = "high"
    
    if "weight management" in user.goals:
        plan["workout_types"].append("cardio")
    if "strength building" in user.goals:
        plan["workout_types"].append("strength training")
    if "flexibility" in user.goals:
        plan["workout_types"].append("stretching")
    if "endurance" in user.goals:
        plan["workout_types"].append("interval training")
    
    if not plan["workout_types"]:
        plan["workout_types"] = ["general fitness", "light cardio"]
    
    plan["weekly_schedule"] = {}
    days = ["Monday", "Wednesday", "Friday", "Tuesday", "Thursday", "Saturday"]
    
    for i in range(plan["workout_days"]):
        workout_type = plan["workout_types"][i % len(plan["workout_types"])]
        plan["weekly_schedule"][days[i]] = {
            "type": workout_type,
            "duration": plan["session_duration"],
            "intensity": plan["intensity"],
            "description": f"{plan['intensity'].capitalize()} {workout_type} session"
        }
    
    return plan


# ======== AGENT 2 — LLM-Based Planner ========
# We've handled the API part. Your task is to COMPLETE THE PROMPT below
# that will instruct the LLM how to generate the plan.

def llm_agent(user: FitnessUser) -> Dict:
    global response
    goals_text = ", ".join(user.goals)
    preferences_text = ", ".join(user.preferences)
    limitations_text = ", ".join(user.limitations) if user.limitations else "None"

    prompt = f"""
    As a certified fitness trainer, create a personalized weekly workout plan for this client.

    Client Information:
    - Age: {user.age} years
    - Fitness Level: {user.fitness_level}/5 (1=beginner, 5=advanced)
    - Fitness Goals: {goals_text}
    - Activity Preferences: {preferences_text}
    - Limitations or Constraints: {limitations_text}
    
    Create a balanced, realistic workout plan that respects the user's current fitness level and addresses their specific goals while keeping in mind their preferences and limitations.

    IMPORTANT GUIDELINES:
    1. Do NOT provide any medical advice or try to address medical conditions
    2. Focus on general fitness and wellbeing, not extreme transformations
    3. Include appropriate rest days
    4. Recommend proper warm-up and cool-down periods
    5. Specify at what intensity the exercises should be performed

    Your response must be in JSON format with these fields:
    {{
        "reasoning": "Brief explanation of your workout design decisions",
        "weekly_schedule": {{
            "day": {{
                "type": "workout type/category",
                "duration": duration in minutes,
                "intensity": "low/moderate/high",
                "description": "brief description of the workout"
            }},
            ... (for each day of the week, including rest days)
        }},
        "considerations": "Any specific considerations for this user"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a certified fitness trainer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )
        result_text = response.choices[0].message.content
        clean_json = re.sub(r"^```json|```$", "", result_text.strip(), flags=re.MULTILINE) 
        print("LLM Response:", result_text)  # For debugging purposes
        return json.loads(clean_json)

    except Exception as e:
        fallback = deterministic_agent(user)
        return {
            "reasoning": f"LLM planning failed: {str(e)}",
            "weekly_schedule": fallback["weekly_schedule"],
            "considerations": "Fallback to rule-based plan."
        }


# ======== COMPARISON LOGIC (DO NOT EDIT) ========

def compare_workout_planning(users: List[FitnessUser]):
    print("\n===== WORKOUT PLAN COMPARISON =====")
    for i, user in enumerate(users, 1):
        print(f"\n--- User {i}: {user.id} ---")
        print(f"Age: {user.age} | Fitness Level: {user.fitness_level}/5")
        print(f"Goals: {', '.join(user.goals)}")
        print(f"Preferences: {', '.join(user.preferences)}")
        print(f"Limitations: {', '.join(user.limitations)}")

        det_plan = deterministic_agent(user)
        print("\n[Deterministic Agent]")
        for day, workout in det_plan["weekly_schedule"].items():
            print(f"- {day}: {workout['type']} ({workout['intensity']}, {workout['duration']} min)")

        llm_plan = llm_agent(user)
        print("\n[LLM Agent]")
        print(f"Reasoning: {llm_plan.get('reasoning', 'No reasoning provided')}")
        for day, workout in llm_plan["weekly_schedule"].items():
            print(f"- {day}: {workout['type']} ({workout['intensity']}, {workout['duration']} min)")
            print(f"  {workout['description']}")
        print(f"Considerations: {llm_plan.get('considerations', 'None')}")


# ======== SAMPLE USERS ========

def main():
    users = [
        FitnessUser(
            id="U001",
            age=35,
            fitness_level=2,
            goals=["weight management", "stress reduction"],
            preferences=["home workouts", "morning routines"],
            limitations=["limited equipment", "time constraints (max 30 min/day)"]
        ),
        FitnessUser(
            id="U002",
            age=55,
            fitness_level=3,
            goals=["joint mobility", "strength building"],
            preferences=["outdoor activities", "swimming"],
            limitations=["mild joint stiffness"]
        )
    ]

    compare_workout_planning(users)

if __name__ == "__main__":
    main()
