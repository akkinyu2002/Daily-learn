from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
import requests
import json

API_URL = "http://127.0.0.1:8000"

class MissionScreen(MDScreen):
    def on_enter(self):
        self.fetch_mission()

    def fetch_mission(self):
        try:
            # In a real app, do this asynchronously
            response = requests.get(f"{API_URL}/mission")
            if response.status_code == 200:
                self.render_mission(response.json())
        except Exception as e:
            print(f"Error fetching mission: {e}")

    def render_mission(self, data):
        task_list = self.ids.task_list
        task_list.clear_widgets()

        # Helper to create card
        def create_task_card(task, label_prefix=""):
            card = MDCard(
                orientation="vertical",
                size_hint_y=None,
                height="80dp",
                padding="10dp",
                radius=[15],
                md_bg_color=(0.1, 0.12, 0.15, 0.8) # Glass-ish
            )
            title = MDLabel(
                text=f"{label_prefix}{task['title']}",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_style="Subtitle1"
            )
            details = MDLabel(
                text=f"{task['time']} • {task['priority']}",
                theme_text_color="Secondary",
                font_style="Caption"
            )
            card.add_widget(title)
            card.add_widget(details)
            return card

        # Top 3
        for task in data.get("mission_tasks", []):
            task_list.add_widget(create_task_card(task))
        
        # Quick Win
        quick_win = data.get("quick_win")
        if quick_win:
             task_list.add_widget(create_task_card(quick_win, label_prefix="[Quick Win] "))

class AddScreen(MDScreen):
    def analyze_task(self):
        text = self.ids.input_field.text
        if not text:
            return
        
        try:
            response = requests.post(f"{API_URL}/tasks/magic_add", params={"user_input": text})
            if response.status_code == 200:
                print("Task Added!")
                self.ids.input_field.text = ""
                MDApp.get_running_app().root.current = "mission"
        except Exception as e:
            print(f"Error adding task: {e}")

class MoodScreen(MDScreen):
    def set_mood(self, mood):
        print(f"Selected Mood: {mood}")
        # In real app, store this in global state or send to backend
        # For now, just navigate to mission
        MDApp.get_running_app().root.current = "mission"
