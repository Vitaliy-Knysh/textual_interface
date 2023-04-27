from textual.app import App, ComposeResult, RenderableType
from textual.widgets import Static, Label, Input, Button, DataTable, TextLog
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.scroll_view import ScrollView
from textual.widget import Widget
from textual.geometry import Size
from textual.reactive import reactive
from rich.progress import Progress, BarColumn
from datetime import datetime
import random
import time


ROWS = [
    ('preburn', '0:00:00', '100%', '(1 из 1 выполнено)'),
    ('burn', '0:00:00', '100%', '(2 из 2 выполнено)'),
    ('inventory', '0:00:00', '100%', '(2 из 2 выполнено)'),
    ('functional', '0:00:01', '100%', '(3 из 3 выполнено)'),
    ('nework', '0:00:01', '100%', '(1 из 1 выполнено)'),
    ('memory_stress', '0:00:00', '0%', '(0 из 1 выполнено)'),
    ('gpu_stress', '0:00:00', '0%', '(0 из 1 выполнено)'),
    ('fio_stress', '0:00:00', '0%', '(0 из 1 выполнено)'),
]

ROWS2 = [
    ('preburn', '0:00:00', '0%', '(1 из 1 выполнено)'),
    ('burn', '0:00:00', '0%', '(2 из 2 выполнено)'),
    ('inventory', '0:00:00', '0%', '(2 из 2 выполнено)'),
    ('functional', '0:00:01', '0%', '(3 из 3 выполнено)'),
    ('nework', '0:00:01', '0%', '(1 из 1 выполнено)'),
    ('memory_stress', '0:00:00', '0%', '(0 из 1 выполнено)'),
    ('gpu_stress', '0:00:00', '0%', '(0 из 1 выполнено)'),
    ('fio_stress', '0:00:00', '0%', '(0 из 1 выполнено)'),
]

stage_col = ['preburn', 'burn', 'inventory', 'functional', 'network', 'memory_stress', 'gpu_stress', 'fio_stress',
             'total']
timer_col = ['0:00:00', '0:00:00', '0:00:00', '0:00:01', '0:00:01', '0:00:13', '0:00:13', '0:00:13', '0:00:40']
percentage_col = ['100%', '100%', '100%', '100%', '100%', '0%', '0%', '0%', '62%']
summary_col = ['(1 из 1 выполнено)', '(2 из 2 выполнено)', '(2 из 2 выполнено)', '(3 из 3 выполнено)',
               '(1 из 1 выполнено)', '(0 из 1 выполнено)', '(0 из 1 выполнено)', '(0 из 1 выполнено)',
               '(5 из 8 выполнено)']
time_elapsed = '0:00:13'
overall_percent = '62%'
overall_summary = '5 из 8 выполнено'
INPUT_LOG = ['input 1', 'input 2', 'input 3', 'input 4', 'input 5', 'input 6', 'input 7', 'input 8', 'input 9',
             'input 10', 'input 11', 'input 12', 'input 13', 'input 14', 'input 15', 'input 16']


class FocusableScroll( VerticalScroll, can_focus=True ):
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

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.rows[0])
        for number, row in enumerate(self.rows, start=1):
            table.add_row(*row, label=number)


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


class InterfaceApp(App):
    CSS_PATH = 'style.css'
    def __int__(self, stages_table, input_log):
        super().__init__()
        self.stages_table = stages_table
        self.input_log = input_log

    def compose(self) -> ComposeResult:
        yield Container(Head(), CurrentStage(), Container(StagesTable(ROWS), InputLog(), id='middle_container'),
                        LastInput(), Input(placeholder='Введите команду'), Button('Таблица', id='btn_randomize_table'),
                        Button('Этап', id='btn_stage'))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'btn_randomize_table':
            # table = self.query_one(DataTable)
            # for row in range(len(ROWS)):
            #     table.update_cell_at([row, 2], f'{random.randint(0, 100)}%')
            tbl = []
            for _ in range(8):
                all_stages = random.randint(1, 8)
                completed = random.randint(0, all_stages)
                percent = int(completed / all_stages * 100)
                s = (random.choice(['preburn', 'burn', 'inventory', 'functional', 'network', 'memory_stress', 'gpu_stress', 'fio_stress']),
                                    f'{random.randint(0, 9)}:{random.randint(0, 59)}:{random.randint(0, 59)}',
                                    f'{percent}%',
                                    f'{completed} из {all_stages} выполнено',)
                tbl.append(s)
            self.update_table(tbl)
        if event.button.id == 'btn_stage':
            label = self.query_one('#label_current_stage_name')
            new_text = random.choice(['preburn', 'burn', 'inventory', 'functional', 'network', 'memory_stress',
                                     'gpu_stress', 'fio_stress'])
            label.update(new_text)


    def on_input_submitted(self):
        text_log = self.query_one(TextLog)
        label = self.query_one('#last_input')
        table = self.query_one(DataTable)
        input_field = self.query_one(Input)
        text_log.write(input_field.value)
        label.update(input_field.value)
        input_field.action_delete_left_all()
        table.add_row('fio_stress', '0:00:00', '0%', '(0 из 1 выполнено)')

    def update_table(self, new_table):
        table = self.query_one(DataTable)
        for row in new_table:
            for cell, content in enumerate(row):
                table.update_cell_at([new_table.index(row), cell], content)



if __name__ == "__main__":
    app = InterfaceApp()
    app.stages_table = ROWS
    app.run()
