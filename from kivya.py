from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window

Window.clearcolor = (0.9, 0.95, 1, 1)  

class CGPACalculatorApp(App):
    def build(self):
        Window.bind(on_key_down=self.on_key_down)  

        self.grade_inputs = []
        self.credit_inputs = []

        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20 )

        self.subject_label = Label(text="Enter number of subjects:", font_size=50,color=(0, 0, 0, 1))
        self.subject_input = TextInput(multiline=False, font_size=28, size_hint_y=None, height=60)
        self.next_button = Button(text="Next", font_size=28, size_hint_y=None, height=60, background_color=(0.6, 0.8, 1, 1))
        self.next_button.bind(on_press=self.generate_subject_fields)

        self.main_layout.add_widget(self.subject_label)
        self.main_layout.add_widget(self.subject_input)
        self.main_layout.add_widget(self.next_button)

        self.result_label = Label(text="", font_size=32, color=(0, 0, 0, 1))
        self.main_layout.add_widget(self.result_label)

        return self.main_layout

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if key == 13:  # Enter key
            if hasattr(self, 'calculate_button'):
                self.calculate_cgpa(None)
        elif key == 275:  # Right arrow key
            self.generate_subject_fields(None)

    def generate_subject_fields(self, instance):
        try:
            num = int(self.subject_input.text.strip())
            if num <= 0:
                self.show_popup("Please enter a number greater than 0.")
                return
        except:
            self.show_popup("Invalid number entered.")
            return

        # Clear previous inputs
        if hasattr(self, 'inputs_layout'):
            self.main_layout.remove_widget(self.inputs_layout)
        if hasattr(self, 'calculate_button'):
            self.main_layout.remove_widget(self.calculate_button)

        self.grade_inputs.clear()
        self.credit_inputs.clear()

        self.inputs_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.inputs_layout.bind(minimum_height=self.inputs_layout.setter('height'))

        for i in range(num):
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
            row.add_widget(Label(text=f"Subject {i+1}:", font_size=28,color=(0, 0, 0, 1), size_hint_x=0.3))
            grade_input = TextInput(hint_text="Grade (H/S/A/B/C/F/RA)", multiline=False, font_size=22, size_hint_x=0.35)
            credit_input = TextInput(hint_text="Credits", multiline=False, font_size=22, size_hint_x=0.25)

            row.add_widget(grade_input)
            row.add_widget(credit_input)

            self.grade_inputs.append(grade_input)
            self.credit_inputs.append(credit_input)
            self.inputs_layout.add_widget(row)

        self.main_layout.add_widget(self.inputs_layout)

        self.calculate_button = Button(text="Calculate CGPA", font_size=28, size_hint_y=None, height=60, background_color=(0.4, 0.7, 1, 1))
        self.calculate_button.bind(on_press=self.calculate_cgpa)
        self.main_layout.add_widget(self.calculate_button)

    def calculate_cgpa(self, instance):
        grade_map = {
            'H': 10,
            'S': 9,
            'A': 8,
            'B': 7,
            'C': 6,
            'F': 0
        }

        total_points = 0
        total_credits = 0

        for i in range(len(self.grade_inputs)):
            grade = self.grade_inputs[i].text.strip().upper()
            credit_text = self.credit_inputs[i].text.strip()

            if grade == "RA":
                continue  # Skip RA

            if grade not in grade_map:
                self.show_popup(f"Invalid grade in Subject {i+1}. Use H, S, A, B, C, F, or RA.")
                return

            try:
                credit = float(credit_text)
                if credit <= 0:
                    self.show_popup(f"Credit must be greater than 0 for Subject {i+1}.")
                    return
            except:
                self.show_popup(f"Invalid credit in Subject {i+1}.")
                return

            gp = grade_map[grade]
            total_points += gp * credit
            total_credits += credit

        if total_credits == 0:
            self.result_label.text = "CGPA: N/A (No valid subjects)"
        else:
            cgpa = round(total_points / total_credits, 2)
            self.result_label.text = f"CGPA: {cgpa}"
        if cgpa <= 5.1 :
        
             Window.clearcolor = (1, 0.5, 0.5, 1)  
        else:
             Window.clearcolor = (0.88, 1, 0.88, 1)  
             return

    def show_popup(self, message):
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        content.add_widget(Label(text=message, font_size=22))
        close_button = Button(text="OK", size_hint_y=None, height=50)
        content.add_widget(close_button)

        popup = Popup(title="Error", content=content, size_hint=(None, None), size=(500, 250), auto_dismiss=False)
        close_button.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    CGPACalculatorApp().run()
