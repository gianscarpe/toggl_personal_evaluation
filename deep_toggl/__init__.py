import pendulum
from toggl import api

from .config import DEEP_TAG, PROJECT_NAME
from .evaluator import Evaluator

pendulum.week_starts_at(pendulum.MONDAY)
pendulum.week_ends_at(pendulum.SUNDAY)

_evaluator = None

def _load_from_toggl(project_name, tags):
    start = pendulum.now().start_of('year')
    project = api.Project.objects.filter(project_name, contain=False)[0]
    entries = api.TimeEntry.objects.filter(project=project,
                                           start=start,
                                           tags=tags,
                                           contain=True)
    return entries


def get_evaluator():
    entries = _load_from_toggl(PROJECT_NAME, DEEP_TAG)
    global _evaluator
    if _evaluator is None:
        _evaluator = Evaluator(entries)
    return _evaluator


def main():
    today = pendulum.now()
    get_evaluator().print_averages(today)
    get_evaluator().plot(today)
