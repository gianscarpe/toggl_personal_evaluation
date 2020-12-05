import configparser
import os
from typing import List

import inquirer
from inquirer.themes import GreenPassion
from toggl import api, utils
from toggl.utils.others import are_credentials_valid

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.deeptogglrc")
ANY_TAG = "any"


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
        message="Your API token", validate=lambda _, current: are_credentials_valid(api_token=current),
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
        config = utils.Config.factory(None)  # Without None it will load the default config file
        config.api_token = token
        config.timezone = "utc"
        self._config = config

    def get_all_projects(self):
        projects = api.Project.objects.filter(config=self._config)
        return projects

    def get_all_tags(self):
        result = api.Tag.objects.filter(config=self._config)
        return result


def get_chosen_projects(toggl_wrapper: TogglWrapper) -> List[str]:
    projects_names = [x.name for x in toggl_wrapper.get_all_projects()]
    while True:
        questions = [
            inquirer.Checkbox("projects", message="Which projects to track?", choices=projects_names,),
        ]
        answers = inquirer.prompt(questions, theme=GreenPassion())
        projects_chosen = answers["projects"]
        if len(projects_chosen) != 0:
            return projects_chosen
        print("You have to pick at least one project.")


def get_chosen_tags(toggl_wrapper: TogglWrapper, chosen_project: str) -> List[str]:
    tags_names = [ANY_TAG]
    tags_names.extend(x.name for x in toggl_wrapper.get_all_tags())
    questions = [inquirer.Checkbox("tags", message=f"What tags to track for {chosen_project}?", choices=tags_names,)]
    answers = inquirer.prompt(questions, theme=GreenPassion())
    return answers["tags"]


def setup():
    config = configparser.ConfigParser()
    token = get_api_token()
    toggl_wrap = TogglWrapper(token)

    chosen_projects = get_chosen_projects(toggl_wrap)
    for chosen_project in chosen_projects:
        chosen_tags = get_chosen_tags(toggl_wrap, chosen_project)
        config[chosen_project] = {}
        config[chosen_project]["tags"] = ",".join(chosen_tags)

    config["app"] = {
        "token": token,
        "projects": ",".join(chosen_projects),
        "timezone": "utc",
    }
    _store(config)
    return config


if __name__ == "__main__":
    setup()
