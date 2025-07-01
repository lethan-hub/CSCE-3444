import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEALS_FILE = os.path.join(BASE_DIR, 'data', 'meals.json')

def load_meal_data():
    try:
        with open(MEALS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_meal_data(data):
    os.makedirs(os.path.dirname(MEALS_FILE), exist_ok=True)
    with open(MEALS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def prompt_date(prompt_text="Enter date (YYYY-MM-DD) or leave blank for today: "):
    date_str = input(prompt_text).strip()
    if not date_str:
        return datetime.now().strftime('%Y-%m-%d')
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return prompt_date(prompt_text)

def meals(username):
    data = load_meal_data()
    if username not in data:
        data[username] = {}
    print("Nutrition Tracker")
    while True:
        print("\nOptions:")
        print("1. Add a meal entry")
        print("2. Browse meals by date")
        print("3. Exit to main menu")
        action = input("Choose an option: ").strip().upper()
        if action == "1":
            while True:
                date = prompt_date("Date for this meal (YYYY-MM-DD, blank for today): ")
                today_str = datetime.now().strftime('%Y-%m-%d')
                if date > today_str:
                    print("You cannot add meals for future dates. Please enter today or a past date.")
                else:
                    break
            if date not in data[username]:
                data[username][date] = []
            print(f"\nLogging meal for {date}.")
            meal = {}
            # Require AM/PM in time
            while True:
                meal_time = input("Time of meal (e.g., 07:30 AM): ").strip()
                if meal_time.lower().endswith('am') or meal_time.lower().endswith('pm'):
                    break
                print("Please include AM or PM in the time (e.g., 07:30 AM or 12:15 pm). Try again.")
            meal['time'] = meal_time
            meal['food'] = input("What did you eat?: ").strip()
            try:
                meal['calories'] = float(input("Calories: ").strip())
                meal['protein_g'] = float(input("Protein (g): ").strip())
                meal['carbs_g'] = float(input("Carbs (g): ").strip())
                meal['fats_g'] = float(input("Fats (g): ").strip())
            except ValueError:
                print("Please enter valid numbers for calories and macros.")
                continue
            data[username][date].append(meal)
            save_meal_data(data)
            print(f"Meal added for {date}!")
        elif action == "2":
            date = prompt_date("Which date do you want to view? (YYYY-MM-DD, blank for today): ")
            meals_on_date = data[username].get(date, [])
            if not meals_on_date:
                print(f"No meals found for {date}.")
            else:
                print(f"\nMeals for {username} on {date}:")
                for idx, meal in enumerate(meals_on_date, 1):
                    print(f"{idx}. {meal['time']} | {meal['food']} | {meal['calories']} kcal | Protein: {meal['protein_g']}g | Carbs: {meal['carbs_g']}g | Fats: {meal['fats_g']}g")
        elif action == "3":
            print("Returning to the main menu.")
            break
        else:
            print("Invalid option. Please select an option.") 