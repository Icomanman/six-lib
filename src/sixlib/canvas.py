from datetime import date
from math import ceil
from typing import Dict, List, Tuple

from manim import Axes, DOWN, UP, Create, Scene, Text, Write

from config import get_colours
from helpers.getters import get_weights


class Canvas(Scene):
    def construct(self) -> None:
        colours: Dict[str, str] = get_colours()
        BACKGROUND = colours["bg"]
        TEXT = colours["text"]
        ACCENT = colours["accent"]
        HIGHLIGHT = colours["highlight"]
        self.camera.background_color = BACKGROUND

        data_src: Dict[str, float] = get_weights()
        if not data_src:
            raise ValueError("Cannot animate an empty time series.")

        observations: List[Tuple[date, float]] = sorted(
            (date.fromisoformat(day), value) for day, value in data_src.items()
        )
        dates: List[str] = [observation_date.isoformat() for observation_date, _ in observations]
        values: List[float] = [value for _, value in observations]
        x_values: List[int] = list(range(len(observations)))

        value_min = min(values)
        value_max = max(values)
        value_range = value_max - value_min
        padding = value_range * 0.1 if value_range else max(abs(value_min) * 0.05, 0.5)
        y_min = value_min - padding
        y_max = value_max + padding
        date_step = max(1, ceil((len(observations) - 1) / 4))

        title: Text = Text("Weight History", color=TEXT).to_edge(UP)
        axes: Axes = Axes(
            x_range=[0, max(1, len(observations) - 1), date_step],
            y_range=[y_min, y_max, (y_max - y_min) / 5],
            x_length=11,
            y_length=5,
        )
        graph = axes.plot_line_graph(
            x_values=x_values,
            y_values=values,
            line_color=ACCENT,
            add_vertex_dots=True,
            vertex_dot_style={"color": HIGHLIGHT},
        )

        date_indices = list(range(0, len(dates), date_step))
        if date_indices[-1] != len(dates) - 1:
            date_indices.append(len(dates) - 1)
        date_labels = [
            Text(dates[index], color=TEXT, font_size=16).next_to(
                axes.c2p(index, y_min), DOWN, buff=0.15
            )
            for index in date_indices
        ]

        self.play(Write(title))
        self.play(Create(axes))
        self.add(*date_labels)
        self.play(Create(graph), run_time=min(8, max(2, len(observations) * 0.1)))
        self.wait(1)
