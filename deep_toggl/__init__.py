import pendulum
from toggl import api

from .config import get_config
from .evaluator import Evaluator
from .summarizer import Summarizer

__version__ = "0.3"

pendulum.week_starts_at(pendulum.MONDAY)
pendulum.week_ends_at(pendulum.SUNDAY)

_evaluator = None


def _load_from_toggl(project_name, tag):
    start = pendulum.now().start_of('year')
    project = api.Project.objects.filter(project_name, contain=False)[0]
    entries = api.TimeEntry.objects.filter(project=project,
                                           start=start,
                                           tags={tag},
                                           contain=False)
    return entries


def get_evaluator():
    config = get_config()
    entries = _load_from_toggl(config['project'], config['tag'])
    global _evaluator
    if _evaluator is None:
        _evaluator = Evaluator(entries)
    return _evaluator


def main():
    today = pendulum.now()
    summarizer = Summarizer(get_evaluator())
    summarizer.print_averages(today)
    summarizer.plot(today)    
