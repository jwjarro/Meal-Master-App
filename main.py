from kivy.app import App
from kivy.lang.builder import Builder
from kivy.storage.jsonstore import JsonStore

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

# Approximate Pixel 7a screen size
#TODO: REMOVE THIS BEFORE BUILD
# from kivy.core.window import Window
# Window.size = (1080/3, 2400/3) 

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
        display_content += f'\nDollars remaining: ${data["weekly_remaining"]:.2f} / ${data["weekly_max"]:.2f}\n\n'
        display_content += f'\nTotal:\n'
        display_content += f'\nDollars remaining: ${data["dollars_remaining"]:.2f} / ${data["dollars_total"]:.2f}'

        self.ids.display.text = display_content

    def meal_swipe(self):

        data = self.load_data()

        data["swipes_remaining"] -= 1

        self.save_data(data)

        self.update_display()

    def progress_week(self):

        data = self.load_data()

        data["week_current"] += 1
        data["week_remaining"] = data["week_total"] - data["week_current"] + 1
        if data["week_remaining"] != 0:
            data["weekly_max"] = data["dollars_remaining"] / data["week_remaining"]
        data["weekly_remaining"] = data["weekly_max"]
        data["swipes_remaining"] = data["swipes_max"]

        self.save_data(data)

        self.update_display()
        
class SettingsScreen(Screen):
    def update_weeks_remaining(self):
        if ((self.ids.week_total.text != "") and (self.ids.week_current.text != "")):
            self.ids.week_remaining.text = int(self.ids.week_total) - int(self.ids.week_current) + 1

    def apply_settings(self):

        data = HomeScreen.load_data(self)



        if self.ids.week_total.text != '':
            data["week_total"] = int(self.ids.week_total.text)

        if self.ids.week_current.text != '':
            data["week_current"] = int(self.ids.week_current.text)

        if (self.ids.week_total.text != '') and (self.ids.week_current.text != ''):
            data["week_remaining"] = int(self.ids.week_total.text) - int(self.ids.week_current.text) + 1

        if self.ids.dollars_total.text != '':
            data["dollars_total"] = float(self.ids.dollars_total.text)

        if self.ids.dollars_remaining.text != '':
            data["dollars_remaining"] = float(self.ids.dollars_remaining.text)

        if self.ids.weekly_max.text != '':
            data["weekly_max"] = float(self.ids.weekly_max.text)

        if self.ids.weekly_remaining.text != '':
            data["weekly_remaining"] = float(self.ids.weekly_remaining.text)

        if self.ids.swipes_max.text != '':
            data["swipes_max"] = int(self.ids.swipes_max.text)

        if self.ids.swipes_remaining.text != '':
            data["swipes_remaining"] = int(self.ids.swipes_remaining.text)



        if data['week_current'] == 0:
            data["dollars_remaining"] = data["dollars_total"]
            data["swipes_remaining"] = data["swipes_max"]

        self.ids.week_total.text = ''
        self.ids.week_current.text = ''
        self.ids.dollars_total.text = ''
        self.ids.dollars_remaining.text = ''
        self.ids.weekly_max.text = ''
        self.ids.weekly_remaining.text = ''
        self.ids.swipes_max.text = ''
        self.ids.swipes_remaining.text = ''

        HomeScreen.save_data(self, data)
        HomeScreen.update_display(self.manager.get_screen("home_screen"))

class DiningDollarScreen(Screen):
    
    def spend_dining_dollars(self):

        if (self.ids.input.text != ""):
            data = HomeScreen.load_data(self)

            data["weekly_remaining"] -= float(self.ids.input.text)
            data["dollars_remaining"] -= float(self.ids.input.text)

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