from kivy.app import App
from kivy.lang.builder import Builder
from kivy.storage.jsonstore import JsonStore

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

# Approximate Pixel 7a screen size
#TODO: REMOVE THIS BEFORE BUILD
from kivy.core.window import Window
Window.size = (1080/3, 2400/3) 

class HomeScreen(BoxLayout):
        
    def save_text(self):
       self.store = JsonStore('data.json')
       text_data = self.store.get("Text")
       text_data["save"] = self.ids.text_label.text
       self.store.put("Text", default=text_data["default"], save=text_data["save"])

    def load_text(self):
        self.store = JsonStore('data.json')
        self.ids.text_box.text = self.store.get("Text")["save"]

    def update_display(self):
        self.store = JsonStore('data.json')
        text_data = self.store.get("Data")

        display_content  = f'Current week: {text_data["week_current"]} / {text_data["week_total"]}\n\n\n'
        display_content += f'This week:\n'
        display_content += f'\nSwipes remaining: {text_data["swipes_remaining"]} / {text_data["swipes_max"]}'
        display_content += f'\nDollars remaining: ${text_data["weekly_remaining"]} / ${text_data["weekly_max"]}\n\n'
        display_content += f'\nTotal:\n'
        display_content += f'\nDollars remaining: ${text_data["dollars_remaining"]} / ${text_data["dollars_total"]}'

        self.ids.display.text = display_content

class MealMaster(App):

    def build(self):
        
        Builder.load_file('main.kv')
        self.store = JsonStore('data.json')

        HS = HomeScreen()

        # HS.ids.text_box.text = self.store.get('Text')['default']
        # HS.ids.text_label.text = 'test'

        return HS

if __name__ == "__main__":
    MealMaster().run()