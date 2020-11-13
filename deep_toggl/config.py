import configparser
import os

import inquirer
from inquirer.themes import GreenPassion
from toggl import api, utils
from toggl.utils.others import are_credentials_valid

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.deeptogglrc")


def _store(cfg, config_path=DEFAULT_CONFIG_PATH):
    with open(config_path, "w") as config_file:
        cfg.write(config_file)


def _parse(cfg: configparser.ConfigParser) -> dict:
    result: dict = {}
    result["app"] = {}
    for k in cfg["app"].keys():
        value = cfg["app"][k]
        result["app"][k] = value

    result["projects"] = {}
    for k in cfg["app"]["projects"].split(","):  # projects
        result["projects"][k] = {}
        result["projects"][k]["tags"] = cfg[k]["tags"].split(",")
    return result


def get_api_token():
    return inquirer.shortcuts.password(
        message="Your API token",
        validate=lambda _, current: are_credentials_valid(api_token=current),
    )


def get_config():
    if os.path.exists(DEFAULT_CONFIG_PATH):
        config = configparser.RawConfigParser()
        config.read(DEFAULT_CONFIG_PATH)
    else:
        config = setup()
    return _parse(config)


class TogglWrapper:
    def __init__(self, token: str, tz: str = "utc"):
        self._set_toggl(token, tz)

    def _set_toggl(self, token: str, tz: str = "utc"):
        config = utils.Config.factory(
            None
        )  # Without None it will load the default config file
        config.api_token = token
        config.timezone = "utc"
        self._config = config

    def get_all_projects(self):
        projects = api.Project.objects.filter(config=self._config)
        return projects

    def get_all_tags(self):
        result = api.Tag.objects.filter(config=self._config)
        return result


def setup():
    config = configparser.ConfigParser()
    token = get_api_token()
    tg = TogglWrapper(token)
    projects = tg.get_all_projects()
    tags = tg.get_all_tags()

    projects_names = [p.name for p in projects]
    tags_names = [x.name for x in tags]

    questions = [
        inquirer.Checkbox(
            "projects", message="Which projects to track?", choices=projects_names
        ),
    ]
    answers = inquirer.prompt(questions, theme=GreenPassion())
    projects_chosen = answers["projects"]

    for project_chosen in projects_chosen:
        questions = [
            inquirer.Checkbox(
                "tags",
                message=f"What tags to track for {project_chosen}?",
                choices=tags_names,
            )
        ]
        answers = inquirer.prompt(questions, theme=GreenPassion())

        config[project_chosen] = {}
        config[project_chosen]["tags"] = ",".join(answers["tags"])

    config["app"] = {
        "token": token,
        "projects": ",".join(projects_chosen),
        "timezone": "utc",
    }
    _store(config)
    return config


if __name__ == "__main__":
    setup()
