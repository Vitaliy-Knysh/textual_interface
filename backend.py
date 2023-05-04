import threading

import interface
from interface import InterfaceApp
import random
import time
import asyncio
from threading import Thread

def randomize_table():
    global ROWS
    while True:
        tbl = []
        for _ in range(8):
            all_stages = random.randint(1, 8)
            completed = random.randint(0, all_stages)
            percent = int(completed / all_stages * 100)
            s = (random.choice(
                ['preburn', 'burn', 'inventory', 'functional', 'network', 'memory_stress', 'gpu_stress', 'fio_stress']),
                 f'{random.randint(0, 9)}:{random.randint(0, 59)}:{random.randint(0, 59)}',
                 f'{percent}%',
                 f'{completed} из {all_stages} выполнено',)
            tbl.append(s)
        await asyncio.sleep(1)
        ROWS = tbl

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    randomize_table()
    loop.run_until_complete(interface.main())