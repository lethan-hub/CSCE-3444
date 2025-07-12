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

# Updates profiles
def save_profile(data):
  with open(Health_file, "w) as f:
            json.dump(data,f,indent = 4)

# Previous profiles
def old_profile(username):
  return load_personalhealth_info().get(username,[])

# Adds new health info for profile
def add_health(username,age,gender,height_cm,weight_kg):
# Calculates the BMI
    height_m = self.height_cm / 100
    return round(self.weight_kg / (height_m ** 2), 2)
# Health Status based on BMI
    if bmi < 18.5:
      return "Underweight"
    elif 18.5 <= bmi < 24.9:
      return "Normal weight"
    elif 25<= bmi < 29.9:
      return "Overweight"
    else:
      return "Obese"

 entry = {
        "Name" : self.name,
        "Age" : self.age,
        "Gender" : self.gender,
        "Height (cm)" : self.height_cm,
        "Weight (kg)" : self.weight_kg,
        "BMI" : self.bmi,
        "Health Status" : self.status
        "Date" : self.date_time
      }

data = load_data()
data.setdefault(username,[]).append(entry)
save_data(data)
