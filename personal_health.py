import os
import json
from datetime import datetime

Health_file = "personal_health_info.json"

# Loads existing profiles or empty structures
def load_personalhealth_info():
  try:
    with open(Health_file, "r") as file:
      return json.load(file)
  except FileNotFoundError:
    return{}

# Updates profiles and saves it to the .json file
def save_profile(data):
  with open(Health_file, "w") as f:
      json.dump(data,f,indent = 4)
# Class for the Personal Health
class PersonalHealth:
    def __init__(self, name, age, gender, height_cm, weight_kg, username):
        self.name = name
        self.age = age
        self.gender = gender
        self.height_cm = height_cm
        self.weight_kg = weight_kg
        self.username = username
        self.bmi = round(weight_kg / ((height_cm / 100) ** 2), 2) # Calculates BMI
        self.status = self.get_health_status() # Gives BMI based on user input
        self.recorded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Gives date and time

    def get_health_status(self):
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def save(self):
      try:
        print(f"Saving profile for user {self.username}...")
        data = load_personalhealth_info()
        entry = {
            "Name": self.name,
            "Age": self.age,
            "Gender": self.gender,
            "Height (cm)": self.height_cm,
            "Weight (kg)": self.weight_kg,
            "BMI": self.bmi,
            "Health Status": self.status,
            "Date": self.recorded_at
        }
        data.setdefault(self.username, []).append(entry)
        save_profile(data)
        print("Profile saved.")
      except Exception as e:
        print(f"Error while saving profile: {e}")
# Saves health profile
    def profile(self):
        return {
            "Name": self.name,
            "Age": self.age,
            "Gender": self.gender,
            "Height (cm)": self.height_cm,
            "Weight (kg)": self.weight_kg,
            "BMI": self.bmi,
            "Health Status": self.status,
            "Date": self.recorded_at
        }
