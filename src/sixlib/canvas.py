
from math import ceil
from typing import Dict, List, Optional

from manim import (
    Axes,
    DEGREES,
    DOWN,
    RIGHT,
    LEFT,
    UP,
    Create,
    Dot,
    Line,
    Mobject,
    MovingCameraScene,
    Text,
    UpdateFromAlphaFunc,
    Write,
    linear,
    smoothstep
)

from config import get_colours
from helpers.getters import daily_moving_average, get_weights, weekly_average


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
        average_src: Dict[str, float] = daily_moving_average(data_src)
        weekly_average_src: Dict[str, float] = weekly_average(data_src)

        dates: List[str] = list(data_src)
        values: List[float] = [data_src[day] for day in dates]
        x_values: List[int] = list(range(len(dates)))
        date_to_x: Dict[str, int] = {
            day: index for index, day in enumerate(dates)
        }

        average_dates: List[str] = list(average_src)
        average_x_values: List[int] = [
            date_to_x[day] for day in average_dates
        ]
        average_values: List[float] = [
            average_src[day] for day in average_dates
        ]

        # line offset
        _offset: int = 1
        average_values_offset: List[float] = [
            average_src[day] - _offset for day in average_dates
        ]

        weekly_dates: List[str] = list(weekly_average_src)
        weekly_x_values: List[int] = [
            date_to_x[day] for day in weekly_dates
        ]
        weekly_values: List[float] = [
            weekly_average_src[day] - _offset for day in weekly_dates
        ]

        value_min = min(values)
        value_max = max(values)
        value_range = value_max - value_min
        padding = value_range * \
            0.1 if value_range else max(abs(value_min) * 0.05, 0.5)
        y_min = value_min - padding
        y_max = value_max + padding
        date_step = max(1, ceil((len(dates) - 1) / 4))
        month_indices = [0]
        month_indices.extend(
            index
            for index in range(1, len(dates))
            if dates[index][:7] != dates[index - 1][:7]
        )
        # *********************************************************

        _new_goal: int = 62
        title: Text = Text("Weight History", color=TEXT).to_edge(UP)
        axes: Axes = Axes(
            x_range=[0, max(1, len(dates) - 1), date_step],
            # y_range=[y_min, y_max, (y_max - y_min) / 5],
            y_range=[_new_goal, 70],
            x_length=26,
            y_length=8,
            x_axis_config={
                "include_ticks": False,
                "include_numbers": False,
                "tip_width": 0.20,
                "tip_height": 0.30,
            },
            y_axis_config={
                "include_numbers": False,
                "tip_width": 0.20,
                "tip_height": 0.30,
            },
        )
        x_axis_label = Text("Date", color=TEXT, font_size=24).next_to(
            axes.x_axis, DOWN, buff=0.75
        )
        y_axis_label = Text("Weight (kg)", color=TEXT, font_size=24).rotate(
            90 * DEGREES
        ).next_to(
            axes.y_axis, LEFT, buff=0.5
        )
        graph = axes.plot_line_graph(
            x_values=x_values,
            y_values=values,
            line_color=ACCENT,
            add_vertex_dots=False,
        )
        line = graph["line_graph"]
        average_line: Optional[Mobject] = None
        if len(average_values) == 1:
            average_line = Dot(
                axes.c2p(average_x_values[0], average_values[0]),
                radius=0.07,
                color=HIGHLIGHT,
            )
        elif average_values:
            average_graph = axes.plot_line_graph(
                x_values=average_x_values,
                y_values=average_values,
                line_color=HIGHLIGHT,
                add_vertex_dots=False,
            )
            average_line = average_graph["line_graph"]

        weekly_graph = axes.plot_line_graph(
            x_values=weekly_x_values,
            y_values=weekly_values,
            line_color=TEXT,
            add_vertex_dots=False,
        )
        weekly_line = weekly_graph["line_graph"]
        average_graph = axes.plot_line_graph(
            x_values=average_x_values,
            y_values=average_values_offset,
            line_color=HIGHLIGHT,
            add_vertex_dots=False,
        )
        average_line_offset = average_graph["line_graph"]

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

        month_ticks = [
            Line(
                axes.c2p(index, _new_goal) + DOWN * 0.08,
                axes.c2p(index, _new_goal) + UP * 0.08,
                color=TEXT,
            )
            for index in month_indices
        ]
        y_tick_values = list(range(_new_goal, 71))
        y_labels = [
            Text(str(value - 60), color=TEXT, font_size=20).next_to(
                axes.c2p(0, value), LEFT, buff=0.35
            )
            for value in y_tick_values
        ]
        date_labels = [
            Text(dates[index][:7], color=TEXT, font_size=20).next_to(
                axes.c2p(index, _new_goal), DOWN, buff=0.35
            )
            for index in month_indices
        ]
        average_label: Optional[Text] = None
        if average_values:
            average_label = Text(
                "7-day moving average", color=HIGHLIGHT, font_size=24
            ).next_to(axes, UP, buff=0.15).align_to(axes, RIGHT)
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
        self.add(x_axis_label, y_axis_label)
        self.add(*month_ticks)
        self.add(*y_labels)
        self.add(*date_labels)
        if average_label is not None:
            self.add(average_label)
        self.add(marker)
        marker_animation = UpdateFromAlphaFunc(marker, follow_data_points)
        plot_animations = [marker_animation, Create(line)]
        if average_line is not None:
            plot_animations.append(Create(average_line))

        # plot_animations.append(Create(weekly_line))
        weekly_label = Text(
            "weekly average", color=TEXT, font_size=24
        ).next_to(axes, UP, buff=-0.25).align_to(axes, RIGHT)
        # self.add(weekly_label)
        # plot_animations.append(Create(average_line_offset))

        plot_animations.append(self.camera.frame.animate.move_to(end_position))
        self.play(
            *plot_animations,
            run_time=min(8, max(2, len(dates) * 0.1)),
            rate_func=linear,
        )
        self.play(
            self.camera.frame.animate.move_to(axes.get_center()).scale(
                full_chart_width / camera_width
            ),
            run_time=3,
            run_func=smoothstep
        )
        self.wait(10)
