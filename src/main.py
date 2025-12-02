from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.uix.image import Image


FONT = "04B_03__.TTF"

# ---------- First Screen ----------
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        self.root = FloatLayout()
        self.add_widget(self.root)

        with self.canvas.before:
            self.bg = Rectangle(source='background1.jpg')
        self.bind(size=self.update_bg, pos=self.update_bg)

        self.layout = GridLayout(
            cols=1,
            padding=20,
            spacing=25,
            size_hint=(0.6, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.32}
        )
        self.root.add_widget(self.layout)

        self.error_label = Label(
            text="",
            font_name=FONT,
            font_size=24,
            color=(1, 0, 0, 1)
        )
        self.layout.add_widget(self.error_label)

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

        self.button = Button(
            text="Start Game",
            font_name=FONT,
            font_size=28
        )
        self.button.bind(on_press=self.start_game)
        self.layout.add_widget(self.button)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def start_game(self, instance):
        username = self.username_input.text.strip()

        if len(username) != 3:
            self.error_label.text = "Username must be 3 letters!"
            return

        if not username.isalpha():
            self.error_label.text = "Letters only!"
            return

        self.error_label.text = ""
        self.manager.username = username.upper()
        self.manager.current = 'game'


# ---------- Second Screen (Difficulty Selection) ----------
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

        self.root = FloatLayout()
        self.add_widget(self.root)

        with self.canvas.before:
            self.bg = Rectangle(source='basic_cloud.jpg')
        self.bind(size=self.update_bg, pos=self.update_bg)

        self.label = Label(
            text="",
            font_name=FONT,
            font_size=48,
            color=(0, 0, 0, .8),
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )
        self.root.add_widget(self.label)

        self.button_layout = GridLayout(
            cols=1,
            spacing=20,
            size_hint=(0.3, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )
        self.root.add_widget(self.button_layout)

        for difficulty in ['EASY', 'MEDIUM', 'HARD']:
            btn = Button(
                text=difficulty,
                font_name=FONT,
                font_size=28,
                size_hint_y=None,
                height=60
            )
            btn.bind(on_press=self.select_difficulty)
            self.button_layout.add_widget(btn)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def on_enter(self):
        self.label.text = f"SELECT GAMEMODE, {self.manager.username}"

    def select_difficulty(self, instance):
        difficulty = instance.text
        self.manager.difficulty = difficulty
        self.manager.current = 'playscreen'   # Go to the new screen


# ---------- Third Screen (Displays Selected Difficulty) ----------
class PlayScreen(Screen):
    def __init__(self, **kwargs):
        super(PlayScreen, self).__init__(**kwargs)

        self.root = FloatLayout()
        self.add_widget(self.root)

        with self.canvas.before:
            self.bg = Rectangle(source='basic_cloud.jpg')
        self.bind(size=self.update_bg, pos=self.update_bg)

        self.target_image = Image(
            source='target.png',
            size_hint=(0.9, 0.9),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.root.add_widget(self.target_image)

        self.label = Label(
            text="",
            font_name=FONT,
            font_size=30,
            color=(0, 0, 0, .9),
            pos_hint={'center_x': 0.5, 'center_y': 0.15}
        )
        self.root.add_widget(self.label)

        self.score_label = Label(
            text="Score: 0",
            font_name = FONT,
            font_size = 32,
            bold=True,
            color=(0,0,0,.9),
            pos_hint={'right': 1.35, 'top': 1.35}
        )
        self.root.add_widget(self.score_label)
        self.score = 0   #initial score

        self.streak_label = Label(
            text="Score: 0",
            font_name = FONT,
            font_size = 25,
            bold=True,
            color=(1,0,0,.9),
            pos_hint={'right': 1.35, 'top': 1.3}
        )
        self.root.add_widget(self.streak_label)
        self.streak = 1   #initial streak


    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def on_enter(self):
        self.label.text = f"DIFFICULTY: {self.manager.difficulty}"
        self.update_score(self.score)
        self.update_streak(self.streak)


    def update_score(self, new_score):
        self.score = new_score
        self.score_label.text = f"Score: {self.score}"

    def update_streak(self, new_streak):
        self.streak = new_streak
        self.streak_label.text = f"Streak x{self.streak}"

# ---------- Screen Manager ----------
class GameApp(App):
    def build(self):
        sm = ScreenManager(transition=CardTransition())
        sm.username = ""
        sm.difficulty = ""

        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(PlayScreen(name='playscreen'))

        return sm


if __name__ == "__main__":
    GameApp().run()

