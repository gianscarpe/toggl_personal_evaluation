import configparser
import os

import inquirer
from inquirer.themes import GreenPassion
from toggl.utils.others import are_credentials_valid

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.deeptogglrc")


def _store(cfg, config_path=DEFAULT_CONFIG_PATH):
    with open(config_path, "w") as config_file:
        cfg.write(config_file)


def get_api_token():
    return inquirer.shortcuts.password(
        message="Your API token",
        validate=lambda _, current: are_credentials_valid(api_token=current),
    )


def get_config():
    if os.path.exists(DEFAULT_CONFIG_PATH):
        reading_config = configparser.RawConfigParser()
        reading_config.read(DEFAULT_CONFIG_PATH)
        config = {}
        config = {
            "tags": reading_config["app"]["tags"].split(","),
            "projects": reading_config["app"]["projects"].split(","),
            "token": reading_config["toggl"]["token"],
            "timezone": reading_config["toggl"]["timezone"],
        }
    else:
        config = setup()
    return config


def setup():
    config = configparser.ConfigParser()
    config["app"] = {}
    config["toggl"] = {}
    token = get_api_token()
    questions = [
        inquirer.Text("name", message="What's your name?"),
        inquirer.Text(
            "tags",
            message="What tags to track?",
        ),
        inquirer.Text(
            "projects",
            message="Which projects to track?",
        ),
    ]
    answers = inquirer.prompt(questions, theme=GreenPassion())
    config["app"] = {
        "username": answers["name"],
        "tag": answers["tag"],
        "project": answers["project"],
    }
    config["toggl"] = {"token": token, "timezone": "utc"}

    _store(config)
    return config


if __name__ == "__main__":
    setup()
