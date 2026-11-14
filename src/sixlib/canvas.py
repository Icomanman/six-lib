
from math import ceil
from typing import Dict, List

from manim import (
    Axes,
    DOWN,
    UP,
    Create,
    Dot,
    Mobject,
    MovingCameraScene,
    Text,
    UpdateFromAlphaFunc,
    Write,
    linear,
    smoothstep
)

from config import get_colours
from helpers.getters import get_weights


class Canvas(MovingCameraScene):
    def construct(self) -> None:
        colours: Dict[str, str] = get_colours()
        BACKGROUND = colours["bg"]
        TEXT = colours["text"]
        ACCENT = colours["accent"]
        HIGHLIGHT = colours["highlight"]
        self.camera.background_color = BACKGROUND

        # *********************************************************
        data_src: Dict[str, float] = get_weights(sort_by_date=True)
        if not data_src:
            raise ValueError("Cannot animate an empty time series.")

        dates: List[str] = list(data_src)
        values: List[float] = [data_src[day] for day in dates]
        x_values: List[int] = list(range(len(dates)))

        value_min = min(values)
        value_max = max(values)
        value_range = value_max - value_min
        padding = value_range * \
            0.1 if value_range else max(abs(value_min) * 0.05, 0.5)
        y_min = value_min - padding
        y_max = value_max + padding
        date_step = max(1, ceil((len(dates) - 1) / 4))
        # *********************************************************

        title: Text = Text("Weight History", color=TEXT).to_edge(UP)
        axes: Axes = Axes(
            x_range=[0, max(1, len(dates) - 1), date_step],
            y_range=[y_min, y_max, (y_max - y_min) / 5],
            x_length=26,
            y_length=5,
        )
        graph = axes.plot_line_graph(
            x_values=x_values,
            y_values=values,
            line_color=ACCENT,
            add_vertex_dots=False,
        )
        line = graph["line_graph"]
        data_points = [
            axes.c2p(x_value, value) for x_value, value in zip(x_values, values)
        ]
        marker = Dot(data_points[0], radius=0.10, color=HIGHLIGHT)

        def follow_data_points(mobject: Mobject, alpha: float) -> None:
            segment_count = len(data_points) - 1
            if segment_count == 0:
                return

            segment_progress = alpha * segment_count
            segment_index = min(int(segment_progress), segment_count - 1)
            segment_alpha = segment_progress - segment_index
            start = data_points[segment_index]
            end = data_points[segment_index + 1]
            mobject.move_to(start + segment_alpha * (end - start))

        date_indices = list(range(0, len(dates), date_step))
        if date_indices[-1] != len(dates) - 1:
            date_indices.append(len(dates) - 1)
        date_labels = [
            Text(dates[index], color=TEXT, font_size=16).next_to(
                axes.c2p(index, y_min), DOWN, buff=0.15
            )
            for index in date_indices
        ]
        camera_y = (y_min + y_max) / 2
        start_position = axes.c2p(x_values[0], camera_y)
        end_position = axes.c2p(x_values[-1], camera_y)
        camera_width = 12
        full_chart_width = axes.width + 2

        self.play(Write(title))
        self.play(
            self.camera.frame.animate.move_to(start_position).scale(
                camera_width / self.camera.frame.width
            ),
            run_time=1.5,
            # rate_func=smoothstep
        )
        self.play(Create(axes))
        self.add(*date_labels)
        self.add(marker)
        marker_animation = UpdateFromAlphaFunc(marker, follow_data_points)
        self.play(
            marker_animation,
            Create(line),
            self.camera.frame.animate.move_to(end_position),
            run_time=min(8, max(2, len(dates) * 0.1)),
            rate_func=linear,
        )
        self.play(
            self.camera.frame.animate.move_to(axes.get_center()).scale(
                full_chart_width / camera_width
            ),
            run_time=5,
            run_func=smoothstep
        )
        self.wait(5)
