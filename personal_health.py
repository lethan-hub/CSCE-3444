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

# Previous profiles are shown
def old_profile(username):
  return load_personalhealth_info().get(username,[])

# Adds new health info for profile
def add_health(username,name,age,gender,height_cm,weight_kg):
# Calculates the BMI
    height_m = height_cm / 100
    bmi =  round(weight_kg / (height_m ** 2), 2)
# Health Status based on BMI
    if bmi < 18.5:
      status =  "Underweight"
    elif 18.5 <= bmi < 24.9:
      status =  "Normal weight"
    elif 25<= bmi < 29.9:
      status = "Overweight"
    else:
      status = "Obese"

# Shows current time
  date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

 entry = {
        "Name" : name,
        "Age" : age,
        "Gender" : .gender,
        "Height (cm)" : height_cm,
        "Weight (kg)" : weight_kg,
        "BMI" : bmi,
        "Health Status" : status,
        "Date" : date_time
      }
# Loads, saves, and updates data
data = load_personalhealth_info()
data.setdefault(username,[]).append(entry)
save_profile(data)
