import argparse

import pendulum

from .config import get_config, setup
from .evaluator import get_evaluator
from .summarizer import Summarizer

__version__ = "0.6"


pendulum.week_starts_at(pendulum.MONDAY)
pendulum.week_ends_at(pendulum.SUNDAY)


def summarize_project(name, config, date: pendulum.Date):
    evaluator = get_evaluator(name, config["projects"][name], config["app"])
    summarizer = Summarizer(evaluator)

    summarizer.print_averages(date)
    summarizer.plot(date)


def summarize_all(config, date: pendulum.Date):
    for name in config["projects"]:
        summarize_project(name, config, date)


def summarize_dispatch(project_name):
    today = pendulum.now()
    cfg = get_config()

    if project_name == "all":
        summarize_all(cfg, today)
    else:
        summarize_project(project_name, cfg, today)


def parse_args():
    parser = argparse.ArgumentParser(description="Deep toggl")
    parser.add_argument(
        "project", nargs="?", type=str, default="all", help="Project name. Defaults to `all`",
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        default=False,
        help="Set-up the tool. If a configuration is presents, it will be overwritten.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.setup:
        _ = setup()
    else:
        project_name = args.project
        summarize_dispatch(project_name)


if __name__ == "__main__":
    main()
