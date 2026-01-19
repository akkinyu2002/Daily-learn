import random
import time
import os
import requests
import html

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class AdaptiveQuiz:
    def __init__(self):
        # Initial question bank with 50 Python questions
        self.local_questions = [
            {"question": "Which keyword is used to define a function in Python?", "options": ["func", "define", "def", "function"], "answer": "def", "weight": 1},
            {"question": "Which of the following data types is mutable in Python?", "options": ["tuple", "string", "list", "int"], "answer": "list", "weight": 1},
            {"question": "What is the output of '2' + '3' in Python?", "options": ["5", "23", "Error", "None of the above"], "answer": "23", "weight": 1},
            {"question": "Which operator is used for exponentiation in Python?", "options": ["^", "**", "*", "//"], "answer": "**", "weight": 1},
            {"question": "What is the correct way to comment out multiple lines in Python?", "options": ["// This is a comment", "/* This is a comment */", "# This is a comment", "''' This is a comment '''"], "answer": "''' This is a comment '''", "weight": 1},
            {"question": "Which of the following is not a valid variable name in Python?", "options": ["_myVar", "myVar2", "2myVar", "my_var"], "answer": "2myVar", "weight": 1},
            {"question": "What does the 'len()' function do in Python?", "options": ["Calculates length", "Checks if empty", "Converts to lowercase", "Returns largest item"], "answer": "Calculates length", "weight": 1},
            {"question": "What is the primary purpose of 'if __name__ == \"__main__\":'?", "options": ["Define main", "Mark start", "Execute if run directly", "Import modules"], "answer": "Execute if run directly", "weight": 1},
            {"question": "Which of these is used to create an empty set in Python?", "options": ["{}", "set()", "[]", "()"], "answer": "set()", "weight": 1},
            {"question": "What is the output of 'type([])'?", "options": ["<class 'list'>", "<class 'array'>", "<class 'tuple'>", "<class 'dict'>"], "answer": "<class 'list'>", "weight": 1},
            {"question": "Which statement is used to exit a loop prematurely?", "options": ["exit", "stop", "break", "continue"], "answer": "break", "weight": 1},
            {"question": "Which keyword is used to handle exceptions in Python?", "options": ["catch", "except", "try", "throw"], "answer": "except", "weight": 1},
            {"question": "What will 'bool(\"False\")' evaluate to?", "options": ["True", "False", "Error", "None"], "answer": "True", "weight": 1},
            {"question": "How do you access 'name' in dictionary 'person'?", "options": ["person.name", "person['name']", "person->name", "person(name)"], "answer": "person['name']", "weight": 1},
            {"question": "What is the result of '10 // 3'?", "options": ["3.33", "3", "4", "1"], "answer": "3", "weight": 1},
            {"question": "Which of the following is an immutable data type?", "options": ["list", "dictionary", "set", "tuple"], "answer": "tuple", "weight": 1},
            {"question": "What does 'pip' stand for?", "options": ["Python Install", "Preferred Installer Program", "Pre-installed", "Programming Interface"], "answer": "Preferred Installer Program", "weight": 1},
            {"question": "Which built-in function converts an integer to a string?", "options": ["int_to_str()", "to_string()", "str()", "convert_str()"], "answer": "str()", "weight": 1},
            {"question": "What is the default return value for a function without 'return'?", "options": ["0", "null", "None", "undefined"], "answer": "None", "weight": 1},
            {"question": "What is the purpose of 'self' in class methods?", "options": ["Refer to superclass", "Refer to current instance", "Reserved keyword", "Define private var"], "answer": "Refer to current instance", "weight": 1},
            {"question": "Which method adds an item to the end of a list?", "options": ["add()", "insert()", "append()", "extend()"], "answer": "append()", "weight": 1},
            {"question": "What is the output of '\"hello\".upper()'?", "options": ["hello", "HELLO", "Hello", "Error"], "answer": "HELLO", "weight": 1},
            {"question": "How do you create a class in Python?", "options": ["class MyClass:", "def MyClass:", "create class MyClass:", "class = MyClass"], "answer": "class MyClass:", "weight": 1},
            {"question": "Which is not a looping construct in Python?", "options": ["for loop", "while loop", "do-while loop", "recursion"], "answer": "do-while loop", "weight": 1},
            {"question": "What is the purpose of 'pass' statement?", "options": ["Exit loop", "Skip iteration", "Null operation", "Raise exception"], "answer": "Null operation", "weight": 1},
            {"question": "What is the correct syntax for 'if' statement?", "options": ["if cond {", "if cond:", "if (cond)", "if cond then"], "answer": "if cond:", "weight": 1},
            {"question": "Which module is used for regular expressions?", "options": ["regex", "re", "regexp", "pattern"], "answer": "re", "weight": 1},
            {"question": "What does '*args' allow?", "options": ["Keyword args", "Arbitrary positional args", "Default args", "By reference"], "answer": "Arbitrary positional args", "weight": 1},
            {"question": "What is a docstring?", "options": ["Single-line comment", "String for documentation", "Error message", "Special variable"], "answer": "String for documentation", "weight": 1},
            {"question": "Which function gets input?", "options": ["get_input()", "read()", "input()", "console.read()"], "answer": "input()", "weight": 1},
            {"question": "What is slicing in Python?", "options": ["Divide list", "Extract portion", "Remove elements", "Sorting"], "answer": "Extract portion", "weight": 1},
            {"question": "What is GIL?", "options": ["Parallel execution", "Protects objects", "Multi-thread tool", "GC optimization"], "answer": "Protects objects", "weight": 1},
            {"question": "Python supports multiple inheritance?", "options": ["True", "False"], "answer": "True", "weight": 1},
            {"question": "What is 'lambda'?", "options": ["Multi-return func", "Anonymous function", "Math-only func", "Inner function"], "answer": "Anonymous function", "weight": 1},
            {"question": "Which module for OS functions?", "options": ["sys", "math", "os", "random"], "answer": "os", "weight": 1},
            {"question": "How remove element by value?", "options": ["delete", "remove", "pop", "del"], "answer": "remove", "weight": 1},
            {"question": "Purpose of try-except?", "options": ["Define func", "Handle errors", "Conditionals", "Iterate"], "answer": "Handle errors", "weight": 1},
            {"question": "Which module for JSON?", "options": ["pickle", "json", "csv", "xml"], "answer": "json", "weight": 1},
            {"question": "Import 'math' correctly?", "options": ["include math", "require math", "import math", "using math"], "answer": "import math", "weight": 1},
            {"question": "Difference between '==' and 'is'?", "options": ["ID vs Value", "Value vs ID", "Identical", "None"], "answer": "Value vs ID", "weight": 1},
            {"question": "What is a generator?", "options": ["Random gen", "Produces sequence", "Dynamic objects", "Sequence type"], "answer": "Produces sequence", "weight": 1},
            {"question": "What does 'range()' return?", "options": ["List", "Tuple", "Iterator", "String"], "answer": "Iterator", "weight": 1},
            {"question": "Result of 'print(0.1 + 0.2 == 0.3)'?", "options": ["True", "False", "Error", "Version dependent"], "answer": "False", "weight": 1},
            {"question": "Removes and returns last item?", "options": ["remove", "delete", "pop", "clear"], "answer": "pop", "weight": 1},
            {"question": "Randomize list in place?", "options": ["list.shuffle()", "random.shuffle(list)", "list.randomize()", "shuffle(list)"], "answer": "random.shuffle(list)", "weight": 1},
            {"question": "What is an f-string?", "options": ["Special chars", "Embedded expressions", "Fixed length", "File paths"], "answer": "Embedded expressions", "weight": 1},
            {"question": "Open file function?", "options": ["file_open", "read_file", "open", "load_file"], "answer": "open", "weight": 1},
            {"question": "Syntax to create dictionary?", "options": ["[]", "()", "{}", "new dict()"], "answer": "{}", "weight": 1},
            {"question": "What does 'enumerate()' do?", "options": ["Permutations", "Adds counter", "Checks unique", "Converts type"], "answer": "Adds counter", "weight": 1},
            {"question": "Which is not a standard module?", "options": ["os", "sys", "django", "math"], "answer": "django", "weight": 1},
        ]
        self.questions = []
        self.score = 0
        self.total_asked = 0
        self.mode = "local"

    def fetch_api_questions(self, amount=10):
        try:
            url = f"https://opentdb.com/api.php?amount={amount}&type=multiple"
            response = requests.get(url)
            data = response.json()
            if data['response_code'] == 0:
                new_questions = []
                for q in data['results']:
                    options = q['incorrect_answers'] + [q['correct_answer']]
                    # Decode HTML entities
                    decoded_q = html.unescape(q['question'])
                    decoded_options = [html.unescape(opt) for opt in options]
                    decoded_answer = html.unescape(q['correct_answer'])
                    
                    new_questions.append({
                        "question": decoded_q,
                        "options": decoded_options,
                        "answer": decoded_answer,
                        "weight": 1
                    })
                return new_questions
            else:
                return []
        except Exception as e:
            print(f"Error fetching questions: {e}")
            return []

    def select_mode(self):
        clear_screen()
        print("--- Adaptive Quiz Mode Selection ---")
        print("1. Local Python Quiz (50+ questions)")
        print("2. Online General Trivia (Unlimited / API)")
        print("q. Quit")
        
        choice = input("\nSelect mode (1/2/q): ").strip().lower()
        if choice == '1':
            self.mode = "local"
            self.questions = self.local_questions
        elif choice == '2':
            self.mode = "online"
            print("Fetching initial questions from OpenTDB...")
            self.questions = self.fetch_api_questions(10)
        elif choice == 'q':
            exit()
        else:
            print("Invalid choice, defaulting to Local Mode.")
            self.questions = self.local_questions
            time.sleep(1)

    def get_weighted_question(self):
        if self.mode == "online" and len(self.questions) < 5:
            # Re-fetch if running low in online mode
            print("\nFetching more questions...")
            new_qs = self.fetch_api_questions(10)
            self.questions.extend(new_qs)

        weights = [q['weight'] for q in self.questions]
        return random.choices(self.questions, weights=weights, k=1)[0]

    def run(self):
        while True:
            self.select_mode()
            self.score = 0
            self.total_asked = 0
            round_limit = 10
            
            print(f"\nWelcome to the Adaptive Quiz! \U0001f4ca")
            print(f"You will be asked {round_limit} random questions.")
            print("Wrong answers will repeat more often in future rounds!")
            time.sleep(1.5)

            try:
                while self.total_asked < round_limit:
                    clear_screen()
                    if not self.questions:
                        print("No questions available!")
                        break

                    q = self.get_weighted_question()
                    
                    print(f"Mode: {self.mode.upper()} | Question: {self.total_asked + 1}/{round_limit} | Score: {self.score}")
                    print(f"\nQuestion: {q['question']}")
                    
                    options = list(q['options'])
                    random.shuffle(options)
                    
                    for i, opt in enumerate(options, 1):
                        print(f"{i}. {opt}")
                    
                    choice = input("\nYour answer (1-4) or 'q' to quit round: ").strip().lower()
                    
                    if choice == 'q':
                        break
                    
                    if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
                        print(f"Invalid input! Please enter a number 1-{len(options)}.")
                        time.sleep(1)
                        continue
                    
                    selected_answer = options[int(choice) - 1]
                    self.total_asked += 1

                    if selected_answer == q['answer']:
                        print("\n\u2705 Correct!")
                        self.score += 1
                        q['weight'] = max(1, q['weight'] - 1)
                    else:
                        print(f"\n\u274c Wrong! Correct was: {q['answer']}")
                        q['weight'] += 3
                        print(f"Weight increased! This question will haunt you later.")

                    time.sleep(1.5)

            except KeyboardInterrupt:
                break

            clear_screen()
            print("--- Quiz Results ---")
            print(f"Mode: {self.mode.upper()}")
            print(f"Total Questions Attempted: {self.total_asked}")
            print(f"Final Score: {self.score} / {self.total_asked}")
            if self.total_asked > 0:
                percentage = (self.score / self.total_asked) * 100
                print(f"Accuracy: {percentage:.2f}%")
            
            print("-" * 20)
            again = input("\nWould you like to play another round? (y/n): ").strip().lower()
            if again != 'y':
                break

        print("\nKeep learning and goodbye!")

if __name__ == "__main__":
    quiz = AdaptiveQuiz()
    quiz.run()
