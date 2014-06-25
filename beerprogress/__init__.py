import os
import psutil
import sys


__all__ = [
    'BeerProgress'
]


_default_display = {
    'cpu': True,
    'mem': True,
    'progressbar': True,
    'percent': True,
    'tasks_ratio': True,
    'skipped_tasks': True,
    'fd_count': True,
    'context_switches': True
}


class BeerProgress(object):
    def __init__(self, indicator='#', total_tasks=0, display=_default_display, progress_character='\U0001F37A'):
        self.indicator = indicator
        self._total_tasks = total_tasks
        self._completed_tasks = 0
        self._skipped_tasks = 0
        self.progress_character = progress_character

        for s in display:
            if s not in _default_display:
                raise ValueError("Unsupported display item: %s", s)

        self.display = display
        self.proc = psutil.Process(os.getpid())
        self.metrics = {
            'cpu': 0,
            'mem': 0,
            'percent': 0,
            'fds': 0,
            'ctxv': 0,
            'ctxi': 0
        }

    @property
    def completed_tasks(self):
        return self._completed_tasks

    @completed_tasks.setter
    def completed_tasks(self, completed_tasks):
        self._completed_tasks = completed_tasks

    @property
    def total_tasks(self):
        return self._total_tasks

    @total_tasks.setter
    def total_tasks(self, total_tasks):
        self._total_tasks = total_tasks

    @property
    def skipped_tasks(self):
        return self._skipped_tasks

    @skipped_tasks.setter
    def skipped_tasks(self, skipped_tasks):
        self._skipped_tasks = skipped_tasks

    def print_progress(self, same_line=True, stream=sys.stderr):
        if same_line:
            stream.write('\r' + self.progress_string())
        else:
            stream.write(self.progress_string()+'\n')

    def tick(self):
        if self._total_tasks == 0:
            raise ValueError("Cannot tick without total tasks set")

        self.metrics['percent'] = float((self.completed_tasks + self.skipped_tasks) * 100.0 / self.total_tasks)

        self.metrics['cpu'] = float(self.proc.get_cpu_percent(interval=0))
        self.metrics['mem'] = float(self.proc.get_memory_info()[0]/1024.0/1024.0)

        self.metrics['fds'] = self.proc.get_num_fds()
        self.metrics['ctxv'] = self.proc.get_num_ctx_switches()[0]
        self.metrics['ctxi'] = self.proc.get_num_ctx_switches()[1]

    def progress_string(self, length=20):
        # in characters, not bytes
        pb_symbol_length = int(self.metrics['percent'] * length / 100)
        pb_spaces_length = length - pb_symbol_length

        full_pb = self.progress_character * length
        pb_string = full_pb[:pb_symbol_length*len(self.progress_character)] + pb_spaces_length * ' '

        status = ""

        if "cpu" in self.display:
            status += "CPU %6.2f%% " % self.metrics['cpu']

        if "mem" in self.display:
            status += "Mem %6.2fMB " % self.metrics['mem']

        if "progressbar" in self.display:
            status += pb_string + " "

        if "percent" in self.display:
            status += "[%6.2f%%] " % self.metrics['percent']

        if "tasks_ratio" in self.display:
            status += "Complete: %d/%d " % (self.completed_tasks+self.skipped_tasks, self.total_tasks)

        if "skipped_tasks" in self.display:
            status += "Skipped: %d " % self.skipped_tasks

        if "fd_count" in self.display:
            status += "CTXvol: %d CTXinvol: %d" % (self.metrics['ctxv'], self.metrics['ctxi'])

        return status
