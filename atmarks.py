def calculate_grade(average):
    if average >= 90:
        return 'A'
    elif average >= 80:
        return 'B'
    elif average >= 70:
        return 'C'
    elif average >= 60:
        return 'D'
    else:
        return 'F'

def main():
    students = {}
    
    print("--- Student Marks Management System ---")
    
    while True:
        name = input("\nEnter student name (or type 'exit' to finish): ").strip()
        if name.lower() == 'exit':
            break
            
        try:
            num_subjects = int(input(f"Enter number of subjects for {name}: "))
            marks = []
            for i in range(num_subjects):
                mark = float(input(f"  Enter mark for subject {i+1}: "))
                marks.append(mark)
            
            total = sum(marks)
            average = total / num_subjects if num_subjects > 0 else 0
            grade = calculate_grade(average)
            
            # Store in dictionary
            students[name] = {
                "marks": marks,
                "total": total,
                "average": round(average, 2),
                "grade": grade
            }
            print(f"Successfully added {name}!")
            
        except ValueError:
            print("Invalid input. Please enter numbers for marks and subject counts.")
            continue

    if not students:
        print("\nNo student records entered.")
        return

    print("\n" + "="*50)
    print(f"{'Name':<15} | {'Total':<10} | {'Average':<10} | {'Grade':<5}")
    print("-" * 50)
    for name, data in students.items():
        print(f"{name:<15} | {data['total']:<10} | {data['average']:<10} | {data['grade']:<5}")
    print("="*50)

if __name__ == "__main__":
    main()
