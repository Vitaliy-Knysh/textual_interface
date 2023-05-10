import asyncio
import textual.widgets
from textual.app import App, ComposeResult, RenderableType
from textual.widgets import Static, Label, Input, Button, DataTable, TextLog, ProgressBar
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.scroll_view import ScrollView
from textual import work
from textual.widget import Widget
from textual.geometry import Size
from textual.reactive import reactive
from textual import events
from datetime import datetime
import random
import time
from rich.text import Text



ROWS = [
    ('preburn', '0:00:00', '(1 выполнено)'),
    ('burn', '0:00:00', '(2 выполнено)'),
    ('inventory', '0:00:00', '(2 выполнено)'),
    ('functional', '0:00:01', '(3 выполнено)'),
    ('nework', '0:00:01', '(1 выполнено)'),
    ('memory_stress', '0:00:00', '(0 выполнено)'),
    ('gpu_stress', '0:00:00', '(0 выполнено)'),
    ('fio_stress', '0:00:00', '(0 выполнено)'),
]

current_stage = 'preburn'


INPUT_LOG = ['input 1', 'input 2', 'input 3', 'input 4', 'input 5', 'input 6', 'input 7', 'input 8', 'input 9',
             'input 10', 'input 11', 'input 12', 'input 13', 'input 14', 'input 15', 'input 16']


class FocusableScroll( VerticalScroll, can_focus=True ):
    pass


class Title(Static):
    pass


class Head(Static):
    """A header widget."""
    def compose(self) -> ComposeResult:
        date = datetime.today().strftime('%Y-%m-%d')
        yield Label('SYSTEM TEST AQ', id='label_company_name', classes='box')
        yield Label(date, id='label_date', classes='box')


class CurrentStage(Static):
    def compose(self) -> ComposeResult:
        curr_stage = 'network'
        yield Label('Текущий этап', id='label_current_stage', classes='box')
        yield Label(curr_stage, id='label_current_stage_name', classes='box')


class StagesTable(Static):

    def __init__(self, rows):
        super().__init__()
        self.rows = rows

    def compose(self) -> ComposeResult:
        yield Static('Прогресс потапно', id='label_progress_header')
        with FocusableScroll():
            yield DataTable(show_header=False, show_row_labels=False, show_cursor=False, id='table_stages')
        # for line in ROWS:
        #     yield ProgressBar(id=line[0])

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.rows[0])
        for number, row in enumerate(self.rows, start=1):
            table.add_row(*row, label=number)

class StageLine(Static):
    def __init__(self, row):
        super().__init__()
        self.row = row
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label(self.row[0])
            yield ProgressBar(total=100, id=f'progress-{self.row[0]}')
            yield Label(self.row[3])

    def _on_mount(self) -> None:
        self.query_one(f'#progress-{self.row[0]}').update(progress=int(self.row[2][:-1]))


class LastInput(Static):
    def compose(self) -> ComposeResult:
        last_input = 'last input placeholder'
        yield Static('Последний ввод', id='label_last_input')
        yield Static(last_input, id='last_input')


class InputLog(Static):
    def compose(self) -> ComposeResult:
        yield Label('Журнал команд', id='label_input_log')
        yield TextLog()

    def on_mount(self) -> None:
        text_log = self.query_one(TextLog)
        for inp in INPUT_LOG:
            text_log.write(inp)


class Sidebar(Container):
    def compose(self) -> ComposeResult:
        yield Label('Код ошибки')
        yield Label('Руководство, что делать при этой ошибке')


class InterfaceApp(App):
    CSS_PATH = 'style.css'
    def __int__(self, stages_table, input_log):
        super().__init__()
        self.stages_table = stages_table
        self.input_log = input_log

    def compose(self) -> ComposeResult:
        yield Container(Head(), Container(StagesTable(ROWS), InputLog(), id='middle_container'),
                        VerticalScroll(id='stages_table_2'), Sidebar())

    # def add_line(self, content):
    #     new_line = StageLine(content)
    #     self.query_one('#stages_table_2').mount(new_line)
    #
    # def remove_line(self):
    #     lines = self.query('#stages_table_2')
    #     if lines:
    #         lines.last().remove()


    def update_table(self, new_table):
        table = self.query_one(DataTable)
        table.clear()
        for number, row in enumerate(new_table, start=1):
            if row[0] == current_stage:
                row = [
                    Text(cell, style="bold #03AC13") for cell in row
                ]
            table.add_row(*row)

    def on_key(self, event: events.Key) -> None:
        if event.key == 'f':
            sidebar = self.query_one(Sidebar)
            self.set_focus(None)
            if sidebar.has_class("-hidden"):
                sidebar.remove_class("-hidden")
            else:
                sidebar.add_class("-hidden")

async def main():
    app = InterfaceApp()
    async def external_input():
        while True:
            rows_prev = ROWS
            await asyncio.sleep(0.2)
            if ROWS != rows_prev:
                app.update_table(ROWS)

    async def randomize_table():
        global ROWS
        global current_stage
        while True:
            tbl = []
            for _ in range(random.randint(1, 8)):
                all_stages = random.randint(1, 8)
                completed = random.randint(0, all_stages)
                percent = int(completed / all_stages * 100)
                s = (random.choice(
                    ['preburn', 'burn', 'inventory', 'functional', 'network', 'memory_stress', 'gpu_stress', 'fio_stress']),
                     f'{random.randint(0, 9)}:{random.randint(0, 59)}:{random.randint(0, 59)}',
                     f'{completed} выполнено',)
                tbl.append(s)
            await asyncio.sleep(1)
            ROWS = tbl
            current_stage = random.choice(
                    ['preburn', 'burn', 'inventory', 'functional', 'network', 'memory_stress', 'gpu_stress', 'fio_stress'])


    runs = [app.run_async(), external_input(), randomize_table()]
    # runs = [app.run_async(), external_input()]
    await asyncio.gather(*runs)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    # app = InterfaceApp()
    # app.stages_table = ROWS
    # app.run()
    # asyncio.run(main())

