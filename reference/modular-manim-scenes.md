# Modular Manim Scenes

Manim can load scene classes from different Python files, but it does not automatically combine separate `Scene` classes into one continuous animation. The right structure depends on what you want to reuse:

| Goal | Use |
| --- | --- |
| Reuse a visual object | A function that builds and returns a `Mobject` or `VGroup` |
| Reuse an animation | A function that returns an `Animation` |
| Reuse a section of a story | A helper function or method that plays that section on the current scene |
| Render independent clips | Separate `Scene` classes, then join their video files with an editor |

## A small package layout

```text
src/
└── sixlib/
    ├── __init__.py
    ├── components.py
    ├── animations.py
    ├── sections.py
    └── scenes/
        ├── __init__.py
        └── introduction.py
```

Keep reusable visual components and animation helpers separate from the `Scene` that decides their order. Use package-qualified imports such as `from sixlib.components import labeled_circle`. Manim loads the scene file directly, so package imports need `src` on Python's import path. From the repository root, the project's `render.sh` does this with `PYTHONPATH=src`.

## Reuse a visual component

`src/sixlib/components.py`:

```python
from manim import Circle, DOWN, Text, VGroup


def labeled_circle(label: str) -> VGroup:
    circle = Circle(color="#4CC9F0", fill_opacity=0.2)
    caption = Text(label, font_size=24).next_to(circle, DOWN)
    return VGroup(circle, caption)
```

The function builds an object; it does not decide when or how that object appears. The scene controls positioning and animation:

```python
from manim import FadeIn, Scene, UP, Write, Text
from sixlib.components import labeled_circle


class Introduction(Scene):
    def construct(self):
        title = Text("A modular scene").to_edge(UP)
        badge = labeled_circle("Reusable component")

        self.play(Write(title))
        self.play(FadeIn(badge))
        self.wait()
```

## Reuse an animation

`src/sixlib/animations.py`:

```python
from manim import Animation, FadeIn, LEFT, Mobject


def enter_from_left(mobject: Mobject) -> Animation:
    return FadeIn(mobject, shift=LEFT)
```

Use the helper in any scene:

```python
from manim import Scene
from sixlib.animations import enter_from_left
from sixlib.components import labeled_circle


class Introduction(Scene):
    def construct(self):
        badge = labeled_circle("Reusable component")
        self.play(enter_from_left(badge))
```

## Reuse a whole story section

When a sequence of actions belongs together, extract a function that receives the current scene. Return any mobjects the next section needs to manipulate:

```python
from manim import Scene, Text, Write


def show_heading(scene: Scene, wording: str) -> Text:
    heading = Text(wording)
    scene.play(Write(heading))
    return heading
```

```python
from manim import Scene
from sixlib.sections import show_heading


class Lesson(Scene):
    def construct(self):
        heading = show_heading(self, "Part one")
        self.play(heading.animate.to_edge(UP))
```

Prefer passing scene state explicitly over hidden module-level state. Avoid splitting every line into a helper; extract parts that are meaningfully reusable or make a scene easier to follow.

## Separate scenes versus one continuous video

Each `Scene` is rendered independently. For example:

```bash
PYTHONPATH=src manim render -pql src/sixlib/scenes/introduction.py Introduction
```

That produces a clip for `Introduction`; another scene class produces another clip. Passing multiple scene names to Manim renders multiple scenes, but does not turn them into one continuous scene. To maintain shared objects, camera state, and transitions across a story, use one `Scene` and compose its sequence from components and section helpers. If the clips should remain independent, render them separately and join the resulting videos with a video editor, keeping their resolution and frame rate consistent.

## Common import pitfall

Relative imports such as `from .components import labeled_circle` require Python to import the module in package context. Manim's file-path scene loader may not provide that context. Prefer absolute package imports (`from sixlib.components import labeled_circle`) and render from the repository root with `PYTHONPATH=src` (as in `render.sh`).
