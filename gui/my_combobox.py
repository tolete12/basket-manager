from typing import List, Optional, Callable, Union

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.metrics import dp


class MyCombobox(MDBoxLayout):
    """
    A beautiful combobox implementation using KivyMD components.
    
    This combobox displays a text field with a dropdown menu of selectable items.
    """
    items = ListProperty([])
    selected_item = StringProperty("")
    hint_text = StringProperty("Select an item")
    on_select = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        """Initialize the combobox with optional parameters."""
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = [dp(5), 0, dp(5), 0]
        
        # Create the text field
        self.text_field = MDTextField(
            hint_text=self.hint_text,
            text=self.selected_item,
            readonly=True,
            size_hint=(0.8, None),
            height=dp(48)
        )
        
        # Create the dropdown button
        self.dropdown_button = MDRaisedButton(
            text="▼",
            size_hint=(0.2, None),
            height=dp(48),
            on_release=self.open_dropdown
        )
        
        # Add widgets to layout
        self.add_widget(self.text_field)
        self.add_widget(self.dropdown_button)
        
        # Initialize the dropdown menu
        self.dropdown_menu = None
        self._create_dropdown_menu()
    
    def _create_dropdown_menu(self) -> None:
        """Create the dropdown menu with the current items."""
        menu_items = [
            {
                "text": item,
                "viewclass": "OneLineListItem",
                "height": dp(56),
                "on_release": lambda x=item: self.select_item(x),
            } for item in self.items
        ]
        
        self.dropdown_menu = MDDropdownMenu(
            caller=self.dropdown_button,
            items=menu_items,
            width_mult=4,
        )
    
    def open_dropdown(self, *args) -> None:
        """Open the dropdown menu when the button is clicked."""
        self.dropdown_menu.open()
    
    def select_item(self, item: str) -> None:
        """
        Set the selected item and update the text field.
        
        Args:
            item: The selected item text
        """
        self.selected_item = item
        self.text_field.text = item
        self.dropdown_menu.dismiss()
        
        # Call the callback function if provided
        if self.on_select:
            self.on_select(item)
    
    def set_items(self, items: List[str]) -> None:
        """
        Update the items in the combobox.
        
        Args:
            items: List of strings to display in the dropdown
        """
        self.items = items
        self._create_dropdown_menu()
    
    def on_items(self, instance, value) -> None:
        """Recreate the dropdown menu when items property changes."""
        self._create_dropdown_menu()
    
    def on_hint_text(self, instance, value) -> None:
        """Update the text field hint when hint_text property changes."""
        self.text_field.hint_text = value


# Demo app to show the combobox in action
class ComboBoxApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Light"
        
        layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(20)
        )
        
        # Create a combobox with some sample items
        combobox = BeautifulComboBox(
            items=["Apple", "Banana", "Cherry", "Orange", "Strawberry"],
            hint_text="Select a fruit",
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5}
        )
        
        layout.add_widget(combobox)
        return layout


if __name__ == "__main__":
    MyCombobox().run()