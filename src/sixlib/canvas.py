from manim import Axes, Scene, Text
from manim import UP, DOWN, LEFT, Write, Create, FadeIn

from typing import Dict

from config import get_colours
from helpers.getters import get_weights


class Canvas(Scene):
    def construct(self):
       # Per-scene background; set this before adding objects.
        colours: Dict[str, str] = get_colours()
        BACKGROUND = colours["bg"]
        TEXT = colours["text"]
        ACCENT = colours["accent"]
        HIGHLIGHT = colours["highlight"]
        self.camera.background_color = BACKGROUND

        # ****************************************
        data_src: Dict[str, float] = get_weights()

        # ****************************************

        title: Text = Text("Weight History", color=TEXT).to_edge(UP)
        axes: Axes = Axes(
            x_range=[0, 50],
            y_range=[0, 50],
        )

        # play() both shows the objects and animates them into view.
        self.play(Write(title))
        self.play(Create(axes))
        self.wait()
