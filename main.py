from kivy.app import App
from kivy.lang.builder import Builder
from kivy.storage.jsonstore import JsonStore

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

# Approximate Pixel 7a screen size
#TODO: REMOVE THIS BEFORE BUILD
from kivy.core.window import Window
Window.size = (1080/3, 2400/3) 

class AppScreenManager(ScreenManager):
    pass

class HomeScreen(Screen):

    def load_data(self):
        self.store = JsonStore('data.json')
        data = {}
        for key in self.store.keys():
            data[key] = self.store.get(key)["value"]
        return data
      
    def save_data(self, data):
       self.store = JsonStore('data.json')
       for key in data:
           self.store.put(key, value=data[key])

    def update_display(self):

        data = self.load_data()

        display_content  = f'Current week: {data["week_current"]} / {data["week_total"]}\n\n\n'
        display_content += f'This week:\n'
        display_content += f'\nSwipes remaining: {data["swipes_remaining"]} / {data["swipes_max"]}'
        display_content += f'\nDollars remaining: ${data["weekly_remaining"]} / ${data["weekly_max"]}\n\n'
        display_content += f'\nTotal:\n'
        display_content += f'\nDollars remaining: ${data["dollars_remaining"]} / ${data["dollars_total"]}'

        self.ids.display.text = display_content

    def meal_swipe(self):

        data = self.load_data()

        data["swipes_remaining"] -= 1

        self.save_data(data)

        self.update_display()

        
class SettingsScreen(Screen):
    pass

class DiningDollarScreen(Screen):
    
    def spend_dining_dollars(self):
        
        data = HomeScreen.load_data(self)

        data["weekly_remaining"] -= float(self.ids.input.text)

        HomeScreen.save_data(self, data)

        HomeScreen.update_display(self.manager.get_screen("home_screen"))

class MealMaster(App):

    def build(self):
        
        Builder.load_file('main.kv')

        Manager = AppScreenManager()
        Manager.current_screen.update_display()

        return Manager

if __name__ == "__main__":
    MealMaster().run()