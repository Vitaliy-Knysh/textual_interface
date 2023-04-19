from textual.app import App, ComposeResult, RenderableType
from textual.widgets import Welcome, Static, Label, Button, Header, Footer, DataTable, LoadingIndicator
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.scroll_view import ScrollView
from textual.widget import Widget
from textual.geometry import Size
from textual.reactive import reactive
from rich.progress import Progress, BarColumn
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
stage_col = ['preburn', 'burn', 'inventory', 'functional', 'nework', 'memory_stress', 'gpu_stress', 'fio_stress',
             'total']
timer_col = ['0:00:00', '0:00:00', '0:00:00', '0:00:01', '0:00:01', '0:00:13', '0:00:13', '0:00:13', '0:00:40']
percentage_col = ['100%', '100%', '100%', '100%', '100%', '0%', '0%', '0%', '62%']
summary_col = ['(1 из 1 выполнено)', '(2 из 2 выполнено)', '(2 из 2 выполнено)', '(3 из 3 выполнено)',
               '(1 из 1 выполнено)', '(0 из 1 выполнено)', '(0 из 1 выполнено)', '(0 из 1 выполнено)',
               '(5 из 8 выполнено)']
time_elapsed = '0:00:13'
overall_percent = '62%'
overall_summary = '5 из 8 выполнено'
input_log = ['input 1', 'input 2', 'input 3', 'input 4', 'input 5', 'input 6', 'input 7', 'input 8', 'input 9',
             'input 10', 'input 11', 'input 12', 'input 13', 'input 14', 'input 15', 'input 16']

class Head(Static):
    """A header widget."""
    def compose(self) -> ComposeResult:
        date = datetime.today().strftime('%Y-%m-%d')
        yield Label('SYSTEM TEST AQ', id='label_company_name', classes='box')
        yield Label(date, id='label_date', classes='box')


# class IntervalUpdater(Static):
#     _renderable_object: RenderableType
#
#     def update_rendering(self) -> None:
#         self.update(self._renderable_object)
#
#     def on_mount(self) -> None:
#         self.interval_update = self.set_interval(1 / 60, self.update_rendering)


# class IndeterminateProgressBar(IntervalUpdater):
#     """Basic indeterminate progress bar widget based on rich.progress.Progress."""
#     def __init__(self) -> None:
#         super().__init__("")
#         self._renderable_object = Progress(BarColumn())
#         self._renderable_object.add_task("", total=None)


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
            # with Vertical():
            #     for stage in percentage_col:
            #         yield IndeterminateProgressBar()
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


class InputLog(Static):
    def compose(self) -> ComposeResult:
        yield Label('Журнал команд', id='label_input_log')
        with VerticalScroll():
            for input in input_log:
                yield Label(input, classes='inputs')


# class OverallProgress(Static):
#     def compose(self) -> ComposeResult:
#         yield Static('Общий прогресс', id='label_overall_progress')
#         with Horizontal(id='progress_string'):
#             yield Label('Total ', classes='label_total')
#             yield Label(f'{time_elapsed} ', classes='table_timer')
#             yield Label(f'{overall_percent} ', classes='table_percent')
#             yield Label(f'{overall_summary} ')


class WelcomeApp(App):
    CSS_PATH = 'style.css'

    def compose(self) -> ComposeResult:
        # yield Container(Head(), CurrentStage(), DataTable(show_header=False, show_cursor=False))
        yield Container(Head(), CurrentStage(), Container(StagesTable(), InputLog(), id='middle_container'),
                        LastInput())
        # yield Container(, LastInput())

    # def on_mount(self) -> None:
    #     table = self.query_one(DataTable)
    #     rows = iter(ROWS)
    #     table.add_columns(*next(rows))
    #     table.add_rows(rows)


if __name__ == "__main__":
    app = WelcomeApp()
    app.run()
