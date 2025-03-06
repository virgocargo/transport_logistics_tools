import tkinter as tk
from tkinter import ttk, messagebox

# Cost calculations
FUEL_COST_PER_MILE = 0.6  # Fuel cost per mile ($)
DISPATCHER_FEE_RATE = 0.1  # Dispatcher fee as % of load pay
MAINTENANCE_COST_PER_MILE = 0.1  # Maintenance cost per mile ($)
DEFAULT_TOLL_COST = 50  # Default toll cost ($)

class LoadCalculatorApp:
    """
    Tkinter-based GUI application for trucking load evaluation.
    Calculates net profit, rate per mile, and expenses based on input data.
    """

    def __init__(self, root):
        """Initialize main application window."""
        self.root = root
        self.root.title("Load Calculator")

        # Store load data
        self.booked_loads = []
        self.considered_loads = []

        # Store distances between known locations
        self.distance_dict = {
            ("Atlanta, GA", "Macon, GA"): 84,
            ("Atlanta, GA", "Savannah, GA"): 248,
            ("Macon, GA", "Savannah, GA"): 165,
        }

        # Create main UI elements
        self.create_main_ui()

    def create_main_ui(self):
        """Creates main interface with buttons and summary labels."""
        # Load Entry Button
        self.add_load_button = ttk.Button(self.root, text="Add New Load", command=self.open_load_entry_form)
        self.add_load_button.grid(row=0, column=0, padx=10, pady=10)

        # View Considered Loads Button
        self.view_considered_button = ttk.Button(self.root, text="View Loads Under Consideration", command=self.view_considered_loads)
        self.view_considered_button.grid(row=0, column=1, padx=10, pady=10)

        # View Booked Loads Button
        self.view_booked_button = ttk.Button(self.root, text="View Booked Loads", command=self.view_booked_loads)
        self.view_booked_button.grid(row=0, column=2, padx=10, pady=10)

        # Summary Labels
        self.profit_label = ttk.Label(self.root, text="Total Profit: $0.00")
        self.profit_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.expenses_label = ttk.Label(self.root, text="Total Expenses: $0.00")
        self.expenses_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def open_load_entry_form(self):
        """Opens a new window for entering load details."""
        self.entry_window = tk.Toplevel(self.root)
        self.entry_window.title("Enter Load Details")

        # Form Fields
        ttk.Label(self.entry_window, text="Origin:").grid(row=0, column=0, padx=5, pady=5)
        self.origin_entry = ttk.Entry(self.entry_window)
        self.origin_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.entry_window, text="Destination:").grid(row=1, column=0, padx=5, pady=5)
        self.destination_entry = ttk.Entry(self.entry_window)
        self.destination_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.entry_window, text="Total Load Pay ($):").grid(row=2, column=0, padx=5, pady=5)
        self.load_pay_entry = ttk.Entry(self.entry_window)
        self.load_pay_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.entry_window, text="Deadhead to Origin (miles):").grid(row=3, column=0, padx=5, pady=5)
        self.deadhead_to_origin_entry = ttk.Entry(self.entry_window)
        self.deadhead_to_origin_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.entry_window, text="Deadhead from Destination (miles):").grid(row=4, column=0, padx=5, pady=5)
        self.deadhead_from_destination_entry = ttk.Entry(self.entry_window)
        self.deadhead_from_destination_entry.grid(row=4, column=1, padx=5, pady=5)

        # Calculate Button
        self.calculate_button = ttk.Button(self.entry_window, text="Calculate", command=self.calculate_load_details)
        self.calculate_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def calculate_load_details(self):
        """Calculates load details, including profit, expenses, and rate per mile."""
        try:
            origin = self.origin_entry.get()
            destination = self.destination_entry.get()
            load_pay = float(self.load_pay_entry.get())
            deadhead_to_origin = float(self.deadhead_to_origin_entry.get())
            deadhead_from_destination = float(self.deadhead_from_destination_entry.get())

            # Determine total miles
            if (origin, destination) in self.distance_dict:
                total_miles = self.distance_dict[(origin, destination)]
            else:
                total_miles = float(messagebox.askstring("Unknown Route", "Enter distance in miles:"))

            total_distance = total_miles + deadhead_to_origin + deadhead_from_destination
            rate_per_mile = load_pay / total_distance

            # Calculate expenses
            fuel_cost = total_distance * FUEL_COST_PER_MILE
            dispatcher_fee = load_pay * DISPATCHER_FEE_RATE
            maintenance_cost = total_distance * MAINTENANCE_COST_PER_MILE
            total_expenses = fuel_cost + dispatcher_fee + maintenance_cost + DEFAULT_TOLL_COST
            net_profit = load_pay - total_expenses

            # Show results in new window
            result_text = (
                f"Total Distance: {total_distance:.2f} miles\n"
                f"Rate per Mile: ${rate_per_mile:.2f}\n"
                f"Fuel Cost: ${fuel_cost:.2f}\n"
                f"Dispatcher Fee: ${dispatcher_fee:.2f}\n"
                f"Maintenance Cost: ${maintenance_cost:.2f}\n"
                f"Tolls: ${DEFAULT_TOLL_COST:.2f}\n"
                f"Total Expenses: ${total_expenses:.2f}\n"
                f"Net Profit: ${net_profit:.2f}\n"
            )

            messagebox.showinfo("Load Calculation Result", result_text)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values.")

    def view_booked_loads(self):
        """Displays booked loads in new window."""
        self.booked_window = tk.Toplevel(self.root)
        self.booked_window.title("Booked Loads")
        ttk.Label(self.booked_window, text="(Feature Under Development)").pack(padx=10, pady=10)

    def view_considered_loads(self):
        """Displays considered loads in new window."""
        self.considered_window = tk.Toplevel(self.root)
        self.considered_window.title("Loads Under Consideration")
        ttk.Label(self.considered_window, text="(Feature Under Development)").pack(padx=10, pady=10)

def main():
    """Main function to start app."""
    root = tk.Tk()
    app = LoadCalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
