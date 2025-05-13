def get_health_data():
    steps = input("Enter number of steps: ")
    calories = input("Enter number of calories consumed: ")
    sleep_hours = input("Enter hours of sleep: ")

    print("\nYou entered:")
    print(f"Steps: {steps}")
    print(f"Calories: {calories}")
    print(f"Sleep Hours: {sleep_hours}")
    return steps, calories, sleep_hours

get_health_data()
import csv
from datetime import date

def save_to_csv(steps, calories, sleep_hours, filename='health_data.csv'):
    today = date.today().isoformat()
    header = ['date', 'steps', 'calories', 'sleep_hours']
    data = [today, steps, calories, sleep_hours]

    try:
        # Fayl mavjud bo'lmasa, sarlavha bilan yoziladi
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            if f.tell() == 0:  # Fayl bo'sh bo'lsa
                writer.writerow(header)
            writer.writerow(data)
        print("Data saved to CSV successfully.")
    except Exception as e:
        print("Error saving to CSV:", e)

# Misol
save_to_csv(8000, 2100, 7.5)
import csv
from datetime import datetime, timedelta
from statistics import mean

def read_last_7_days(filename='health_data.csv'):
    data = []
    today = datetime.today().date()
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_date = datetime.strptime(row['date'], "%Y-%m-%d").date()
            if (today - row_date).days <= 6:  # including today
                data.append({
                    'steps': int(row['steps']),
                    'calories': int(row['calories']),
                    'sleep_hours': float(row['sleep_hours'])
                })
    return data

def calculate_stats(data, key):
    values = [item[key] for item in data]
    if not values:
        return "No data"
    return {
        'average': round(mean(values), 2),
        'max': max(values),
        'min': min(values)
    }

def show_weekly_stats():
    data = read_last_7_days()
    if not data:
        print("No data available for the last 7 days.")
        return
    print("📊 Weekly Health Statistics (Last 7 Days):\n")
def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("❌ Please enter an absolute number.")

def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("❌ Please enter an absolute number.")

def get_health_data():
    print("📝 Please enter your health info")

    def generate_summary_report():
        data = read_last_7_days()
        if not data:
            print("⚠️ There is no enough data(within 7 days).")
            return

        print("\n📋 Weekly Health Summary Report (Last 7 Days)\n")
        print("{:<12} {:<10} {:<10} {:<10}".format("Parameter", "Average", "Max", "Min"))
        print("-" * 45)

        for key in ['steps', 'calories', 'sleep_hours']:
            stats = calculate_stats(data, key)
            print("{:<12} {:<10} {:<10} {:<10}".format(
                key.capitalize(),
                stats['average'],
                stats['max'],
                stats['min']
            ))

    generate_summary_report()