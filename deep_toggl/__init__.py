import pendulum
from toggl import api, utils

from .config import get_config
from .evaluator import Evaluator
from .summarizer import Summarizer

__version__ = "0.4"

pendulum.week_starts_at(pendulum.MONDAY)
pendulum.week_ends_at(pendulum.SUNDAY)


def _load_from_toggl(project_name: str, tags: list, token, timezone) -> list:
    config = utils.Config.factory(
        None
    )  # Without None it will load the default config file
    config.api_token = token
    config.timezone = timezone

    start = pendulum.now().start_of("year")

    project = api.Project.objects.filter(name=project_name, config=config)[0]
    project_entries = api.TimeEntry.objects.filter(
        project=project, start=start, tags={*tags}, config=config, contain=False
    )
    return project_entries


def get_evaluator(project_name, tags, token, timezone):
    entries = _load_from_toggl(project_name, tags, token, timezone)
    _evaluator = Evaluator(project_name, entries)
    return _evaluator


def main():
    config = get_config()
    projects = config["projects"]
    today = pendulum.now()
    for project_name in projects:
        evaluator = get_evaluator(
            project_name, config["tags"], config["token"], config["timezone"]
        )
        summarizer = Summarizer(evaluator)
        summarizer.print_averages(today)
    # summarizer.plot(today)
