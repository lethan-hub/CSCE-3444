import json
from datetime import datetime

WORKOUTS_FILE = 'workouts.json'

# Load existing workouts from file or initialize empty structure
def load_workouts():
    try:
        with open(WORKOUTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save workouts to file
def save_workouts(workouts):
    with open(WORKOUTS_FILE, "w") as file:
        json.dump(workouts, file, indent=4)


''' **Main workouts function**
    - Log cardio workouts (running, stairmaster, cycling)
    - View today's logged workouts
    - Future: Strength traiing implementation later on 
'''
def workouts(username):
    workouts_data = load_workouts()
    today = datetime.now().strftime("%Y-%m-%d")
    if username not in workouts_data:
        workouts_data[username] = {}
    if today not in workouts_data[username]:
        workouts_data[username][today] = []
    print("\n[Workouts]")

    while True:
        print("1. Log new workout")
        print("2. View today's workout")
        print("3. Return to main menu")
        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            print("\nWhat type of workout today?")
            print("1. Cardio") # only choice for now
            print("2. Strength Training") # coming later on 
            type_choice = input("Select workout type (1-2): ").strip()
            
            if type_choice == "1":
                print("\n[Select Cardio Workout]")
                print("1. Running")
                print("2. Stairmaster")
                print("3. Cycling")

                cardio_types = {
                    "1": "Running",
                    "2": "Stairmaster",
                    "3": "Cycling"
                }
                cardio_choice = input("Cardio type (1-3): ").strip()

                if cardio_choice not in cardio_types:
                    print("Invalid cardio type. Please try again.")
                    continue
                workout_type = cardio_types[cardio_choice]
                duration = input("Duration (minutes): ").strip()

                try: 
                    duration = int(duration)
                    if workout_type == "Running":
                        steps = duration * 160 # avg 160 steps/min
                    elif workout_type == "Stairmaster":
                        steps = duration * 130 # avg 130 steps/min
                    elif workout_type == "Cycling":
                        steps = 0 # cycling doesn't count steps

                except ValueError:
                        print("Invalid duration. Please enter a number.")
                        continue
                
                workout_entry = {
                    "category": "Cardio",
                    "type": workout_type,
                    "duration_minutes": duration,
                    "steps": steps
                }
                workouts_data[username][today].append(workout_entry)
                save_workouts(workouts_data)
                print(f"Logged {workout_type} workout! Steps estimated: {steps}\n")

            elif type_choice == "2":
                print("\nStrength Training coming soon!\n")
                continue

        elif choice == "2":
            todays_logs = workouts_data[username].get(today, [])
            if not todays_logs:
                print("No workouts logged today.\n")
            else:
                print(f"\n[Today's Workouts for {username} on {today}]")
                for i, workout in enumerate(todays_logs, 1):
                    print(f"{i}. {workout['category']} - {workout['type']}, Duration: {workout['duration_minutes']} mins, Steps: {workout['steps']}")
                print()

        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

                

