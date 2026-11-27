"""Realtime Counter — reactive state with WebSocket-driven DOM updates.

Run: python main.py  or  grumo dev
"""

from grumo import App, page, state
from grumo.core import event
from grumo.ui import Button, Div, Heading, Text

app = App()

count = state(0)


@page("/")
def counter():
    return Div(
        Heading("Realtime Counter", level=1),
        Text(f"Count: {count.get()}", id="count-display"),
        Button("+1", onclick="vd.event('increment', 'count-display', 1)"),
        Button("-1", onclick="vd.event('decrement', 'count-display', 1)"),
        Button("Reset", onclick="vd.event('reset', 'count-display')"),
    )


@event
async def increment(element_id, value):
    count.set(count.get() + value)


@event
async def decrement(element_id, value):
    count.set(count.get() - value)


@event
async def reset(element_id, value):
    count.set(0)


if __name__ == "__main__":
    app.run()
