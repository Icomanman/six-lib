from manim import UP, DOWN, LEFT, Circle, Scene, Text, Write, Create, FadeIn
from typing import Dict

from sixlib.config import get_colours


class Canvas(Scene):
    def construct(self):
       # Per-scene background; set this before adding objects.
        colours: Dict[str, str] = get_colours()
        BACKGROUND = colours["bg"]
        TEXT = colours["text"]
        ACCENT = colours["accent"]
        HIGHLIGHT = colours["highlight"]

        self.camera.background_color = BACKGROUND

        title = Text("A first scene", color=TEXT).to_edge(UP)
        circle = Circle(color=ACCENT, fill_color=ACCENT, fill_opacity=0.2)
        label = Text("An object", color=TEXT).next_to(circle, DOWN)

        # play() both shows the objects and animates them into view.
        self.play(Write(title))
        self.play(Create(circle), FadeIn(label))
        self.play(
            circle.animate.shift(LEFT * 2).set_color(HIGHLIGHT),
            label.animate.next_to(circle, DOWN),
            run_time=1.5,
        )
        self.wait()
