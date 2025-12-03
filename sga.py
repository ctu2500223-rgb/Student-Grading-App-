import sys
import json
import os # We need 'os' to check if the file exists

# --- Persistent Storage Configuration ---
FILE_NAME = "student_grades.json"

# Main data structure: a dictionary to store all student data.
student_data = {}

def load_data():
    """Loads student data from a JSON file if it exists."""
    global student_data
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r') as f:
            try:
                student_data = json.load(f)
                print(f"Data loaded successfully from {FILE_NAME}.")
            except json.JSONDecodeError:
                # Handle case where file is empty or corrupted
                student_data = {}
                print("Warning: Could not decode data file. Starting with empty records.")
    else:
        print(f"No existing data file ({FILE_NAME}) found. Starting with empty records.")

def save_data():
    """Saves the current student data to a JSON file."""
    with open(FILE_NAME, 'w') as f:
        json.dump(student_data, f, indent=4)
        print(f"Data saved successfully to {FILE_NAME}.")

def add_student(name):
    """Adds a new student to the records if they don't already exist."""
    if name in student_data:
        print(f"Error: {name} already exists.")
    else:
        student_data[name] = {}
        print(f"Added new student: {name}")

def add_grade(name, subject, grade):
    """Adds or updates a grade for an existing student and subject."""
    if name not in student_data:
        print(f"Error: {name} not found. Please add the student first.")
        return

    try:
        # Convert grade to float to allow for calculation
        grade = float(grade)
        if 0 <= grade <= 100:
            student_data[name][subject] = grade
            print(f"Added grade for {name} in {subject}: {grade}")
        else:
            print("Error: Grade must be between 0 and 100.")
    except ValueError:
        print("Error: Invalid grade format. Please enter a number.")

def calculate_average_grade(name):
    """Calculates the average grade for a specific student."""
    if name not in student_data or not student_data[name]:
        return "N/A"
    
    grades = student_data[name].values()
    average = sum(grades) / len(grades)
    return round(average, 2)

def view_student_report(name):
    """Displays a full report for a single student."""
    if name not in student_data:
        print(f"Error: {name} not found.")
        return

    print(f"\n--- Report for {name} ---")
    if not student_data[name]:
        print("No grades recorded yet.")
        return

    for subject, grade in student_data[name].items():
        print(f"  {subject}: {grade}")
    
    average = calculate_average_grade(name)
    print(f"  Overall Average: {average}")
    print("-" * (len(name) + 18))

def calculate_class_subject_average(subject):
    """Calculates the average grade for a specific subject across all students."""
    total_grades = 0
    student_count = 0
    
    for name, subjects in student_data.items():
        if subject in subjects:
            total_grades += subjects[subject]
            student_count += 1
    
    if student_count == 0:
        return "N/A"

    average = total_grades / student_count
    return round(average, 2)

# --- Deletion Functions ---

def delete_student(name):
    """Deletes an entire student record from the system."""
    if name in student_data:
        del student_data[name]
        print(f"Successfully deleted student: {name}.")
    else:
        print(f"Error: Student '{name}' not found.")

def delete_grade(name, subject):
    """Deletes a single grade for a student and subject."""
    if name not in student_data:
        print(f"Error: Student '{name}' not found.")
        return
    
    if subject in student_data[name]:
        del student_data[name][subject]
        print(f"Successfully deleted grade for {name} in {subject}.")
    else:
        print(f"Error: Subject '{subject}' not found for student '{name}'.")

# --- Menu Functions ---

def delete_menu():
    """Sub-menu for deletion operations."""
    while True:
        print("\n*** Delete Menu ***")
        print("1. Delete a student (and all their grades)")
        print("2. Delete a single grade (for a student/subject)")
        print("3. Back to Main Menu")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            name = input("Enter student name to delete: ")
            delete_student(name)
        elif choice == '2':
            name = input("Enter student name: ")
            subject = input("Enter subject name to delete grade for: ")
            delete_grade(name, subject)
        elif choice == '3':
            return
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

def main_menu():
    """Provides a command-line interface for the application."""
    # Load data at the start of the application
    load_data() 
    
    while True:
        print("\n*** Students Grading App Menu ***")
        print("1. Add a new student")
        print("2. Add a grade for a student")
        print("3. View a student report")
        print("4. Calculate class average for a subject")
        print("5. View all students")
        print("6. Delete Data (Student or Grade)") # New menu option
        print("7. Exit (Save Data)") # Updated exit option
        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            name = input("Enter student name: ")
            add_student(name)
        elif choice == '2':
            name = input("Enter student name: ")
            subject = input("Enter subject name: ")
            grade = input("Enter grade: ")
            add_grade(name, subject, grade)
        elif choice == '3':
            name = input("Enter student name to view report: ")
            view_student_report(name)
        elif choice == '4':
            subject = input("Enter subject name to calculate class average: ")
            average = calculate_class_subject_average(subject)
            if average != "N/A":
                print(f"Class average for {subject}: {average}")
            else:
                print(f"No grades found for subject: {subject}")
        elif choice == '5':
            print("\nCurrent Students:")
            if not student_data:
                print("(No students recorded)")
            for name in student_data:
                print(f"- {name}")
        elif choice == '6':
            delete_menu() # Call the new sub-menu
        elif choice == '7':
            save_data() # Save data before exiting
            print("Exiting application. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main_menu()