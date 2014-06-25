# beerprogress

Command line progress indicator library Python

![alt text](https://raw.githubusercontent.com/fcvarela/beerprogress/master/shot.png "Screenshot")

### Usage:
    import os
    import time

    from beerprogress import BeerProgress

    bp = BeerProgress()
    bp.total_tasks = 1075

    for x in range(bp.total_tasks):
        bp.tick()
        # or get the string and log it
        bp.print_progress(os.stderr, single_line=True)
        # sleep so we can enjoy the beauty of this
        time.sleep(0.01)
        # skip something every once in a while
        if x % 10 == 0:
            bp.skipped_tasks += 1
        else:
            bp.completed_tasks += 1
