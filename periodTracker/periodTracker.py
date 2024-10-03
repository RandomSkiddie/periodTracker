import datetime
import os

class PeriodTracker:
    def __init__(self, file_name="periods.txt"):
        self.file_name = file_name
        self.periods = self.load_periods()

    def load_periods(self):
        periods = []
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                for line in file:
                    start, end = line.strip().split(',')
                    periods.append((datetime.datetime.strptime(start, '%Y-%m-%d'),
                                    datetime.datetime.strptime(end, '%Y-%m-%d')))
        return periods

    def save_periods(self):
        with open(self.file_name, 'w') as file:
            for start, end in self.periods:
                file.write(f"{start.strftime('%Y-%m-%d')},{end.strftime('%Y-%m-%d')}\n")

    def add_period(self, start_date, end_date):
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        self.periods.append((start, end))
        self.save_periods()

    def edit_period(self, index, start_date, end_date):
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        self.periods[index] = (start, end)
        self.save_periods()

    def average_cycle_length(self):
        if len(self.periods) < 2:
            return None
        cycle_lengths = [(self.periods[i][0] - self.periods[i-1][0]).days for i in range(1, len(self.periods))]
        return sum(cycle_lengths) / len(cycle_lengths)

    def predict_next_period(self):
        if len(self.periods) < 2:
            return None
        last_period_start = self.periods[-1][0]
        avg_cycle = self.average_cycle_length()
        if avg_cycle:
            next_period_start = last_period_start + datetime.timedelta(days=avg_cycle)
            return next_period_start
        return None

    def display_periods(self):
        for i, (start, end) in enumerate(self.periods, 1):
            print(f"{i}. Start: {start.strftime('%Y-%m-%d')}, End: {end.strftime('%Y-%m-%d')}")

def clear_screen():
    # This will clear the screen for Windows, macOS, and Linux
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_input():
    tracker = PeriodTracker()

    while True:
        clear_screen()  # Clear screen before displaying the menu
        print("Welcome to period tracker by Skid. Type a number and press Enter.")
        print("1. Add new period")
        print("2. View previous periods")
        print("3. Edit a period")
        print("4. View average cycle length")
        print("5. Predict next period")
        print("6. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            while True:
                start_date = input("Enter the start date (YYYY-MM-DD) or type 'q' to return to the menu: ")
                if start_date.lower() == 'q':
                    break
                end_date = input("Enter the end date (YYYY-MM-DD) or type 'q' to return to the menu: ")
                if end_date.lower() == 'q':
                    break
                tracker.add_period(start_date, end_date)
                print("Period added successfully!")
                input("Press Enter to return to the menu.")
                break

        elif choice == '2':
            clear_screen()
            if tracker.periods:
                print("Previous periods:")
                tracker.display_periods()
            else:
                print("No periods recorded yet.")
            input("Press Enter to return to the menu.")

        elif choice == '3':
            clear_screen()
            if tracker.periods:
                tracker.display_periods()
                index = input("Select the number of the period you want to edit (or type 'q' to return to the menu): ")
                if index.lower() == 'q':
                    continue
                try:
                    index = int(index) - 1
                    if 0 <= index < len(tracker.periods):
                        start_date = input("Enter the new start date (YYYY-MM-DD) or type 'q' to return to the menu: ")
                        if start_date.lower() == 'q':
                            continue
                        end_date = input("Enter the new end date (YYYY-MM-DD) or type 'q' to return to the menu: ")
                        if end_date.lower() == 'q':
                            continue
                        tracker.edit_period(index, start_date, end_date)
                        print("Period updated successfully!")
                    else:
                        print("Invalid selection.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            else:
                print("No periods recorded yet.")
            input("Press Enter to return to the menu.")

        elif choice == '4':
            clear_screen()
            avg_cycle = tracker.average_cycle_length()
            if avg_cycle:
                print(f"Average cycle length: {avg_cycle:.2f} days")
            else:
                print("Not enough data to calculate average cycle length.")
            input("Press Enter to return to the menu.")

        elif choice == '5':
            clear_screen()
            next_period = tracker.predict_next_period()
            if next_period:
                print(f"Next period is predicted to start on: {next_period.strftime('%Y-%m-%d')}")
            else:
                print("Not enough data to predict the next period.")
            input("Press Enter to return to the menu.")

        elif choice == '6':
            clear_screen()
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

# Run the CLI
get_user_input()
