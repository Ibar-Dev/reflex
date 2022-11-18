"""Create a list of components from an iterable."""
from __future__ import annotations

from typing import Any, List, Protocol, runtime_checkable

from pynecone.components.component import Component
from pynecone.components.tags import IterTag, Tag
from pynecone.var import BaseVar, Var


@runtime_checkable
class RenderFn(Protocol):
    """A function that renders a component."""

    def __call__(self, *args, **kwargs) -> Component:
        """Render a component.

        Args:
            *args: The positional arguments.
            **kwargs: The keyword arguments.

        Returns: # noqa: DAR202
            The rendered component.
        """
        ...


class Foreach(Component):
    """Display a foreach."""

    # The iterable to create components from.
    iterable: Var[List]

    # A function from the render args to the component.
    render_fn: RenderFn

    @classmethod
    def create(cls, iterable: Var[List], render_fn: RenderFn, **props) -> Foreach:
        """Create a foreach component.

        Args:
            iterable: The iterable to create components from.
            render_fn: A function from the render args to the component.
            **props: The attributes to pass to each child component.

        Returns:
            The foreach component.
        """
        try:
            type_ = iterable.type_.__args__[0]
        except:
            type_ = Any
        arg = BaseVar(name="_", type_=type_, is_local=True)
        return cls(
            iterable=iterable,
            render_fn=render_fn,
            children=[IterTag.render_component(render_fn, arg=arg)],
            **props,
        )

    def _render(self) -> Tag:
        return IterTag(iterable=self.iterable, render_fn=self.render_fn)
