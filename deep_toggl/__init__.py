import argparse

import pendulum

from .config import get_config
from .evaluator import Evaluator
from .summarizer import Summarizer
from .togglwrapper import load_from_toggl

__version__ = "0.6"


pendulum.week_starts_at(pendulum.MONDAY)
pendulum.week_ends_at(pendulum.SUNDAY)


def get_evaluator(project_name, config_project, config_app):
    entries = load_from_toggl(
        project_name=project_name,
        tags=config_project["tags"],
        token=config_app["token"],
        timezone=config_app["timezone"],
    )
    _evaluator = Evaluator(name=project_name, entries=entries)
    return _evaluator


def summarize_project(name, config, date: pendulum.Date):
    evaluator = get_evaluator(name, config["projects"][name], config["app"])
    summarizer = Summarizer(evaluator)
    summarizer.print_averages(date)
    summarizer.plot(date)


def summarize_all(config, date: pendulum.Date):
    for name in config["projects"].keys():
        summarize_project(name, config, date)


def summarize_dispatch(project_name):
    today = pendulum.now()
    config = get_config()

    if project_name == "all":
        summarize_all(config, today)
    else:
        summarize_project(project_name, config, today)


def main():
    parser = argparse.ArgumentParser(description="Deep toggl")
    parser.add_argument("project", metavar="project", type=str, help="Project name")

    args = parser.parse_args()
    project_name = args.project
    summarize_dispatch(project_name)
