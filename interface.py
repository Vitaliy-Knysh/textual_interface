from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Welcome, Static, Label, Button, Header, Footer, DataTable
from textual.containers import Container, Horizontal, Vertical
from textual.widget import Widget
from textual.reactive import reactive
from datetime import datetime

ROWS = [
    ['preburn', '0:00:00', '100%', '(1 из 1 выполнено)'],
    ['burn', '0:00:00', '100%', '(2 из 2 выполнено)'],
    ['inventory', '0:00:00', '100%', '(2 из 2 выполнено)'],
    ['functional', '0:00:01', '100%', '(3 из 3 выполнено)'],
    ['nework', '0:00:01', '100%', '(1 из 1 выполнено)'],
    ['memory_stress', '0:00:00', '0%', '(0 из 1 выполнено)'],
    ['gpu_stress', '0:00:00', '0%', '(0 из 1 выполнено)'],
    ['fio_stress', '0:00:00', '0%', '(0 из 1 выполнено)'],
]
stage_col = ['preburn', 'burn', 'inventory', 'functional', 'nework', 'memory_stress', 'gpu_stress', 'fio_stress']
timer_col = ['0:00:00', '0:00:00', '0:00:00', '0:00:01', '0:00:01', '0:00:13', '0:00:13', '0:00:13']
percentage_col = ['100%', '100%', '100%', '100%', '100%', '0%', '0%', '0%']
summary_col = ['(1 из 1 выполнено)', '(2 из 2 выполнено)', '(2 из 2 выполнено)', '(3 из 3 выполнено)',
               '(1 из 1 выполнено)', '(0 из 1 выполнено)', '(0 из 1 выполнено)', '(0 из 1 выполнено)']
time_elapsed = '0:00:13'
overall_percent = '62%'
overall_summary = '5 из 8 выполнено'

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
    def compose(self) -> ComposeResult:
        yield Static('Прогресс потапно', id='label_progress_header')
        with Horizontal():
            with Vertical():
                for stage in stage_col:
                    yield Label(stage, classes='table_stage')
            with Vertical():
                for stage in timer_col:
                    yield Label(stage, classes='table_timer')
            with Vertical():
                for stage in percentage_col:
                    yield Label(stage, classes='table_percent')
            with Vertical():
                for stage in summary_col:
                    yield Label(stage, classes='table_summary')


class LastInput(Static):
    def compose(self) -> ComposeResult:
        last_input = 'last input placeholder'
        yield Static('Последний ввод', id='label_last_input')
        yield Static(last_input, id='last_input')


class OverallProgress(Static):
    def compose(self) -> ComposeResult:
        yield Static('Общий прогресс', id='label_overall_progress')
        with Horizontal(id='progress_string'):
            yield Label('Total ', classes='label_total')
            yield Label(f'{time_elapsed} ', classes='table_timer')
            yield Label(f'{overall_percent} ', classes='table_percent')
            yield Label(f'{overall_summary} ')


class WelcomeApp(App):
    CSS_PATH = 'style.css'

    def compose(self) -> ComposeResult:
        # yield Container(Head(), CurrentStage(), DataTable(show_header=False, show_cursor=False))
        yield Container(Head(), CurrentStage(), Container(StagesTable(), LastInput(), id='middle_container'),
                        OverallProgress())
        # yield Container(, LastInput())

    # def on_mount(self) -> None:
    #     table = self.query_one(DataTable)
    #     rows = iter(ROWS)
    #     table.add_columns(*next(rows))
    #     table.add_rows(rows)


if __name__ == "__main__":
    app = WelcomeApp()
    app.run()
