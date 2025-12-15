# Import the main Kivy App class (base of every Kivy application)
from kivy.app import App

# Import screen management tools to switch between different screens
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition

# Import layout classes for positioning widgets
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout

# Import basic UI widgets
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

# Used for drawing graphics (background images)
from kivy.graphics import Rectangle

# Widget used to display images
from kivy.uix.image import Image

# Clock is used for scheduling timed events (like countdowns)
from kivy.clock import Clock

# Font used throughout the application
FONT = "04B_03__.TTF"


# ---------- First Screen ----------
# This screen handles user login / username entry
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Root layout that allows absolute positioning
        self.root = FloatLayout()
        self.add_widget(self.root)

        # Draw a background image behind all widgets
        with self.canvas.before:
            self.bg = Rectangle(source='background1.jpg')

        # Update background size/position whenever screen changes
        self.bind(size=self.update_bg, pos=self.update_bg)

        # Layout that stacks widgets vertically
        self.layout = GridLayout(
            cols=1,
            padding=20,
            spacing=25,
            size_hint=(0.6, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.root.add_widget(self.layout)

        # Label used to display validation errors
        self.error_label = Label(
            text="",
            font_name=FONT,
            font_size=24,
            color=(1, 0, 0, 1)  # red text
        )
        self.layout.add_widget(self.error_label)

        # Text field where the user enters a username
        self.username_input = TextInput(
            multiline=False,
            font_name=FONT,
            font_size=32,
            halign='center',
            foreground_color=(0, 0, 1, 1),
            background_normal='',
            background_active='',
            background_color=(0, 0, 0, 0),
            cursor_color=(0, 0, 1, 1),
            size_hint_y=None,
            height=60
        )
        self.layout.add_widget(self.username_input)

        # Button that attempts to start the game
        self.button = Button(
            text="Start Game",
            font_name=FONT,
            font_size=28
        )
        # When pressed, call start_game()
        self.button.bind(on_press=self.start_game)
        self.layout.add_widget(self.button)

    # Keeps the background image stretched to the screen size
    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    # Validates the username and transitions to the next screen
    def start_game(self, instance):
        username = self.username_input.text.strip()

        # Username must be exactly 3 characters
        if len(username) != 3:
            self.error_label.text = "Username must be 3 letters!"
            return

        # Username must contain only letters
        if not username.isalpha():
            self.error_label.text = "Letters only!"
            return

        # Clear errors and save username globally in ScreenManager
        self.error_label.text = ""
        self.manager.username = username.upper()

        # Switch to the difficulty selection screen
        self.manager.current = 'game'


# ---------- Second Screen (Difficulty Selection) ----------
# Allows the user to choose a difficulty level
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

        self.root = FloatLayout()
        self.add_widget(self.root)

        # Background image for the screen
        with self.canvas.before:
            self.bg = Rectangle(source='basic_cloud.jpg')
        self.bind(size=self.update_bg, pos=self.update_bg)

        # Label that greets the user
        self.label = Label(
            text="",
            font_name=FONT,
            font_size=48,
            color=(0, 0, 0, .8),
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )
        self.root.add_widget(self.label)

        # Layout holding difficulty buttons
        self.button_layout = GridLayout(
            cols=1,
            spacing=20,
            size_hint=(0.3, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.root.add_widget(self.button_layout)

        # Create buttons for each difficulty option
        for difficulty in ['EASY', 'MEDIUM', 'HARD']:
            btn = Button(
                text=difficulty,
                font_name=FONT,
                font_size=28,
                size_hint_y=None,
                height=60
            )
            # When pressed, call select_difficulty()
            btn.bind(on_press=self.select_difficulty)
            self.button_layout.add_widget(btn)

    # Resize background when screen changes
    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    # Called automatically when this screen is entered
    def on_enter(self):
        # Display the username saved from the login screen
        self.label.text = f"SELECT GAMEMODE, {self.manager.username}"

    # Saves the chosen difficulty and moves to gameplay screen
    def select_difficulty(self, instance):
        difficulty = instance.text
        self.manager.difficulty = difficulty
        self.manager.current = 'playscreen'


# ---------- Third Screen (Gameplay Screen) ----------
# Displays the game, countdown timer, score, and target
class PlayScreen(Screen):
    def __init__(self, **kwargs):
        super(PlayScreen, self).__init__(**kwargs)

        self.root = FloatLayout()
        self.add_widget(self.root)

        # Background image
        with self.canvas.before:
            self.bg = Rectangle(source='basic_cloud.jpg')
        self.bind(size=self.update_bg, pos=self.update_bg)

        # Initial countdown value
        self.time_left = 30

        # Countdown display
        self.countdown_label = Label(
            text=f"Time: {self.time_left}",
            font_name=FONT,
            font_size=32,
            color=(0, 0, 0, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}
        )
        self.root.add_widget(self.countdown_label)

        # Target image displayed during the game
        self.target_image = Image(
            source='target.png',
            size_hint=(0.9, 0.9),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.root.add_widget(self.target_image)

        # Displays selected difficulty
        self.label = Label(
            text="",
            font_name=FONT,
            font_size=30,
            color=(0, 0, 0, .9),
            pos_hint={'center_x': 0.5, 'center_y': 0.15}
        )
        self.root.add_widget(self.label)

        # Score label
        self.score_label = Label(
            text="Score: 0",
            font_name=FONT,
            font_size=32,
            bold=True,
            color=(0, 0, 0, .9),
            pos_hint={'right': 1.35, 'top': 1.35}
        )
        self.root.add_widget(self.score_label)
        self.score = 0  # initial score

        # Streak multiplier label
        self.streak_label = Label(
            text="Score: 0",
            font_name=FONT,
            font_size=25,
            bold=True,
            color=(1, 0, 0, .9),
            pos_hint={'right': 1.35, 'top': 1.3}
        )
        self.root.add_widget(self.streak_label)
        self.streak = 1  # initial streak

    # Resize background to screen
    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    # Runs when this screen becomes active
    def on_enter(self):
        self.label.text = f"DIFFICULTY: {self.manager.difficulty}"
        self.update_score(self.score)
        self.update_streak(self.streak)
        self.time_left = 30
        self.update_countdown(0)

        # Start a 1-second repeating timer
        self.timer_event = Clock.schedule_interval(self.update_countdown, 1)

    # Called every second by the Clock
    def update_countdown(self, dt):
        self.time_left -= 1
        self.countdown_label.text = f"Time: {self.time_left}"

        # End the game when time reaches zero
        if self.time_left <= 0:
            Clock.unschedule(self.timer_event)
            self.countdown_label.text = "Time: 0"
            self.game_over()

    # Handles end-of-game behavior
    def game_over(self):
        Clock.unschedule(self.timer_event)
        self.manager.current = "end_screen"

    # Updates the score display
    def update_score(self, new_score):
        self.score = new_score
        self.score_label.text = f"Score: {self.score}"

    # Updates the streak display
    def update_streak(self, new_streak):
        self.streak = new_streak
        self.streak_label.text = f"Streak x{self.streak}"


# ---------- End Screen ----------
# Simple screen shown when the game ends
class EndScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        layout.add_widget(Label(
            text="Game Over!",
            font_size=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        ))
        self.add_widget(layout)


# ---------- Screen Manager ----------
# Main application class
class GameApp(App):
    def build(self):
        # ScreenManager controls transitions between screens
        sm = ScreenManager(transition=CardTransition())

        # Shared data accessible by all screens
        sm.username = ""
        sm.difficulty = ""

        # Register screens
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(PlayScreen(name='playscreen'))
        sm.add_widget(EndScreen(name="end_screen"))

        return sm


# Entry point of the application
if __name__ == "__main__":
    GameApp().run()
