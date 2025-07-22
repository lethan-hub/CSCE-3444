import json
import os
from datetime import datetime, timedelta

def load_meal_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MEALS_FILE = os.path.join(BASE_DIR, '../data/meals.json')
    try:
        with open(MEALS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_meal_data(data):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MEALS_FILE = os.path.join(BASE_DIR, '../data/meals.json')
    os.makedirs(os.path.dirname(MEALS_FILE), exist_ok=True)
    with open(MEALS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def parse_date_shortcut(date_str, default=None):
    date_str = date_str.strip().lower()
    today = datetime.now()
    if not date_str and default:
        return default
    if date_str.lower() in ('today', ''):
        return today.strftime('%Y-%m-%d')
    if date_str.lower() == 'yesterday':
        return (today - timedelta(days=1)).strftime('%Y-%m-%d')
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD, 'today', or 'yesterday'.")
        return None

def prompt_date(prompt_text, default=None):
    while True:
        date_str = input(prompt_text).strip()
        parsed = parse_date_shortcut(date_str, default)
        if parsed:
            return parsed

def print_meals(meals_on_date):
    for idx, meal in enumerate(meals_on_date, 1):
        print(f"{idx}. {meal['time']} | {meal['food']} | {meal['calories']} kcal | Protein: {meal['protein_g']}g | Carbs: {meal['carbs_g']}g | Fats: {meal['fats_g']}g")

def daily_totals(meals_on_date):
    total_cal = sum(m['calories'] for m in meals_on_date)
    total_pro = sum(m['protein_g'] for m in meals_on_date)
    total_carb = sum(m['carbs_g'] for m in meals_on_date)
    total_fat = sum(m['fats_g'] for m in meals_on_date)
    print(f"Total: {total_cal} kcal | Protein: {total_pro}g | Carbs: {total_carb}g | Fats: {total_fat}g")
    return total_cal, total_pro, total_carb, total_fat

def get_float_input(prompt):
    while True:
        val = input(prompt).strip()
        try:
            return float(val)
        except ValueError:
            print("Please enter a valid number.")

def get_time_input(prompt):
    while True:
        meal_time = input(prompt).strip()
        time_parts = meal_time.split()
        if len(time_parts) == 2 and (time_parts[1].lower() in ['am', 'pm']) and any(c.isdigit() for c in time_parts[0]):
            if time_parts[1].lower() == 'am':
                return time_parts[0] + ' AM'
            else:
                return time_parts[0] + ' PM'
        print("Please enter a valid time with AM or PM (e.g., 07:30 AM or 12:15 pm). Try again.")

def get_confirmation(prompt):
    while True:
        confirm = input(prompt).strip().lower()
        if confirm in ('y', 'n'):
            return confirm == 'y'
        print("Please enter 'y' or 'n'.")

def print_meals_and_totals(meals_on_date):
    print_meals(meals_on_date)
    daily_totals(meals_on_date)

def add_meal(data, username, date):
    if date not in data[username]:
        data[username][date] = []
    meal = {}
    meal['time'] = get_time_input("Time of meal (e.g., 07:30 AM): ")
    meal['food'] = input("What did you eat?: ").strip()
    meal['calories'] = get_float_input("Calories: ")
    meal['protein_g'] = get_float_input("Protein (g): ")
    meal['carbs_g'] = get_float_input("Carbs (g): ")
    meal['fats_g'] = get_float_input("Fats (g): ")
    temp_meals = data[username][date] + [meal]
    print("Preview of today's meals including this entry:")
    print_meals_and_totals(temp_meals)
    if get_confirmation("Add this meal? (y/n): "):
        data[username][date].append(meal)
        save_meal_data(data)
        print(f"Meal added for {date}!")
    else:
        print("Meal not added.")

def edit_meal(data, username, date):
    meals_on_date = data[username].get(date, [])
    if not meals_on_date:
        print(f"No meals found for {date}.")
        return
    print_meals(meals_on_date)
    entry = input("Enter the number of the meal to edit (or 0 to cancel): ").strip()
    if entry == "0" or entry == "":
        return
    try:
        entry_num = int(entry)
        if 1 <= entry_num <= len(meals_on_date):
            meal = meals_on_date[entry_num-1]
            print("Leave blank to keep current value.")
            new_time = input(f"Time ({meal['time']}): ").strip()
            if new_time:
                meal['time'] = get_time_input("Time (e.g., 07:30 AM): ") if new_time else meal['time']
            new_food = input(f"Food ({meal['food']}): ").strip()
            if new_food:
                meal['food'] = new_food
            for macro in ['calories', 'protein_g', 'carbs_g', 'fats_g']:
                new_val = input(f"{macro.replace('_g','').capitalize()} ({meal[macro]}): ").strip()
                if new_val:
                    try:
                        meal[macro] = float(new_val)
                    except ValueError:
                        print(f"Invalid input for {macro}. Keeping previous value.")
            if get_confirmation("Save changes to this meal? (y/n): "):
                save_meal_data(data)
                print("Meal updated.")
                print_meals_and_totals(meals_on_date)
            else:
                print("Edit cancelled.")
        else:
            print("Invalid entry number.")
    except ValueError:
        print("Invalid input.")

def delete_meal(data, username, date):
    meals_on_date = data[username].get(date, [])
    if not meals_on_date:
        print(f"No meals found for {date}.")
        return
    print_meals(meals_on_date)
    entry = input("Enter the number of the meal to delete (or 0 to cancel): ").strip()
    if entry == "0" or entry == "":
        return
    try:
        entry_num = int(entry)
        if 1 <= entry_num <= len(meals_on_date):
            if get_confirmation("Are you sure you want to delete this meal? (y/n): "):
                del meals_on_date[entry_num-1]
                save_meal_data(data)
                print("Meal deleted.")
                print_meals_and_totals(meals_on_date)
            else:
                print("Delete cancelled.")
        else:
            print("Invalid entry number.")
    except ValueError:
        print("Invalid input.")

def view_weekly_average(data, username, today_str):
    today = datetime.strptime(today_str, '%Y-%m-%d')
    totals = {'calories': 0, 'protein_g': 0, 'carbs_g': 0, 'fats_g': 0}
    days_counted = 0
    for i in range(7):
        day = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        meals = data[username].get(day, [])
        if meals:
            days_counted += 1
            for meal in meals:
                totals['calories'] += meal['calories']
                totals['protein_g'] += meal['protein_g']
                totals['carbs_g'] += meal['carbs_g']
                totals['fats_g'] += meal['fats_g']
    if days_counted == 0:
        print("No meals found in the past week.")
        return
    print(f"Weekly Average (last {days_counted} days):")
    print(f"Calories: {totals['calories']//days_counted} kcal | Protein: {totals['protein_g']//days_counted}g | Carbs: {totals['carbs_g']//days_counted}g | Fats: {totals['fats_g']//days_counted}g")

def print_main_menu():
    print("\nNUTRITION TRACKER MAIN MENU")
    print("1. Daily Meals")
    print("2. Nutrition Summary")
    print("3. Exit")

def print_daily_menu():
    print("\nDAILY MEALS MENU")
    print("1. View all meals today")
    print("2. Add new meal")
    print("3. Edit existing meal")
    print("4. Delete a meal")
    print("5. Back to main menu")

def print_summary_menu():
    print("\nNUTRITION SUMMARY MENU")
    print("1. View today's summary")
    print("2. View past days")
    print("3. View weekly average")
    print("4. Back to main menu")

def meals(username):
    data = load_meal_data()
    if username not in data:
        data[username] = {}
    while True:
        print_main_menu()
        main_choice = input("Select an option (1-3): ").strip()
        today_str = datetime.now().strftime('%Y-%m-%d')
        if main_choice == "1":
            while True:
                print_daily_menu()
                daily_choice = input("Select an option (1-5): ").strip()
                if daily_choice == "1":
                    meals_on_date = data[username].get(today_str, [])
                    if not meals_on_date:
                        print("No meals logged for today.")
                    else:
                        print_meals(meals_on_date)
                        daily_totals(meals_on_date)
                    input("Press Enter to continue")
                elif daily_choice == "2":
                    add_meal(data, username, today_str)
                    input("Press Enter to continue")
                elif daily_choice == "3":
                    edit_meal(data, username, today_str)
                    input("Press Enter to continue")
                elif daily_choice == "4":
                    delete_meal(data, username, today_str)
                    input("Press Enter to continue")
                elif daily_choice == "5":
                    break
                else:
                    print("Invalid option. Please select a number from 1 to 5.")
        elif main_choice == "2":
            while True:
                print_summary_menu()
                summary_choice = input("Select an option (1-4): ").strip()
                if summary_choice == "1":
                    meals_on_date = data[username].get(today_str, [])
                    if not meals_on_date:
                        print("No meals logged for today.")
                    else:
                        print_meals(meals_on_date)
                        daily_totals(meals_on_date)
                    input("Press Enter to continue")
                elif summary_choice == "2":
                    date = prompt_date("Which date do you want to view? (YYYY-MM-DD): ", default=today_str)
                    meals_on_date = data[username].get(date, [])
                    if not meals_on_date:
                        print(f"No meals found for {date}.")
                    else:
                        print_meals(meals_on_date)
                        daily_totals(meals_on_date)
                    input("Press Enter to continue")
                elif summary_choice == "3":
                    view_weekly_average(data, username, today_str)
                    input("Press Enter to continue")
                elif summary_choice == "4":
                    break
                else:
                    print("Invalid option. Please select a number from 1 to 4.")
        elif main_choice == "3":
            print("Returning to the main menu.")
            break
        else:
            print("Invalid option. Please select a number from 1 to 3.") 