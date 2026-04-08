import json
import os

class StudentManager:
    def __init__(self, filename='students.json'):
        self.filename = filename
        self.students = self.load_students()

    def load_students(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_students(self):
        with open(self.filename, 'w') as f:
            json.dump(self.students, f, indent=4)

    def add_student(self, name, age, grade, roll, contact, email, address, marks):
        student = {
            "name": name,
            "age": age,
            "grade": grade,
            "roll": roll,
            "contact": contact,
            "email": email,
            "address": address,
            "marks": marks
        }
        self.students.append(student)
        self.save_students()
        print(f"Student {name} added successfully.")

    def view_students(self):
        if not self.students:
            print("No students found.")
            return
        
        print("\n--- Student List ---")
        for idx, s in enumerate(self.students, 1):
            name = s.get('name', 'N/A')
            roll = s.get('roll', 'N/A')
            grade = s.get('grade', 'N/A')
            age = s.get('age', 'N/A')
            contact = s.get('contact', 'N/A')
            email = s.get('email', 'N/A')
            address = s.get('address', 'N/A')
            marks = s.get('marks', 'N/A')
            print(f"{idx}. {name} (Roll: {roll}, Grade: {grade}, Age: {age})")
            print(f"   Contact: {contact}, Email: {email}, Address: {address}, Marks: {marks}")

    def edit_student(self, index):
        if 0 <= index < len(self.students):
            student = self.students[index]
            print(f"\nEditing: {student.get('name', 'New Student')}")
            print("Leave blank to keep current value.")
            
            student['name'] = input(f"Enter Name [{student.get('name', '')}]: ") or student.get('name', '')
            student['age'] = input(f"Enter Age [{student.get('age', '')}]: ") or student.get('age', '')
            student['grade'] = input(f"Enter Grade [{student.get('grade', '')}]: ") or student.get('grade', '')
            student['roll'] = input(f"Enter Roll [{student.get('roll', '')}]: ") or student.get('roll', '')
            student['contact'] = input(f"Enter Contact [{student.get('contact', '')}]: ") or student.get('contact', '')
            student['email'] = input(f"Enter Email [{student.get('email', '')}]: ") or student.get('email', '')
            student['address'] = input(f"Enter Address [{student.get('address', '')}]: ") or student.get('address', '')
            student['marks'] = input(f"Enter Marks [{student.get('marks', '')}]: ") or student.get('marks', '')
            
            self.save_students()
            print("Student updated successfully.")
        else:
            print("Invalid index.")

    def search_student(self, name):
        results = [s for s in self.students if name.lower() in s.get('name', '').lower()]
        if results:
            for s in results:
                print(f"Found: Name: {s.get('name', 'N/A')}, Roll: {s.get('roll', 'N/A')}, Grade: {s.get('grade', 'N/A')}")
        else:
            print("No student found with that name.")

def main():
    manager = StudentManager()
    
    while True:
        print("\nStudent Management System")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Edit Student")
        print("5. Exit")
        
        choice = input("Enter choice (1-5): ")
        
        if choice == '1':
            name = input("Enter Name: ")
            age = input("Enter Age: ")
            grade = input("Enter Grade: ")
            roll = input("Enter Roll: ")
            contact = input("Enter Contact: ")
            email = input("Enter Email: ")
            address = input("Enter Address: ")
            marks = input("Enter Marks: ")
            manager.add_student(name, age, grade, roll, contact, email, address, marks)
        elif choice == '2':
            manager.view_students()
        elif choice == '3':
            name = input("Enter Name to search: ")
            manager.search_student(name)
        elif choice == '4':
            manager.view_students()
            if manager.students:
                try:
                    idx = int(input("Enter student number to edit: ")) - 1
                    manager.edit_student(idx)
                except ValueError:
                    print("Please enter a valid number.")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
