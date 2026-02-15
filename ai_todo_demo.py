#!/usr/bin/env python3
"""
AI-Powered Gamified To-Do App - DEMO MODE

This demo simulates the app running without network dependencies.
It demonstrates all core functionality using mock data.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")

# Simulated database
class MockDatabase:
    def __init__(self):
        self.users = {}
        self.tasks = {}
        self.user_id_counter = 1
        self.task_id_counter = 1
    
    def create_user(self, username: str) -> Dict:
        user = {
            "id": self.user_id_counter,
            "username": username,
            "total_xp": 0,
            "level": 1,
            "streak": 0,
            "last_completion_date": None,
            "created_at": datetime.now().isoformat()
        }
        self.users[self.user_id_counter] = user
        self.user_id_counter += 1
        return user
    
    def create_task(self, user_id: int, task_data: Dict) -> Dict:
        task = {
            "id": self.task_id_counter,
            "user_id": user_id,
            "title": task_data["title"],
            "deadline": task_data["deadline"],
            "complexity": task_data["complexity"],
            "priority_score": task_data["priority_score"],
            "xp": task_data["xp"],
            "completed": False,
            "reminder_sent": False,
            "motivation": None,
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        self.tasks[self.task_id_counter] = task
        self.task_id_counter += 1
        return task
    
    def complete_task(self, task_id: int, user_id: int) -> Dict:
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError("Task not found")
        
        task["completed"] = True
        task["completed_at"] = datetime.now().isoformat()
        task["motivation"] = "Great job! You're crushing your goals! 🎉"
        
        # Update user XP
        user = self.users.get(user_id)
        user["total_xp"] += task["xp"]
        user["level"] = (user["total_xp"] // 100) + 1
        user["streak"] += 1
        user["last_completion_date"] = datetime.now().isoformat()
        
        return task
    
    def get_user_tasks(self, user_id: int, completed: bool = None) -> List[Dict]:
        tasks = [t for t in self.tasks.values() if t["user_id"] == user_id]
        if completed is not None:
            tasks = [t for t in tasks if t["completed"] == completed]
        # Sort by priority score descending
        tasks.sort(key=lambda x: x["priority_score"], reverse=True)
        return tasks

# AI Service Simulator
class MockAIService:
    def parse_task(self, input_text: str) -> Dict:
        """Simulate AI parsing of task input"""
        text_lower = input_text.lower()
        
        # Extract title (simplified)
        title = input_text
        
        # Detect complexity
        complexity = "medium"
        if any(word in text_lower for word in ["easy", "simple", "quick", "buy", "call"]):
            complexity = "easy"
        elif any(word in text_lower for word in ["hard", "complex", "project", "study", "code", "build"]):
            complexity = "hard"
        
        # Parse deadline
        deadline = None
        if "tomorrow" in text_lower:
            deadline = (datetime.now() + timedelta(days=1)).replace(hour=23, minute=59)
        elif "today" in text_lower:
            deadline = datetime.now().replace(hour=23, minute=59)
        elif "next week" in text_lower:
            deadline = (datetime.now() + timedelta(days=7)).replace(hour=23, minute=59)
        elif "in 3 days" in text_lower:
            deadline = (datetime.now() + timedelta(days=3)).replace(hour=23, minute=59)
        
        return {
            "title": title,
            "deadline": deadline.isoformat() if deadline else None,
            "complexity": complexity
        }

# Priority Calculator
def calculate_priority_score(deadline_str: str, complexity: str) -> float:
    """Calculate priority score based on deadline and complexity"""
    score = 0.0
    
    # Deadline urgency (0-70 points)
    if deadline_str:
        deadline = datetime.fromisoformat(deadline_str)
        now = datetime.now()
        hours_until = (deadline - now).total_seconds() / 3600
        
        if hours_until < 0:
            score += 70  # Overdue
        elif hours_until <= 24:
            score += 60  # Within 24 hours
        elif hours_until <= 72:
            score += 40  # Within 3 days
        elif hours_until <= 168:
            score += 20  # Within 1 week
        else:
            score += 5   # More than a week
    else:
        score += 1  # No deadline
    
    # Complexity weight (10-30 points)
    complexity_scores = {"easy": 10, "medium": 20, "hard": 30}
    score += complexity_scores.get(complexity, 20)
    
    return round(score, 2)

def get_xp_reward(complexity: str) -> int:
    """Get XP reward based on complexity"""
    xp_mapping = {"easy": 10, "medium": 25, "hard": 50}
    return xp_mapping.get(complexity, 25)

# Demo Application
def run_demo():
    print_header("🎮 AI-POWERED GAMIFIED TO-DO APP - DEMO MODE")
    
    print(f"{Colors.CYAN}This demo simulates the complete application without network dependencies.{Colors.ENDC}")
    print(f"{Colors.CYAN}It demonstrates all core MVP features.{Colors.ENDC}\n")
    
    db = MockDatabase()
    ai = MockAIService()
    
    # Step 1: Create User
    print_header("Step 1: Creating User")
    user = db.create_user("demo_user")
    print_success(f"Created user: {user['username']}")
    print(json.dumps(user, indent=2, default=str))
    
    # Step 2: Create Tasks
    print_header("Step 2: Creating Tasks with AI Parsing")
    
    test_inputs = [
        "Buy groceries tomorrow",
        "Finish project report by next week",
        "Study for final exam in 3 days",
        "Quick email to team",
        "Build authentication system - complex project"
    ]
    
    created_tasks = []
    for i, input_text in enumerate(test_inputs, 1):
        print(f"\n{Colors.BOLD}Task {i}: \"{input_text}\"{Colors.ENDC}")
        
        # AI parsing
        parsed = ai.parse_task(input_text)
        print_info(f"AI Parsed → Title: '{parsed['title']}', Complexity: {parsed['complexity']}")
        
        # Calculate priority
        priority_score = calculate_priority_score(parsed['deadline'], parsed['complexity'])
        xp = get_xp_reward(parsed['complexity'])
        
        task_data = {
            "title": parsed["title"],
            "deadline": parsed["deadline"],
            "complexity": parsed["complexity"],
            "priority_score": priority_score,
            "xp": xp
        }
        
        task = db.create_task(user["id"], task_data)
        created_tasks.append(task)
        
        print_success(f"Created task ID {task['id']} | Priority: {priority_score} | XP: {xp}")
    
    # Step 3: Show All Tasks
    print_header("Step 3: All Tasks (Sorted by Priority)")
    
    tasks = db.get_user_tasks(user["id"])
    
    print(f"\n{'ID':<5} {'Title':<40} {'Priority':<10} {'Complexity':<12} {'XP':<5}")
    print(f"{'-'*5} {'-'*40} {'-'*10} {'-'*12} {'-'*5}")
    
    for task in tasks:
        color = Colors.RED if task['priority_score'] >= 60 else Colors.YELLOW if task['priority_score'] >= 40 else Colors.GREEN
        print(f"{task['id']:<5} {task['title'][:40]:<40} {color}{task['priority_score']:<10.2f}{Colors.ENDC} {task['complexity']:<12} {task['xp']:<5}")
    
    # Step 4: Daily Missions (Top 3)
    print_header("Step 4: Daily Mission Tasks (Top 3 Priorities)")
    
    mission_tasks = tasks[:3]
    
    for i, task in enumerate(mission_tasks, 1):
        print(f"\n{Colors.BOLD}🎯 Mission #{i}{Colors.ENDC}")
        print(f"   Title: {task['title']}")
        print(f"   Priority: {Colors.RED if task['priority_score'] >= 60 else Colors.YELLOW}{task['priority_score']}{Colors.ENDC}")
        print(f"   XP Reward: {Colors.GREEN}{task['xp']}{Colors.ENDC}")
        if task['deadline']:
            deadline = datetime.fromisoformat(task['deadline'])
            print(f"   Deadline: {deadline.strftime('%Y-%m-%d %H:%M')}")
    
    # Step 5: Complete a Task
    print_header("Step 5: Completing a Task")
    
    task_to_complete = created_tasks[0]
    print(f"{Colors.BOLD}Completing: \"{task_to_complete['title']}\"{Colors.ENDC}\n")
    
    completed_task = db.complete_task(task_to_complete["id"], user["id"])
    
    print_success(f"Task completed!")
    print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 {completed_task['motivation']}{Colors.ENDC}")
    print(f"{Colors.CYAN}+{completed_task['xp']} XP earned!{Colors.ENDC}")
    
    # Step 6: User Stats
    print_header("Step 6: User Statistics")
    
    updated_user = db.users[user["id"]]
    total_tasks = len(db.get_user_tasks(user["id"]))
    completed_tasks = len(db.get_user_tasks(user["id"], completed=True))
    pending_tasks = total_tasks - completed_tasks
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    print(f"{Colors.BOLD}User Profile:{Colors.ENDC}")
    print(f"  Username: {updated_user['username']}")
    print(f"  Level: {Colors.GREEN}{updated_user['level']}{Colors.ENDC}")
    print(f"  Total XP: {Colors.CYAN}{updated_user['total_xp']}{Colors.ENDC}")
    print(f"  Streak: {Colors.YELLOW}{updated_user['streak']} days{Colors.ENDC}")
    print(f"\n{Colors.BOLD}Task Statistics:{Colors.ENDC}")
    print(f"  Total Tasks: {total_tasks}")
    print(f"  Completed: {Colors.GREEN}{completed_tasks}{Colors.ENDC}")
    print(f"  Pending: {Colors.YELLOW}{pending_tasks}{Colors.ENDC}")
    print(f"  Completion Rate: {completion_rate:.1f}%")
    
    next_level_xp = (updated_user['level'] * 100) - updated_user['total_xp']
    print(f"\n{Colors.BOLD}Progress to Next Level:{Colors.ENDC}")
    print(f"  XP Needed: {Colors.CYAN}{next_level_xp} XP{Colors.ENDC}")
    
    # Step 7: Dashboard Data
    print_header("Step 7: Dashboard Data (for Mobile App)")
    
    dashboard = {
        "user": updated_user,
        "mission_tasks": mission_tasks,
        "recent_tasks": tasks[:5],
        "total_pending": pending_tasks
    }
    
    print(json.dumps(dashboard, indent=2, default=str))
    
    # Step 8: Priority Algorithm Demo
    print_header("Step 8: Priority Scoring Algorithm Explained")
    
    print(f"{Colors.BOLD}Priority Score = Deadline Urgency (0-70) + Complexity Weight (10-30){Colors.ENDC}\n")
    
    print(f"{Colors.CYAN}Deadline Urgency:{Colors.ENDC}")
    print(f"  • Overdue: 70 points")
    print(f"  • Within 24 hours: 60 points")
    print(f"  • Within 3 days: 40 points")
    print(f"  • Within 1 week: 20 points")
    print(f"  • More than 1 week: 5 points")
    print(f"  • No deadline: 1 point")
    
    print(f"\n{Colors.CYAN}Complexity Weight:{Colors.ENDC}")
    print(f"  • Easy: 10 points (10 XP reward)")
    print(f"  • Medium: 20 points (25 XP reward)")
    print(f"  • Hard: 30 points (50 XP reward)")
    
    print(f"\n{Colors.YELLOW}Example:{Colors.ENDC}")
    print(f"  Task: Hard project due in 12 hours")
    print(f"  Urgency: 60 points (< 24 hours)")
    print(f"  Complexity: 30 points (hard)")
    print(f"  {Colors.GREEN}Total Priority Score: 90 points{Colors.ENDC}")
    
    # Final Summary
    print_header("🎉 Demo Complete!")
    
    print(f"{Colors.GREEN}{Colors.BOLD}✅ All Core Features Demonstrated:{Colors.ENDC}")
    print(f"  ✓ User creation and management")
    print(f"  ✓ AI-powered task parsing (simulated)")
    print(f"  ✓ Intelligent priority scoring")
    print(f"  ✓ XP rewards and leveling system")
    print(f"  ✓ Streak tracking")
    print(f"  ✓ Daily mission tasks (top 3)")
    print(f"  ✓ Task completion with motivation")
    print(f"  ✓ Comprehensive statistics")
    print(f"  ✓ Dashboard data for mobile apps")
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}📱 Next Steps:{Colors.ENDC}")
    print(f"  1. Install dependencies: pip install -r requirements.txt")
    print(f"  2. Add your Anthropic API key to .env file")
    print(f"  3. Run the server: python -m uvicorn app.main:app --reload")
    print(f"  4. Visit http://localhost:8000/docs for interactive API docs")
    print(f"  5. Test with: python test_api.py")
    
    print(f"\n{Colors.YELLOW}{Colors.BOLD}📚 Documentation:{Colors.ENDC}")
    print(f"  • QUICKSTART.md - Get started in 5 minutes")
    print(f"  • README.md - Complete API reference")
    print(f"  • PROJECT_SUMMARY.md - Architecture overview")
    print(f"  • ARCHITECTURE.md - Detailed system design")
    
    print(f"\n{Colors.GREEN}The complete, production-ready backend is ready to use! 🚀{Colors.ENDC}\n")

if __name__ == "__main__":
    run_demo()
