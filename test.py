import time

from beerprogress import BeerProgress

bp = BeerProgress()
bp.total_tasks = 1075

for x in range(bp.total_tasks):
    bp.tick()
    bp.print_progress()
    time.sleep(0.01)
    if x % 10 == 0:
        bp.skipped_tasks += 1
    else:
        bp.completed_tasks += 1

print("\n")

