import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import pandas as pd

# Create main window
root = tk.Tk()
root.title("Employee Management")

# Fields
fields = ["ID", "Name", "Department", "Position", "DOB", "Gender", "ID Number"]

# Input Entries
entries = {}

# Function to save data to CSV
def save_data():
    data = {field: entry.get() for field, entry in entries.items()}
    with open("employees.csv", mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        if file.tell() == 0:  # Write header if file is empty
            writer.writeheader()
        writer.writerow(data)
    messagebox.showinfo("Success", "Employee data saved successfully!")

# Function to find today's birthdays
def find_birthdays():
    today = datetime.now().strftime("%m-%d")
    with open("employees.csv", "r") as file:
        reader = csv.DictReader(file)
        birthdays = [row for row in reader if row["DOB"][5:] == today]
    if birthdays:
        messagebox.showinfo("Birthdays Today", "\n".join([row["Name"] for row in birthdays]))
    else:
        messagebox.showinfo("Birthdays Today", "No birthdays today!")

# Function to export sorted data to Excel
def export_to_excel():
    data = pd.read_csv("employees.csv")
    data["DOB"] = pd.to_datetime(data["DOB"])  # Ensure DOB is in datetime format
    sorted_data = data.sort_values(by="DOB", ascending=False)  # Sort by age
    sorted_data.to_excel("sorted_employees.xlsx", index=False)
    messagebox.showinfo("Success", "Data exported to sorted_employees.xlsx!")

# Create form
for idx, field in enumerate(fields):
    tk.Label(root, text=field).grid(row=idx, column=0, sticky="w")
    entry = tk.Entry(root)
    entry.grid(row=idx, column=1, pady=5)
    entries[field] = entry

# Gender options
gender_var = tk.StringVar(value="Male")
tk.Radiobutton(root, text="Male", variable=gender_var, value="Male").grid(row=5, column=1, sticky="w")
tk.Radiobutton(root, text="Female", variable=gender_var, value="Female").grid(row=5, column=1, sticky="e")
entries["Gender"] = gender_var

# Buttons
tk.Button(root, text="Save Data", command=save_data).grid(row=len(fields), column=0, pady=10)
tk.Button(root, text="Find Birthdays", command=find_birthdays).grid(row=len(fields), column=1, pady=10)
tk.Button(root, text="Export to Excel", command=export_to_excel).grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

# Start the GUI event loop
root.mainloop()