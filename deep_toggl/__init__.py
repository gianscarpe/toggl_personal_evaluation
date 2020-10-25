import pendulum
from toggl import api, utils

from .config import get_config
from .evaluator import Evaluator
from .summarizer import Summarizer

__version__ = "0.3"

pendulum.week_starts_at(pendulum.MONDAY)
pendulum.week_ends_at(pendulum.SUNDAY)

_evaluator = None


def _load_from_toggl(project_name, tag, token, timezone):
    config = utils.Config.factory(
        None)  # Without None it will load the default config file
    config.api_token = token
    config.timezone = timezone

    start = pendulum.now().start_of('year')
    project = api.Project.objects.filter(project_name,
                                         contain=False,
                                         config=config)[0]
    entries = api.TimeEntry.objects.filter(project=project,
                                           start=start,
                                           tags={tag},
                                           config=config,
                                           contain=False)
    return entries


def get_evaluator():
    config = get_config()
    entries = _load_from_toggl(config['app']['project'], config['app']['tag'],
                               config['toggl']['token'],
                               config['toggl']['timezone'])
    global _evaluator
    if _evaluator is None:
        _evaluator = Evaluator(entries)
    return _evaluator


def main():
    today = pendulum.now()
    summarizer = Summarizer(get_evaluator())
    summarizer.print_averages(today)
    # summarizer.plot(today)
