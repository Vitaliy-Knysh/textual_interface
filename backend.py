import threading

from interface import InterfaceApp
import random
import time
from threading import Thread


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


if __name__ == "__main__":
    app = InterfaceApp()
    app.stages_table = ROWS
    thread1 = Thread(target=app.run())
    thread1.start()

