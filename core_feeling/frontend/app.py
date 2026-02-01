from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from frontend.screens import MissionScreen, AddScreen, MoodScreen
import os

class CoreFeelingApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        
        # Load KV
        Builder.load_file(os.path.join("frontend", "styles.kv"))
        
        sm = MDScreenManager()
        
        # Main Layout with Bottom Nav (optional, or just screen switching)
        # For this "Cinematic" feel, let's just use ScreenManager and swipe/buttons
        
        mission_screen = MissionScreen(name="mission")
        add_screen = AddScreen(name="add")
        mood_screen = MoodScreen(name="mood")
        
        sm.add_widget(mood_screen) # Start with mood? Or Mission?
        sm.add_widget(mission_screen)
        sm.add_widget(add_screen)
        
        sm.current = "mood" # Start with mood check-in
        
        return sm

if __name__ == "__main__":
    CoreFeelingApp().run()
