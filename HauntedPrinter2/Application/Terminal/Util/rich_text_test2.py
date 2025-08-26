from rich import print
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

layout = Layout()
layout.split_column(
    Layout(name="upper"),
    Layout(name="lower")
)

layout["upper"].update(Layout(Panel("nothing yet...",title="history", title_align="center", padding=1)))

layout["lower"].size = 5


grid = Table.grid(expand=True)
grid.add_column(justify="center", ratio=1)
grid.add_row("attack explore sleep eat")
layout["lower"].update(Layout(Panel(grid,title="actions", title_align="center", padding=1)))

print(layout)
