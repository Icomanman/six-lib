# Manim Cheat Sheet

Quick reference for **Manim Community Edition** (the project environment currently uses v0.22.1). Manim scenes are Python classes: create mobjects, add them to a scene, and animate them with `play`.

## Scene skeleton

```python
from manim import *


class FirstScene(Scene):
    def construct(self):
        title = Text("Hello, Manim").to_edge(UP)
        circle = Circle(color=BLUE, fill_opacity=0.25)

        self.play(Write(title), Create(circle))
        self.play(circle.animate.shift(RIGHT * 2))
        self.wait()
```

`construct()` is where a scene is assembled. `Scene` is the standard 2D scene; use `ThreeDScene` for 3D camera controls.

## Render from the terminal

```bash
manim render -pql scene.py FirstScene
```

| Option | Meaning |
| --- | --- |
| `-p` | Preview the rendered output |
| `-q l` / `-q m` / `-q h` / `-q p` / `-q k` | Low / medium / high / 1440p / 4K quality |
| `-s` | Save only the final frame as a PNG |
| `-a` | Render every scene in the file |
| `--format=gif` | Select an output format (`mp4`, `gif`, `webm`, `mov`, `png`, or `png-sequence`) |
| `--renderer=opengl` | Use the OpenGL renderer instead of the default Cairo renderer |

Omit `-p` to render without opening the result. Add `--help` to see all options.

## Common mobjects

```python
circle = Circle(radius=1, color=BLUE)
square = Square(side_length=2, color=GREEN)
rectangle = Rectangle(width=3, height=1.5)
line = Line(LEFT, RIGHT)
arrow = Arrow(ORIGIN, UP * 2)
dot = Dot(ORIGIN)
label = Text("A label")
formula = MathTex(r"e^{i\pi} + 1 = 0")
```

Useful shapes include `Polygon`, `Ellipse`, `Arc`, `Brace`, `NumberLine`, `Axes`, and `NumberPlane`. Most mobjects accept styling arguments such as `color`, `stroke_width`, `fill_color`, and `fill_opacity`.

## Positioning and grouping

The scene centre is `ORIGIN` (`[0, 0, 0]`). Directions are `UP`, `DOWN`, `LEFT`, `RIGHT`, and diagonals such as `UL` and `DR`.

```python
shape.move_to(ORIGIN)
shape.shift(2 * RIGHT + UP)
shape.scale(0.75)
shape.rotate(PI / 4)

label.next_to(shape, RIGHT, buff=0.2)
shape.to_edge(LEFT)
label.to_corner(UR)

items = VGroup(Circle(), Square(), Triangle())
items.arrange(RIGHT, buff=0.4)
items.arrange(DOWN, aligned_edge=LEFT)
```

`move_to`, `shift`, `scale`, and `rotate` change an object immediately. Use `.animate` with `self.play` to animate a change.

## Animations

```python
self.play(Create(circle))                 # Draw a shape
self.play(Write(text))                     # Reveal text
self.play(FadeIn(dot), run_time=0.5)
self.play(FadeOut(dot))
self.play(circle.animate.set_color(RED))
self.play(circle.animate.move_to(LEFT))
self.play(Transform(circle, square))       # Morph the source into the target
self.play(ReplacementTransform(circle, square))
self.play(Indicate(text), Circumscribe(square))
self.wait(1)
```

Group or sequence animations:

```python
self.play(AnimationGroup(
    Create(circle),
    Write(text),
    lag_ratio=0.3,
))

self.play(LaggedStart(
    *[FadeIn(mob) for mob in items],
    lag_ratio=0.15,
))
```

Common timing controls: `run_time=2`, `rate_func=linear`, `rate_func=smooth`, and `rate_func=there_and_back`.

## Text and equations

```python
title = Text("A title", font_size=48, color=YELLOW)
equation = MathTex(r"\int_0^1 x^2\,dx = \frac{1}{3}")

equation.scale(0.9)
equation.set_color_by_tex(r"\frac{1}{3}", GREEN)
self.play(Write(equation))
```

Use `Text` for ordinary text and `MathTex` for LaTeX mathematics. LaTeX must be installed and available to Manim. For multi-part formulas, pass separate strings to `MathTex` to make pieces easier to reference:

```python
equation = MathTex("a^2", "+", "b^2", "=", "c^2")
self.play(Write(equation[0]))
```

## Axes and graphs

```python
axes = Axes(
    x_range=[-3, 3, 1],
    y_range=[-1, 5, 1],
    axis_config={"include_numbers": True},
)
curve = axes.plot(lambda x: x**2, x_range=[-2, 2], color=BLUE)
point = Dot(axes.c2p(1, 1), color=YELLOW)

self.play(Create(axes), Create(curve), FadeIn(point))
```

Use `axes.c2p(x, y)` to convert graph coordinates to scene coordinates and `axes.p2c(point)` for the reverse conversion.

## Dynamic values and updaters

```python
tracker = ValueTracker(0)
marker = Dot()
marker.add_updater(
    lambda mob: mob.move_to(axes.c2p(tracker.get_value(), tracker.get_value() ** 2))
)

self.add(axes, marker)
self.play(tracker.animate.set_value(2), run_time=2)
marker.clear_updaters()
```

Use `add_updater` when a mobject should be recalculated as the scene changes. `always_redraw(lambda: ...)` is handy when the whole mobject needs to be rebuilt each frame.

## Styling and useful constants

Common colours: `WHITE`, `BLACK`, `RED`, `GREEN`, `BLUE`, `YELLOW`, `ORANGE`, `PURPLE`, and `PINK`.

```python
shape.set_color(TEAL)
shape.set_fill(ORANGE, opacity=0.5)
shape.set_stroke(WHITE, width=3)
```

Other useful constants: `PI`, `TAU` (one full turn), `DEGREES`, `ORIGIN`, and `SMALL_BUFF`, `MED_SMALL_BUFF`, `MED_LARGE_BUFF`, `LARGE_BUFF`.

## Quick troubleshooting

- **A scene is missing from the render:** pass its class name after the file name, or use `-a` to render all scenes.
- **Text or equations fail to compile:** check that a LaTeX installation is available; use `Text` when mathematical typesetting is not needed.
- **A mobject appears in the wrong place:** remember that scene positions are 3D vectors and use `axes.c2p(...)` for graph coordinates.
- **An updater keeps running:** call `clear_updaters()` when it is no longer needed.
- **Rendering is slow:** iterate with `-ql`; switch to higher quality for the final render.

For complete API details, see the [Manim Community documentation](https://docs.manim.community/en/stable/).
