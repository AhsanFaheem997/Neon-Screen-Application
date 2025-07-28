from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle
import random

class NeonClubApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)

        self.anchor = AnchorLayout()
        self.layout = BoxLayout(orientation='vertical', padding=50, spacing=30, size_hint=(None, None))
        self.layout.size = (300, 300)

        self.running = False
        self.phase = 0
        self.direction = 1

        # Simulated gradient background using canvas
        with self.anchor.canvas.before:
            self.bg_color_top = Color(1, 0, 1, 1)
            self.bg_rect_top = Rectangle(size=Window.size, pos=self.anchor.pos)
            self.bg_color_bottom = Color(0, 1, 1, 1)
            self.bg_rect_bottom = Rectangle(size=Window.size, pos=self.anchor.pos)

        Window.bind(on_resize=self.update_gradient)

        # Start Button
        self.start_button = Button(
            text='Start',
            font_size=24,
            size_hint=(None, None),
            size=(250, 100),
            background_normal='',
            background_color=get_color_from_hex('#00ffff'),
            color=(0, 0, 0, 1)
        )
        self.start_button.bind(on_press=self.start_party)
        self.layout.add_widget(self.start_button)

        # Exit Button
        self.exit_button = Button(
            text='Exit',
            font_size=24,
            size_hint=(None, None),
            size=(250, 100),
            background_normal='',
            background_color=get_color_from_hex('#00ffff'),
            color=(0, 0, 0, 1)
        )
        self.exit_button.bind(on_press=self.stop_party)
        self.layout.add_widget(self.exit_button)

        self.anchor.add_widget(self.layout)
        return self.anchor

    def update_gradient(self, *args):
        self.bg_rect_top.size = Window.size
        self.bg_rect_bottom.size = Window.size

    def random_color(self):
        return (
            random.uniform(0.2, 1.0),
            random.uniform(0.2, 1.0),
            random.uniform(0.2, 1.0),
            1
        )

    def start_party(self, *args):
        if not self.running:
            self.running = True
            self.target_color1 = self.random_color()
            self.target_color2 = self.random_color()
            self.animate_background()
            self.glow_buttons()

    def stop_party(self, *args):
        self.running = False
        Window.clearcolor = (0, 0, 0, 1)
        self.bg_color_top.rgba = (0, 0, 0, 1)
        self.bg_color_bottom.rgba = (0, 0, 0, 1)
        self.start_button.background_color = get_color_from_hex('#00ffff')
        self.start_button.color = (0, 0, 0, 1)
        self.exit_button.background_color = get_color_from_hex('#00ffff')
        self.exit_button.color = (0, 0, 0, 1)

    def animate_background(self, *args):
        if not self.running:
            return

        def interpolate(c1, c2, t):
            return tuple(c1[i] + (c2[i] - c1[i]) * t for i in range(4))

        t = 0.05  # Smoothing factor
        new_color1 = interpolate(self.bg_color_top.rgba, self.target_color1, t)
        new_color2 = interpolate(self.bg_color_bottom.rgba, self.target_color2, t)

        self.bg_color_top.rgba = new_color1
        self.bg_color_bottom.rgba = new_color2

        if all(abs(new_color1[i] - self.target_color1[i]) < 0.05 for i in range(3)):
            self.target_color1 = self.random_color()
        if all(abs(new_color2[i] - self.target_color2[i]) < 0.05 for i in range(3)):
            self.target_color2 = self.random_color()

        Clock.schedule_once(self.animate_background, 0.05)

    def glow_buttons(self, *args):
        if not self.running:
            return

        factor = self.phase / 100.0
        glow_color = (0, 1, factor, 1)
        text_color = (factor, factor, factor, 1)

        self.start_button.background_color = glow_color
        self.exit_button.background_color = glow_color
        self.start_button.color = text_color
        self.exit_button.color = text_color

        self.phase += self.direction * 2
        if self.phase >= 100:
            self.phase = 100
            self.direction = -1
        elif self.phase <= 0:
            self.phase = 0
            self.direction = 1

        Clock.schedule_once(self.glow_buttons, 0.05)

if __name__ == '__main__':
    NeonClubApp().run()
