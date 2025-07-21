import json
from datetime import datetime

WORKOUTS_FILE = 'workouts.json'

# Load existing workouts from file or initialize empty structure
def load_workouts():
    try:
        with open(WORKOUTS_FILE, "r") as file:
            data = json.load(file)

            if not isinstance(data, dict):
                print("Invalid data format in workouts file. Initializing empty workouts.")
                return {}
            return data
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON from workouts file. Initializing empty workouts.")
        return {}

# Save workouts to file
def save_workouts(workouts):
    with open(WORKOUTS_FILE, "w") as file:
        json.dump(workouts, file, indent=4)

def log_cardio_workout(workouts_data, username, today):
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
        return
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
            return
                
    workout_entry = {
        "category": "Cardio",
        "type": workout_type,
        "duration_minutes": duration,
        "steps": steps
        }
    workouts_data[username][today].append(workout_entry)
    save_workouts(workouts_data)
    print(f"Logged {workout_type} workout! Steps estimated: {steps}\n")


''' Log strength training workouts
    - Allows user to log strength training workouts
    - Saves the workout data to a JSON file
    - Calculates total volume lifted based on sets, reps, and weight
'''    
def log_strength_workout(workouts_data, username, today):
    print(f"\n[Strength Training Logger]")
     
    if username not in workouts_data:
        workouts_data[username] = {}    
    if today not in workouts_data[username]:
        workouts_data[username][today] = []

    while True:
        exercise = input("Enter the exercise name (or 'done' to finish): ").strip()
        if exercise.lower() == 'done':
            break

        try:
            sets = int(input("Enter the number of sets: ").strip())
            reps = int(input("Enter the number of reps per set: ").strip())
            weight = float(input("Enter the weight used (in lbs): ").strip())
        except ValueError:
            print("Invalid input. Please enter numeric values for sets, reps, and weight.")
            continue

        volume = sets * reps * weight

        workout_entry = {
            "category": "Strength",
            "type": exercise,
            "sets": sets,
            "reps_per_set": reps,
            "weight": weight,
            "volume": volume     # Calculate total volume lifted         
        }
    
        workouts_data[username][today].append(workout_entry)
        save_workouts(workouts_data)

       
        print(f"Logged Strength: {sets}x{reps} @ {weight} lbs - Total Volume: {volume:.1f}\n")

        more = input("Log another exercise? (yes/no): ").strip().lower()
        if more == 'yes':
            break
        elif more == 'no':
            return
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


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
        print("1. Log cardio workout")
        print("2. Log strength workout")
        print("3. View today's workout")
        print("4. Return to main menu")
        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            log_cardio_workout(workouts_data, username, today)
        elif choice == "2":
            log_strength_workout(workouts_data, username, today)
        elif choice == "3":
            todays_logs = workouts_data[username].get(today, [])
            if not todays_logs:
                print("No workouts logged today.\n")
            else:
                print(f"\n[Today's Workouts for {username} on {today}]")
                for i, workout in enumerate(todays_logs, 1):
                    if workout['category'] == "Cardio":
                        print(f"{i}. {workout['type']} - Duration: {workout['duration_minutes']} mins, Steps: {workout['steps']}")
                    elif workout['category'] == "Strength":
                        print(f"{i}. {workout['type']} - Sets: {workout['sets']} x Reps: {workout['reps_per_set']} @ {workout['weight']} lbs, Volume: {workout['volume']}")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

